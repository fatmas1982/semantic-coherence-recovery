#!/usr/bin/env python3
"""P2_81 CPU validity / shortcut diagnostics.

This script reproduces the new CPU analyses added after reviewer-style validity review:
  E1. Anonymous generator-identity recoverability from model outputs.
  E2. Metadata-only target diagnostics (task, anonymous generator, task+generator).
  E3. Dual-blocked M1 sensitivity (hold out BOTH Prompt_ID fold and generator stratum).
  E4. Source-bearing-only B->C reanalysis for frozen M3 and final forced-choice M4 OOF predictions.
  E5. ModernBERT token-length / truncation audit (optional; requires transformers + tokenizer).
  E6. Export of top semantic-similarity pairs for human manual audit.

Scientific boundary:
- Generator strata are anonymous integers (0..5). They are used only as a shortcut/validity diagnostic.
- No checkpoint ranking or model-quality conclusion is produced.
- FINAL GOLD and frozen folds are never modified.
- All uncertainty resampling uses Prompt_ID clusters.

Expected frozen inputs:
  P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx
  P2_CPU_Baselines_v1.0.xlsx

Optional result inputs for E4/E6:
  M3 result directory containing OOF_M3_T{1..4}_{B,C}_seed20260908.csv
  M4 forced-choice result directory containing OOF_M4_FORCED_T{1..4}_{B,C}.csv
  semantic audit files SEMANTIC_AUDIT_TOP100_PROMPT_ONLY.csv and
    SEMANTIC_AUDIT_TOP100_PROMPT_PLUS_SOURCE.csv

Example:
  python P2_81_CPU_VALIDITY_DIAGNOSTICS.py \
      --gold /content/drive/MyDrive/P2/input/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx \
      --base /content/drive/MyDrive/P2/input/P2_CPU_Baselines_v1.0.xlsx \
      --m3-dir /content/drive/MyDrive/P2/results \
      --m4-dir /content/drive/MyDrive/P2/results/M4_FORCED_CHOICE_V2 \
      --out /content/drive/MyDrive/P2/results/P2_81_CPU_DIAGNOSTICS
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import LinearSVC

SEED = 20260908
BOOT_REPS = 2000
EXPECTED_SHA256 = {
    "gold": "ccc910b7bafbfa9607e93ef2eba8605f56f7ed87460ef74892d4877c7db4de65",
    "base": "4502e71bd6d1b6d2941b0b10650caaa433d7188bf958017d2fc646d328a31163",
}
TARGETS = ["T1", "T2", "T3", "T4"]
TARGET_LABELS = {"T1": [0,1], "T2": [0,1], "T3": [0,1], "T4": [1,2,3]}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def serialise(row: pd.Series, condition: str) -> str:
    prompt = "" if pd.isna(row.get("Prompt_Text")) else str(row["Prompt_Text"]).strip()
    source = "" if pd.isna(row.get("Source_Context")) else str(row["Source_Context"]).strip()
    output = "" if pd.isna(row.get("Model_Output")) else str(row["Model_Output"]).strip()
    if condition == "A":
        return output
    if condition == "B":
        return f"Task:\n{prompt}\n\nResponse:\n{output}"
    if condition == "C":
        if str(row.get("Source_Available", "")).lower() == "yes" and source:
            return f"Task:\n{prompt}\n\nAuthorised source/context:\n{source}\n\nResponse:\n{output}"
        return f"Task:\n{prompt}\n\nResponse:\n{output}"
    raise ValueError(condition)


def macro_from_cm(cm: np.ndarray) -> float:
    tp = np.diag(cm).astype(float)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp
    den = 2 * tp + fp + fn
    f = np.divide(2 * tp, den, out=np.zeros_like(tp), where=den != 0)
    return float(f.mean())


def cluster_cms(df: pd.DataFrame, true_col: str, pred_col: str, labels: list[int]) -> np.ndarray:
    idx = {v:i for i,v in enumerate(labels)}
    arr = []
    for _, g in df.assign(_pid=df["Prompt_ID"].astype(str)).groupby("_pid", sort=True):
        cm = np.zeros((len(labels), len(labels)), dtype=np.int64)
        for yt, yp in zip(g[true_col].astype(int), g[pred_col].astype(int)):
            cm[idx[int(yt)], idx[int(yp)]] += 1
        arr.append(cm)
    return np.stack(arr)


def cluster_bootstrap_ci(df: pd.DataFrame, true_col: str, pred_col: str,
                         labels: list[int], reps: int = BOOT_REPS, seed: int = SEED):
    cms = cluster_cms(df, true_col, pred_col, labels)
    rng = np.random.default_rng(seed)
    sampled = rng.choice(len(cms), size=(reps, len(cms)), replace=True)
    vals = np.empty(reps, dtype=float)
    for i in range(reps):
        vals[i] = macro_from_cm(cms[sampled[i]].sum(axis=0))
    return tuple(np.percentile(vals, [2.5, 97.5]))


def paired_cluster_bootstrap_delta(df: pd.DataFrame, true_col: str,
                                   pred_a: str, pred_b: str,
                                   labels: list[int], reps: int = BOOT_REPS,
                                   seed: int = SEED):
    ca = cluster_cms(df, true_col, pred_a, labels)
    cb = cluster_cms(df, true_col, pred_b, labels)
    assert len(ca) == len(cb)
    rng = np.random.default_rng(seed)
    sampled = rng.choice(len(ca), size=(reps, len(ca)), replace=True)
    vals = np.empty(reps, dtype=float)
    for i in range(reps):
        ix = sampled[i]
        vals[i] = macro_from_cm(cb[ix].sum(axis=0)) - macro_from_cm(ca[ix].sum(axis=0))
    return tuple(np.percentile(vals, [2.5, 97.5]))


def derive_working_cases(gold: pd.DataFrame, folds: pd.DataFrame) -> pd.DataFrame:
    """Create anonymous generator strata without exposing checkpoint names.

    The frozen corpus contains exactly six rows per Prompt_ID in a stable within-prompt
    generation order. The stratum is therefore the within-prompt row position 0..5.
    """
    d = gold.copy().reset_index(drop=True)
    counts = d.groupby("Prompt_ID", sort=False).size()
    assert len(counts) == 120 and counts.eq(6).all(), "Expected 120 Prompt_ID groups x 6 outputs."
    d["Generator_Stratum"] = d.groupby("Prompt_ID", sort=False).cumcount().astype(int)
    assert d.groupby("Prompt_ID")["Generator_Stratum"].nunique().eq(6).all()
    d = d.merge(folds[["Prompt_ID", "Fold"]], on="Prompt_ID", how="left", validate="many_to_one")
    assert d["Fold"].notna().all()
    d["Fold"] = d["Fold"].astype(int)
    keep = [
        "Case_ID","Prompt_ID","Task_Type","Source_Available","Prompt_Text","Source_Context",
        "Model_Output","Final_Primary","Final_Family","Final_Boundary","Final_Severity",
        "Any_Failure","Generator_Stratum","Fold"
    ]
    return d[keep]


def fixed_fold_text_oof(texts: pd.Series, y: pd.Series, folds: pd.Series, kind: str) -> np.ndarray:
    pred = np.full(len(y), -1, dtype=int)
    for f in sorted(folds.unique()):
        tr = folds != f
        te = folds == f
        if kind == "word":
            features = TfidfVectorizer(
                ngram_range=(1,2), min_df=2, max_df=.98,
                max_features=40000, sublinear_tf=True
            )
        elif kind == "char":
            features = TfidfVectorizer(
                analyzer="char", ngram_range=(3,5), min_df=2,
                max_features=40000, sublinear_tf=True
            )
        elif kind == "word_char":
            features = FeatureUnion([
                ("word", TfidfVectorizer(
                    ngram_range=(1,2), min_df=2, max_df=.98,
                    max_features=40000, sublinear_tf=True
                )),
                ("char", TfidfVectorizer(
                    analyzer="char", ngram_range=(3,5), min_df=2,
                    max_features=40000, sublinear_tf=True
                )),
            ])
        else:
            raise ValueError(kind)
        Xtr = features.fit_transform(texts.loc[tr])
        Xte = features.transform(texts.loc[te])
        clf = LinearSVC(C=1.0, class_weight="balanced", random_state=SEED)
        clf.fit(Xtr, y.loc[tr])
        pred[te.to_numpy()] = clf.predict(Xte)
    assert np.all(pred >= 0)
    return pred


def run_generator_probe(work: pd.DataFrame, out_dir: Path):
    y = work["Generator_Stratum"].astype(int).reset_index(drop=True)
    texts = work["Model_Output"].fillna("").astype(str).reset_index(drop=True)
    folds = work["Fold"].astype(int).reset_index(drop=True)
    base = work[["Case_ID","Prompt_ID"]].reset_index(drop=True)
    rows = []
    oof_all = []
    for kind in ["word","char","word_char"]:
        pred = fixed_fold_text_oof(texts, y, folds, kind)
        d = base.copy(); d["y_true"] = y; d["pred"] = pred; d["probe"] = kind
        lo, hi = cluster_bootstrap_ci(d, "y_true", "pred", list(range(6)))
        rows.append({
            "probe": kind, "n": len(d),
            "macro_f1": f1_score(y, pred, average="macro"),
            "accuracy": accuracy_score(y, pred),
            "ci_low": lo, "ci_high": hi,
        })
        oof_all.append(d)
    result = pd.DataFrame(rows)
    result.to_csv(out_dir/"P2_81_GENERATOR_IDENTITY_PROBE.csv", index=False)
    pd.concat(oof_all, ignore_index=True).to_csv(out_dir/"P2_81_GENERATOR_IDENTITY_PROBE_OOF.csv", index=False)
    return result


def run_metadata_diagnostics(work: pd.DataFrame, oof: dict[str,pd.DataFrame], out_dir: Path):
    rows = []
    pred_rows = []
    metas = {
        "task_only": ["Task_Type"],
        "generator_only": ["Generator_Stratum"],
        "task_plus_generator": ["Task_Type","Generator_Stratum"],
    }
    lookup = work[["Case_ID","Task_Type","Generator_Stratum"]].copy()
    for target in TARGETS:
        d = oof[target].merge(lookup, on="Case_ID", how="left", validate="one_to_one", suffixes=("","_work"))
        # If Task_Type exists in both, use the frozen OOF value.
        if "Task_Type_work" in d.columns:
            d.drop(columns=["Task_Type_work"], inplace=True)
        for meta, cols in metas.items():
            pred = np.full(len(d), -999, dtype=int)
            for f in sorted(d["Fold"].astype(int).unique()):
                tr = d["Fold"].astype(int) != f
                te = d["Fold"].astype(int) == f
                pipe = Pipeline([
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ("lr", LogisticRegression(
                        class_weight="balanced", max_iter=2000, random_state=SEED
                    )),
                ])
                pipe.fit(d.loc[tr, cols].astype(str), d.loc[tr, "y_true"].astype(int))
                pred[te.to_numpy()] = pipe.predict(d.loc[te, cols].astype(str))
            assert np.all(pred != -999)
            x = d[["Case_ID","Prompt_ID","y_true"]].copy(); x["pred"] = pred
            lo, hi = cluster_bootstrap_ci(x, "y_true", "pred", TARGET_LABELS[target])
            rows.append({
                "target": target, "metadata": meta, "n": len(d),
                "macro_f1": f1_score(d["y_true"], pred, average="macro"),
                "accuracy": accuracy_score(d["y_true"], pred),
                "ci_low": lo, "ci_high": hi,
            })
            x["target"] = target; x["metadata"] = meta; pred_rows.append(x)
    result = pd.DataFrame(rows)
    result.to_csv(out_dir/"P2_81_METADATA_ONLY_TARGET_DIAGNOSTICS.csv", index=False)
    pd.concat(pred_rows, ignore_index=True).to_csv(out_dir/"P2_81_METADATA_ONLY_TARGET_OOF.csv", index=False)
    return result


def run_m1_dual_blocked(work: pd.DataFrame, oof: dict[str,pd.DataFrame], out_dir: Path):
    work2 = work[["Case_ID","Generator_Stratum","Prompt_Text","Source_Context","Source_Available","Model_Output"]].copy()
    work2["text_C"] = work2.apply(lambda r: serialise(r, "C"), axis=1)
    rows = []
    oof_rows = []
    for target in TARGETS:
        d = oof[target].merge(work2[["Case_ID","Generator_Stratum","text_C"]], on="Case_ID", validate="one_to_one")
        dual = np.full(len(d), -999, dtype=int)
        for f in sorted(d["Fold"].astype(int).unique()):
            for g in sorted(d["Generator_Stratum"].astype(int).unique()):
                te = (d["Fold"].astype(int) == f) & (d["Generator_Stratum"].astype(int) == g)
                if not te.any():
                    continue
                tr = (d["Fold"].astype(int) != f) & (d["Generator_Stratum"].astype(int) != g)
                train_labels = set(d.loc[tr, "y_true"].astype(int).unique())
                full_labels = set(d["y_true"].astype(int).unique())
                assert train_labels == full_labels, f"{target}: missing class in fold={f}, generator={g}"
                vec = TfidfVectorizer(
                    ngram_range=(1,2), min_df=2, max_df=.98,
                    max_features=40000, sublinear_tf=True
                )
                Xtr = vec.fit_transform(d.loc[tr, "text_C"])
                Xte = vec.transform(d.loc[te, "text_C"])
                clf = LinearSVC(C=1.0, class_weight="balanced", random_state=SEED)
                clf.fit(Xtr, d.loc[tr, "y_true"].astype(int))
                dual[te.to_numpy()] = clf.predict(Xte)
        assert np.all(dual != -999)
        d["dual_blocked_pred"] = dual
        d["standard_m1_pred"] = d["M1_pred"].astype(int)
        standard = f1_score(d["y_true"], d["standard_m1_pred"], average="macro")
        blocked = f1_score(d["y_true"], d["dual_blocked_pred"], average="macro")
        lo, hi = paired_cluster_bootstrap_delta(
            d, "y_true", "standard_m1_pred", "dual_blocked_pred", TARGET_LABELS[target]
        )
        rows.append({
            "target": target, "n": len(d),
            "standard_m1_macro_f1": standard,
            "dual_blocked_m1_macro_f1": blocked,
            "delta": blocked-standard,
            "ci_low": lo, "ci_high": hi,
        })
        x = d[["Case_ID","Prompt_ID","Task_Type","Fold","Generator_Stratum","y_true","standard_m1_pred","dual_blocked_pred"]].copy()
        x["target"] = target; oof_rows.append(x)
    result = pd.DataFrame(rows)
    result.to_csv(out_dir/"P2_81_M1_DUAL_BLOCKED_SENSITIVITY.csv", index=False)
    pd.concat(oof_rows, ignore_index=True).to_csv(out_dir/"P2_81_M1_DUAL_BLOCKED_OOF.csv", index=False)
    return result


def locate_prediction_file(root: Path, candidates: list[str]) -> Path:
    for c in candidates:
        p = root/c
        if p.exists():
            return p
    # recursive fallback
    for c in candidates:
        hits = list(root.rglob(c))
        if hits:
            return hits[0]
    raise FileNotFoundError(f"None of {candidates} found under {root}")


def run_source_bearing_reanalysis(gold: pd.DataFrame, m3_dir: Path, m4_dir: Path, out_dir: Path):
    source_ids = set(gold.loc[
        gold["Source_Available"].astype(str).str.lower().eq("yes"), "Case_ID"
    ].astype(str))
    rows = []
    for model in ["M3","M4"]:
        for target in TARGETS:
            if model == "M3":
                pb = locate_prediction_file(m3_dir, [f"OOF_M3_{target}_B_seed20260908.csv"])
                pc = locate_prediction_file(m3_dir, [f"OOF_M3_{target}_C_seed20260908.csv"])
                pred_col = "M3_pred"
            else:
                pb = locate_prediction_file(m4_dir, [
                    f"OOF_M4_FORCED_{target}_B.csv", f"OOF_M4_FINALV3_{target}_B.csv"
                ])
                pc = locate_prediction_file(m4_dir, [
                    f"OOF_M4_FORCED_{target}_C.csv", f"OOF_M4_FINALV3_{target}_C.csv"
                ])
                pred_col = "M4_pred"
            B = pd.read_csv(pb)[["Case_ID","Prompt_ID","y_true",pred_col]].rename(columns={pred_col:"pred_B"})
            C = pd.read_csv(pc)[["Case_ID",pred_col]].rename(columns={pred_col:"pred_C"})
            d = B.merge(C, on="Case_ID", validate="one_to_one")
            d = d[d["Case_ID"].astype(str).isin(source_ids)].copy()
            d["pred_B"] = d["pred_B"].astype(int); d["pred_C"] = d["pred_C"].astype(int)
            fB = f1_score(d["y_true"], d["pred_B"], average="macro")
            fC = f1_score(d["y_true"], d["pred_C"], average="macro")
            lo, hi = paired_cluster_bootstrap_delta(d, "y_true", "pred_B", "pred_C", TARGET_LABELS[target])
            rows.append({
                "model": model, "target": target,
                "n_cases": len(d), "n_prompts": d["Prompt_ID"].nunique(),
                "macro_f1_B": fB, "macro_f1_C": fC,
                "delta": fC-fB, "ci_low": lo, "ci_high": hi,
            })
    result = pd.DataFrame(rows)
    result.to_csv(out_dir/"P2_81_SOURCE_BEARING_BC_REANALYSIS.csv", index=False)
    return result


def run_token_audit(gold: pd.DataFrame, out_dir: Path, local_tokenizer_dir: Path|None = None):
    """Reconstruct ModernBERT token counts before the 1024-token truncation step.

    Preferred path: pass a directory containing tokenizer.json/tokenizer_config.json from a
    retained ModernBERT training checkpoint. Otherwise the frozen HF revision is loaded.
    """
    try:
        from transformers import AutoTokenizer, PreTrainedTokenizerFast
    except Exception as e:
        raise RuntimeError("Install transformers/tokenizers to run E5 token audit.") from e

    if local_tokenizer_dir and (local_tokenizer_dir/"tokenizer.json").exists():
        try:
            tok = AutoTokenizer.from_pretrained(str(local_tokenizer_dir), local_files_only=True)
        except Exception:
            tok = PreTrainedTokenizerFast(tokenizer_file=str(local_tokenizer_dir/"tokenizer.json"))
    else:
        tok = AutoTokenizer.from_pretrained(
            "answerdotai/ModernBERT-base",
            revision="c0e44438c79d5a72972fe8b14dbbc822418356c9",
        )

    rows = []
    for _, g in gold.iterrows():
        for cond in ["A","B","C"]:
            text = serialise(g, cond)
            ids = tok(text, add_special_tokens=True, truncation=False)["input_ids"]
            rows.append({
                "Case_ID": g["Case_ID"], "Prompt_ID": g["Prompt_ID"], "Task_Type": g["Task_Type"],
                "condition": cond, "token_count_reconstructed": len(ids),
                "chars": len(text), "whitespace_words": len(text.split()),
                "source_available": str(g["Source_Available"]).lower()=="yes",
            })
    d = pd.DataFrame(rows)
    d.to_csv(out_dir/"P2_81_M3_TOKEN_AUDIT_RECONSTRUCTED.csv", index=False)
    summary = d.groupby("condition")["token_count_reconstructed"].agg(
        count="count", median="median", max="max", p95=lambda x: x.quantile(.95)
    ).reset_index()
    summary["n_over_1024"] = summary["condition"].map(
        d.groupby("condition")["token_count_reconstructed"].apply(lambda x:int((x>1024).sum()))
    )
    summary.to_csv(out_dir/"P2_81_M3_TOKEN_AUDIT_SUMMARY.csv", index=False)
    return d, summary


def export_similarity_candidates(gold: pd.DataFrame, semantic_dir: Path, out_dir: Path):
    prompt_table = gold.drop_duplicates("Prompt_ID").set_index("Prompt_ID", drop=False)
    outputs = []
    specs = [
        ("prompt_only", "SEMANTIC_AUDIT_TOP100_PROMPT_ONLY.csv"),
        ("prompt_plus_source", "SEMANTIC_AUDIT_TOP100_PROMPT_PLUS_SOURCE.csv"),
    ]
    for representation, fname in specs:
        p = locate_prediction_file(semantic_dir, [fname])
        d = pd.read_csv(p).head(25).copy()
        d["representation"] = representation
        def text_for(pid):
            r = prompt_table.loc[str(pid)] if str(pid) in prompt_table.index.astype(str) else None
            if r is None: return ""
            if representation == "prompt_only": return str(r["Prompt_Text"])
            source = str(r["Source_Context"]) if str(r["Source_Available"]).lower()=="yes" else ""
            return str(r["Prompt_Text"]) + (("\n\n"+source) if source else "")
        # Robust lookup without depending on index dtype
        by_pid = {str(r.Prompt_ID):r for _,r in prompt_table.iterrows()}
        d["text_1"] = d["prompt_1"].astype(str).map(lambda x: text_for_pid(by_pid, x, representation))
        d["text_2"] = d["prompt_2"].astype(str).map(lambda x: text_for_pid(by_pid, x, representation))
        d["manual_classification"] = ""
        d["manual_note"] = ""
        outputs.append(d)
    result = pd.concat(outputs, ignore_index=True)
    result.to_csv(out_dir/"P2_81_TOP25_SIMILARITY_MANUAL_AUDIT_TEMPLATE.csv", index=False)
    return result


def text_for_pid(by_pid, pid: str, representation: str):
    r = by_pid[str(pid)]
    prompt = "" if pd.isna(r["Prompt_Text"]) else str(r["Prompt_Text"])
    if representation == "prompt_only":
        return prompt
    source = "" if pd.isna(r["Source_Context"]) else str(r["Source_Context"])
    if str(r["Source_Available"]).lower()=="yes" and source:
        return prompt + "\n\n" + source
    return prompt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", type=Path, required=True)
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--m3-dir", type=Path)
    ap.add_argument("--m4-dir", type=Path)
    ap.add_argument("--semantic-dir", type=Path)
    ap.add_argument("--tokenizer-dir", type=Path)
    ap.add_argument("--run-token-audit", action="store_true")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    observed = {"gold":sha256(args.gold), "base":sha256(args.base)}
    for k,v in observed.items():
        print(k, v)
        assert v == EXPECTED_SHA256[k], f"Frozen {k} hash mismatch"

    gold = pd.read_excel(args.gold, sheet_name="FINAL_GOLD")
    folds = pd.read_excel(args.base, sheet_name="Fold_Assignments")
    oof = {t: pd.read_excel(args.base, sheet_name=f"OOF_{t}") for t in TARGETS}
    assert len(gold)==720 and gold["Case_ID"].nunique()==720 and gold["Prompt_ID"].nunique()==120

    work = derive_working_cases(gold, folds)
    work.to_csv(args.out/"P2_81_WORKING_CASES_ANONYMOUS_GENERATOR.csv", index=False)

    print("\nE1 Generator identity probe")
    print(run_generator_probe(work, args.out).to_string(index=False))

    print("\nE2 Metadata-only target diagnostics")
    print(run_metadata_diagnostics(work, oof, args.out).to_string(index=False))

    print("\nE3 Dual-blocked M1")
    print(run_m1_dual_blocked(work, oof, args.out).to_string(index=False))

    if args.m3_dir and args.m4_dir:
        print("\nE4 Source-bearing-only B->C")
        print(run_source_bearing_reanalysis(gold, args.m3_dir, args.m4_dir, args.out).to_string(index=False))
    else:
        print("\nE4 skipped: provide --m3-dir and --m4-dir")

    if args.run_token_audit:
        print("\nE5 ModernBERT token audit")
        _, s = run_token_audit(gold, args.out, args.tokenizer_dir)
        print(s.to_string(index=False))
    else:
        print("\nE5 skipped: add --run-token-audit (and optionally --tokenizer-dir)")

    if args.semantic_dir:
        print("\nE6 Export top-25 similarity pairs for HUMAN manual audit")
        d = export_similarity_candidates(gold, args.semantic_dir, args.out)
        print("Wrote", len(d), "rows. Manual classification must be performed by a human/reviewer; do not auto-label it.")
    else:
        print("\nE6 skipped: provide --semantic-dir")

    manifest = {
        "protocol":"P2_81_CPU_VALIDITY_DIAGNOSTICS_v1.0",
        "seed":SEED,"bootstrap_replicates":BOOT_REPS,
        "gold_sha256":observed["gold"],"base_sha256":observed["base"],
        "generator_identity_is_anonymous":True,
        "manual_similarity_audit_is_human":True,
    }
    (args.out/"P2_81_CPU_DIAGNOSTICS_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()