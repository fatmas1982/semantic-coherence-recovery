#!/usr/bin/env python3
"""Reproduce the computational-semantics structure diagnostics for the IP&M manuscript.

This script uses FINAL GOLD v1.0 only. It does not change labels or retrain models.

Analyses:
1. T3 family (Core SCF vs OVR) x final grounding status.
2. Task type x final mechanism family (Core SCF, OVR, HREF, NONE).

Association is summarised descriptively with Cramer's V:
    V = sqrt(chi2 / (N * min(r - 1, c - 1)))

95% intervals for V use 2,000 task-stratified Prompt_ID-cluster bootstrap
resamples (seed 20260919), preserving all six checkpoint outputs belonging
to each sampled prompt. No p-values are reported because the prompt bank
and corpus were purposively constructed.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

BOOT_REPS = 2000
SEED = 20260919
FAMILY_ORDER = ["Core SCF", "OVR", "HREF", "NONE"]
GROUNDING_ORDER = ["semantic_only", "overlap"]

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--gold", type=Path, default=Path("data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx"))
    p.add_argument("--out-dir", type=Path, default=Path("results/followup"))
    p.add_argument("--bootstrap-reps", type=int, default=BOOT_REPS)
    p.add_argument("--seed", type=int, default=SEED)
    return p.parse_args()

def cramers_v(table):
    a = np.asarray(table, dtype=float)
    n = a.sum()
    if n <= 0 or min(a.shape) <= 1:
        return np.nan, np.nan
    chi2 = chi2_contingency(a, correction=False)[0]
    v = math.sqrt(chi2 / (n * min(a.shape[0] - 1, a.shape[1] - 1)))
    return float(v), float(chi2)

def main():
    a = parse_args()
    gold = pd.read_excel(a.gold, sheet_name="FINAL_GOLD")
    tasks = sorted(gold["Task_Type"].unique())

    t3 = gold[gold["Final_Family"].isin(["Core SCF", "OVR"])].copy()
    ct_fg = pd.crosstab(t3["Final_Family"], t3["Final_Boundary"]).reindex(
        index=["Core SCF", "OVR"], columns=GROUNDING_ORDER, fill_value=0
    )
    v_fg, chi2_fg = cramers_v(ct_fg.values)

    fg_rows = []
    for fam in ["Core SCF", "OVR"]:
        total = int(ct_fg.loc[fam].sum())
        for boundary in GROUNDING_ORDER:
            n = int(ct_fg.loc[fam, boundary])
            fg_rows.append({
                "family": fam, "grounding_status": boundary, "n": n,
                "row_total": total, "row_pct": 100.0 * n / total
            })
    fg = pd.DataFrame(fg_rows)

    ct_tf = pd.crosstab(gold["Task_Type"], gold["Final_Family"]).reindex(
        index=tasks, columns=FAMILY_ORDER, fill_value=0
    )
    v_tf, chi2_tf = cramers_v(ct_tf.values)

    tf_rows = []
    for task in tasks:
        total = int(ct_tf.loc[task].sum())
        for fam in FAMILY_ORDER:
            n = int(ct_tf.loc[task, fam])
            tf_rows.append({
                "task": task, "family": fam, "n": n,
                "row_total": total, "row_pct": 100.0 * n / total
            })
    tf = pd.DataFrame(tf_rows)

    rng = np.random.default_rng(a.seed)
    prompt_by_task = {
        t: np.asarray(sorted(gold.loc[gold["Task_Type"].eq(t), "Prompt_ID"].unique()), dtype=object)
        for t in tasks
    }
    lookup = {
        (t, p): gold.index[(gold["Task_Type"].eq(t)) & (gold["Prompt_ID"].eq(p))].to_numpy()
        for t in tasks for p in prompt_by_task[t]
    }

    v_fg_boot, v_tf_boot = [], []
    for _ in range(a.bootstrap_reps):
        chunks = []
        for t in tasks:
            prompts = prompt_by_task[t]
            sampled = rng.choice(prompts, size=len(prompts), replace=True)
            chunks.extend(lookup[(t, p)] for p in sampled)
        idx = np.concatenate(chunks)
        d = gold.loc[idx]

        d_t3 = d[d["Final_Family"].isin(["Core SCF", "OVR"])]
        c1 = pd.crosstab(d_t3["Final_Family"], d_t3["Final_Boundary"]).reindex(
            index=["Core SCF", "OVR"], columns=GROUNDING_ORDER, fill_value=0
        )
        v_fg_boot.append(cramers_v(c1.values)[0])

        c2 = pd.crosstab(d["Task_Type"], d["Final_Family"]).reindex(
            index=tasks, columns=FAMILY_ORDER, fill_value=0
        )
        v_tf_boot.append(cramers_v(c2.values)[0])

    fg_ci = np.quantile(v_fg_boot, [0.025, 0.975])
    tf_ci = np.quantile(v_tf_boot, [0.025, 0.975])

    summary = pd.DataFrame([
        {
            "analysis": "T3 family x grounding status",
            "N_rows": len(t3),
            "N_prompt_clusters": t3["Prompt_ID"].nunique(),
            "rows": ct_fg.shape[0], "columns": ct_fg.shape[1],
            "chi_square_descriptive": chi2_fg, "cramers_v": v_fg,
            "bootstrap_ci_low": fg_ci[0], "bootstrap_ci_high": fg_ci[1],
            "bootstrap_reps": a.bootstrap_reps, "bootstrap_seed": a.seed,
            "inference_note": "Descriptive association; no p-value is used because the corpus is purposively constructed."
        },
        {
            "analysis": "Task x mechanism family",
            "N_rows": len(gold),
            "N_prompt_clusters": gold["Prompt_ID"].nunique(),
            "rows": ct_tf.shape[0], "columns": ct_tf.shape[1],
            "chi_square_descriptive": chi2_tf, "cramers_v": v_tf,
            "bootstrap_ci_low": tf_ci[0], "bootstrap_ci_high": tf_ci[1],
            "bootstrap_reps": a.bootstrap_reps, "bootstrap_seed": a.seed,
            "inference_note": "Descriptive association; no p-value is used because task allocation and the corpus are purposively constructed."
        },
    ])

    a.out_dir.mkdir(parents=True, exist_ok=True)
    fg.to_csv(a.out_dir / "P2_IPM_T3_FAMILY_BY_GROUNDING_CROSSTAB.csv", index=False, float_format="%.6f")
    tf.to_csv(a.out_dir / "P2_IPM_TASK_BY_MECHANISM_FAMILY_CROSSTAB.csv", index=False, float_format="%.6f")
    summary.to_csv(a.out_dir / "P2_IPM_COMPUTATIONAL_SEMANTICS_ASSOCIATION_SUMMARY.csv", index=False, float_format="%.9f")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
