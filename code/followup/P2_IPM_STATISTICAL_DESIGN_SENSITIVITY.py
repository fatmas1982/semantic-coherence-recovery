#!/usr/bin/env python3
"""Post-hoc statistical-design sensitivity analyses for the IP&M manuscript.

This script does NOT retrain any model. It operates on frozen OOF predictions to:
1) audit class support in every outer fold after target-specific gold filtering; and
2) compare the ordinary Prompt_ID-cluster bootstrap with a task-stratified
   Prompt_ID-cluster bootstrap that preserves the designed six-task composition.

Expected public inputs after unpacking the repository release:
- baseline OOF CSV mirrors (OOF_T1.csv ... OOF_T4.csv), with columns
  Case_ID, Prompt_ID, Task_Type, Fold, y_true, M0_pred, M1_pred, M2_pred, Human_Easy;
- M3 OOF files OOF_M3_T{1..4}_{A,B,C}_seed20260908.csv;
- archived P1/identity M4 OOF files, either one file per target or a directory
  containing OOF_M4_SENS_T{1..4}_P1_identity.csv.

The bootstrap unit is Prompt_ID. In the task-stratified sensitivity, Prompt_IDs
are sampled with replacement independently inside each Task_Type. All eligible
rows belonging to a sampled Prompt_ID are retained, including repeated draws.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, f1_score

TARGETS = ("T1", "T2", "T3", "T4")
LABELS = {"T1": [0, 1], "T2": [0, 1], "T3": [0, 1], "T4": [1, 2, 3]}
SEED = 20260908
N_BOOT = 2000


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--baseline-dir", type=Path, required=True,
                   help="Directory containing OOF_T1.csv ... OOF_T4.csv")
    p.add_argument("--m3-dir", type=Path, required=True,
                   help="Directory containing OOF_M3_T*_A/B/C_seed20260908.csv")
    p.add_argument("--m4-dir", type=Path, required=True,
                   help="Directory containing archived P1/identity M4 OOF files")
    p.add_argument("--out-dir", type=Path, default=Path("reproduced_statistical_design"))
    p.add_argument("--bootstrap-reps", type=int, default=N_BOOT)
    p.add_argument("--seed", type=int, default=SEED)
    return p.parse_args()


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def load_baseline(base: Path, t: str) -> pd.DataFrame:
    candidates = [base / f"OOF_{t}.csv", base / f"{t}.csv"]
    for p in candidates:
        if p.exists():
            return read_csv(p)
    raise FileNotFoundError(f"No baseline OOF CSV found for {t} in {base}")


def load_m3(base: Path, t: str, cond: str) -> pd.DataFrame:
    return read_csv(base / f"OOF_M3_{t}_{cond}_seed20260908.csv")


def load_m4(base: Path, t: str) -> pd.DataFrame:
    candidates = [
        base / f"OOF_M4_SENS_{t}_P1_identity.csv",
        base / f"OOF_M4_{t}_C.csv",
    ]
    for p in candidates:
        if p.exists():
            d = read_csv(p)
            if "condition" in d.columns:
                d = d[d["condition"].astype(str).str.upper().eq("C")].copy()
            if "template" in d.columns:
                d = d[d["template"].astype(str).eq("P1")].copy()
            if "permutation" in d.columns:
                d = d[d["permutation"].astype(str).eq("identity")].copy()
            return d
    raise FileNotFoundError(f"No archived P1/identity M4 OOF found for {t} in {base}")


def pred_col(df: pd.DataFrame, prefix: str) -> str:
    for c in (f"{prefix}_pred", "y_pred", "pred"):
        if c in df.columns:
            return c
    raise KeyError(f"Prediction column for {prefix} not found: {list(df.columns)}")


def macro_f1(y: Sequence[int], p: Sequence[int], t: str) -> float:
    return float(f1_score(y, p, labels=LABELS[t], average="macro", zero_division=0))


def qwk(y: Sequence[int], p: Sequence[int]) -> float:
    return float(cohen_kappa_score(y, p, labels=LABELS["T4"], weights="quadratic"))


def parse_probs(x) -> np.ndarray:
    if isinstance(x, str):
        try:
            return np.asarray(ast.literal_eval(x), dtype=float)
        except Exception:
            return np.asarray(json.loads(x), dtype=float)
    return np.asarray(x, dtype=float)


def norm_entropy(probs: Iterable) -> np.ndarray:
    out = []
    for x in probs:
        p = parse_probs(x)
        p = np.clip(p, 1e-15, 1.0)
        p = p / p.sum()
        out.append(float(-(p * np.log(p)).sum() / np.log(len(p))))
    return np.asarray(out)


def sampled_row_indices(df: pd.DataFrame, rng: np.random.Generator, stratified: bool) -> np.ndarray:
    chunks: List[np.ndarray] = []
    if stratified:
        tasks = sorted(df["Task_Type"].dropna().unique())
        for task in tasks:
            sub = df[df["Task_Type"] == task]
            prompts = np.asarray(sorted(sub["Prompt_ID"].unique()))
            sampled = rng.choice(prompts, size=len(prompts), replace=True)
            lookup = {pid: sub.index[sub["Prompt_ID"] == pid].to_numpy() for pid in prompts}
            chunks.extend(lookup[pid] for pid in sampled)
    else:
        prompts = np.asarray(sorted(df["Prompt_ID"].unique()))
        sampled = rng.choice(prompts, size=len(prompts), replace=True)
        lookup = {pid: df.index[df["Prompt_ID"] == pid].to_numpy() for pid in prompts}
        chunks.extend(lookup[pid] for pid in sampled)
    return np.concatenate(chunks)


def bootstrap_single(df: pd.DataFrame, func, reps: int, seed: int, stratified: bool) -> Tuple[float, float]:
    rng = np.random.default_rng(seed)
    vals = np.empty(reps, dtype=float)
    for b in range(reps):
        idx = sampled_row_indices(df, rng, stratified)
        vals[b] = func(df.loc[idx])
    return tuple(np.quantile(vals, [0.025, 0.975]))


def add_pred(base: pd.DataFrame, d: pd.DataFrame, outcol: str, source_prefix: str) -> pd.DataFrame:
    c = pred_col(d, source_prefix)
    return base.merge(d[["Case_ID", c]].rename(columns={c: outcol}), on="Case_ID", how="left", validate="one_to_one")


def interval_rows_for_single(section: str, target: str, contrast: str, metric: str,
                             df: pd.DataFrame, func, reps: int, seed: int) -> Dict[str, object]:
    point = func(df)
    lo_u, hi_u = bootstrap_single(df, func, reps, seed, False)
    lo_s, hi_s = bootstrap_single(df, func, reps, seed, True)
    return {
        "section": section, "target": target, "contrast": contrast, "metric": metric,
        "point": point,
        "unstratified_low": lo_u, "unstratified_high": hi_u,
        "task_stratified_low": lo_s, "task_stratified_high": hi_s,
        "max_endpoint_shift": max(abs(lo_s-lo_u), abs(hi_s-hi_u)),
        "zero_inclusion_changed": ((lo_u <= 0 <= hi_u) != (lo_s <= 0 <= hi_s)),
    }


def fold_audit(m3_dir: Path) -> pd.DataFrame:
    rows = []
    for t in TARGETS:
        d = load_m3(m3_dir, t, "C")
        for fold, s in d.groupby("Fold", sort=True):
            vc = s["y_true"].value_counts().to_dict()
            rec = {
                "target": t, "fold": int(fold), "rows": len(s),
                "prompt_clusters": s["Prompt_ID"].nunique(),
                "class_0_n": vc.get(0, ""), "class_1_n": vc.get(1, ""),
                "class_2_n": vc.get(2, ""), "class_3_n": vc.get(3, ""),
            }
            rec["min_class_n"] = min(int(vc.get(k, 0)) for k in LABELS[t])
            rows.append(rec)
    return pd.DataFrame(rows)


def main() -> None:
    a = args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    audit = fold_audit(a.m3_dir)
    audit.to_csv(a.out_dir / "P2_IPM_FOLD_BY_CLASS_AUDIT.csv", index=False)
    if (audit["min_class_n"] <= 0).any():
        raise AssertionError("At least one outer-fold target class is absent")

    results: List[Dict[str, object]] = []

    for t in TARGETS:
        b = load_baseline(a.baseline_dir, t)
        m3 = load_m3(a.m3_dir, t, "C")
        m4 = load_m4(a.m4_dir, t)
        base = b[["Case_ID", "Prompt_ID", "Task_Type", "y_true"]].copy()
        for model in ("M0", "M1", "M2"):
            base = add_pred(base, b, model, model)
        base = add_pred(base, m3, "M3", "M3")
        base = add_pred(base, m4, "M4", "M4")

        for model in ("M0", "M1", "M2", "M3", "M4"):
            results.append(interval_rows_for_single(
                "Table16", t, model, "macro-F1", base,
                lambda x, m=model, tt=t: macro_f1(x.y_true, x[m], tt), a.bootstrap_reps, a.seed))
            if t == "T4":
                results.append(interval_rows_for_single(
                    "Table16", t, model, "QWK", base,
                    lambda x, m=model: qwk(x.y_true, x[m]), a.bootstrap_reps, a.seed))

        for name, left, right in (("M3-M1", "M3", "M1"), ("M4-M3", "M4", "M3")):
            results.append(interval_rows_for_single(
                "Table17", t, name, "delta macro-F1", base,
                lambda x, l=left, r=right, tt=t: macro_f1(x.y_true, x[l], tt) - macro_f1(x.y_true, x[r], tt),
                a.bootstrap_reps, a.seed))

        ma, mb, mc = load_m3(a.m3_dir, t, "A"), load_m3(a.m3_dir, t, "B"), load_m3(a.m3_dir, t, "C")
        e = ma[["Case_ID", "Prompt_ID", "Task_Type", "y_true"]].copy()
        e = add_pred(e, ma, "A", "M3")
        e = add_pred(e, mb, "B", "M3")
        e = add_pred(e, mc, "C", "M3")
        for name, left, right in (("M3 B-A", "B", "A"), ("M3 C-B", "C", "B")):
            results.append(interval_rows_for_single(
                "Table18", t, name, "delta macro-F1", e,
                lambda x, l=left, r=right, tt=t: macro_f1(x.y_true, x[l], tt) - macro_f1(x.y_true, x[r], tt),
                a.bootstrap_reps, a.seed))

        h = mc.copy()
        pcol = pred_col(h, "M3")
        if "Human_Easy" not in h.columns or "M3_probs" not in h.columns:
            raise KeyError("M3 OOF must include Human_Easy and M3_probs for Table 19 sensitivity")
        h["err"] = (h[pcol].astype(int) != h["y_true"].astype(int)).astype(float)
        h["entropy"] = norm_entropy(h["M3_probs"])
        h["Human_Easy"] = h["Human_Easy"].astype(str).str.lower().map({"true": True, "false": False}).fillna(h["Human_Easy"]).astype(bool)

        def delta_group(x, col):
            hard = x.loc[~x.Human_Easy, col]
            easy = x.loc[x.Human_Easy, col]
            return float(hard.mean() - easy.mean())

        results.append(interval_rows_for_single(
            "Table19", t, "hard-easy", "error delta", h,
            lambda x: delta_group(x, "err"), a.bootstrap_reps, a.seed))
        results.append(interval_rows_for_single(
            "Table19", t, "hard-easy", "normalized entropy delta", h,
            lambda x: delta_group(x, "entropy"), a.bootstrap_reps, a.seed))

    out = pd.DataFrame(results)
    out.to_csv(a.out_dir / "P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SENSITIVITY.csv", index=False)
    summary = out.groupby("section", as_index=False).agg(
        intervals=("section", "size"),
        max_endpoint_shift=("max_endpoint_shift", "max"),
        zero_inclusion_changes=("zero_inclusion_changed", "sum"),
    )
    summary.to_csv(a.out_dir / "P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SUMMARY.csv", index=False)
    print(summary.to_string(index=False))
    print("Minimum fold-by-class count:", int(audit.min_class_n.min()))


if __name__ == "__main__":
    main()
