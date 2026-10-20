#!/usr/bin/env python3
"""Audit archived M4 Condition-C predictions by generating checkpoint.

This is a descriptive, post-hoc audit. It does not identify self-preference:
generator strata differ in their output content and reference-label balance.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score


def score(frame, labels):
    return f1_score(frame.y_true, frame.M4_pred, labels=labels, average="macro", zero_division=0)


def macro_from_cm(cm):
    tp = np.diag(cm)
    denom = cm.sum(axis=0) + cm.sum(axis=1)
    return float(np.divide(2 * tp, denom, out=np.zeros(len(tp), dtype=float), where=denom != 0).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260928)
    args = ap.parse_args()
    root = args.root.resolve()
    out = args.out or root / "results/reviewer_20260928/m4_generator_stratum"
    out.mkdir(parents=True, exist_ok=True)
    plan = pd.read_csv(root / "data/prompts/paper2_generation_plan_720.csv")
    plan = plan[["case_id", "model_id", "model_checkpoint"]].rename(columns={"case_id": "Case_ID"})
    assert plan.Case_ID.is_unique and len(plan) == 720
    rng = np.random.default_rng(args.seed)
    rows, counts = [], []
    for target in ("T1", "T2", "T3", "T4"):
        pred = pd.read_csv(root / f"data/computational/m4/OOF_M4_FORCED_{target}_C.csv")
        df = pred.merge(plan, on="Case_ID", validate="one_to_one")
        assert len(df) == len(pred) and df.Case_ID.is_unique
        labels = sorted(df.y_true.unique())
        assert set(df.M4_pred.unique()).issubset(set(labels))
        groups = [("all", df), ("exclude_M01", df[df.model_id != "M01"])]
        groups += [(m, df[df.model_id == m]) for m in sorted(df.model_id.unique())]
        for name, part in groups:
            rows.append(dict(target=target, group=name, n=len(part), prompts=part.Prompt_ID.nunique(),
                             macro_f1=score(part, labels), accuracy=float((part.y_true == part.M4_pred).mean())))
            for lab in labels:
                counts.append(dict(target=target, group=name, label=lab,
                                   gold_n=int((part.y_true == lab).sum()), predicted_n=int((part.M4_pred == lab).sum())))
        # Precompute prompt confusion matrices: resampling must retain every
        # eligible generator row for a sampled prompt, including duplicates.
        prompt_ids = df.Prompt_ID.drop_duplicates().tolist()
        index = {pid: i for i, pid in enumerate(prompt_ids)}
        strata = [np.array([index[p] for p in g.Prompt_ID.drop_duplicates()])
                  for _, g in df.groupby("Task_Type", sort=True)]
        names = [name for name, _ in groups]
        cms = np.zeros((len(names), len(prompt_ids), len(labels), len(labels)), dtype=int)
        li = {lab: i for i, lab in enumerate(labels)}
        for row in df.itertuples(index=False):
            p = index[row.Prompt_ID]
            for j, name in enumerate(names):
                if name == "all" or (name == "exclude_M01" and row.model_id != "M01") or name == row.model_id:
                    cms[j, p, li[row.y_true], li[row.M4_pred]] += 1
        boots = {name: [] for name in names}
        for _ in range(args.reps):
            selected = np.concatenate([rng.choice(ids, size=len(ids), replace=True) for ids in strata])
            for j, name in enumerate(names):
                boots[name].append(macro_from_cm(cms[j, selected].sum(axis=0)))
        for row in rows:
            if row["target"] == target:
                row["ci_low"], row["ci_high"] = np.percentile(boots[row["group"]], [2.5, 97.5])
        pair_delta = np.asarray(boots["exclude_M01"]) - np.asarray(boots["all"])
        print(target, "all", score(df, labels), "exclude M01", score(df[df.model_id != "M01"], labels),
              "exclusion delta CI", np.percentile(pair_delta, [2.5, 97.5]))
    pd.DataFrame(rows).to_csv(out / "m4_by_generator.csv", index=False)
    pd.DataFrame(counts).to_csv(out / "m4_generator_class_counts.csv", index=False)
    (out / "manifest.json").write_text(json.dumps(dict(seed=args.seed, bootstrap_replicates=args.reps,
        method="task-stratified Prompt_ID cluster bootstrap over archived Condition-C M4 predictions",
        scope="post-hoc descriptive same-family sensitivity; no causal bias estimate"), indent=2))


if __name__ == "__main__":
    main()
