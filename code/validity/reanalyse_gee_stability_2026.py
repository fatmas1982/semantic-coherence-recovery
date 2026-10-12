#!/usr/bin/env python3
"""Post-hoc GEE stability audit of archived E1/E2 paired decisions.

Same 60 working-independence binomial GEE fits as the published exploratory
human–judge analysis; adds changed-event support, robust log-OR SE and nominal
Wald OR CIs. Does not generate model predictions or add hypothesis tests.
"""
from __future__ import annotations
import argparse, csv, math
from collections import defaultdict
from pathlib import Path
import numpy as np
import statsmodels.api as sm

KEYS = ("judge", "target", "experiment", "variant")
AXES = {"primary": "primary_disagree", "boundary": "boundary_disagree",
        "severity": "severity_disagree"}

def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def audit(data_dir, output):
    data_dir = Path(data_dir)
    pieces = sorted(data_dir.glob("paired_cases_part_*.csv"))
    if len(pieces) != 11:
        raise ValueError(f"Expected 11 paired-case parts, found {len(pieces)}")
    cases = [r for path in pieces for r in read_csv(path)]
    if len(cases) != 10408:
        raise ValueError(f"Expected 10408 paired case rows; got {len(cases)}")
    reference = read_csv(data_dir / "HJI_60_CORRECTED_CI_SEED_20261010.csv")
    ref = {tuple(r[k] for k in (*KEYS, "human_axis")): r for r in reference}
    if len(ref) != 60 or len(reference) != 60:
        raise AssertionError("Reference must include 60 distinct HJI fits")
    groups = defaultdict(list)
    for row in cases:
        groups[tuple(row[k] for k in KEYS)].append(row)
    if len(groups) != 20:
        raise AssertionError(f"Expected 20 paired groups, got {len(groups)}")
    output_rows = []
    for key, rows in sorted(groups.items()):
        labels = sorted({r["gold_label"] for r in rows})
        slots = sorted({r["generator_id"] for r in rows}, key=int)
        y = np.asarray([int(r["changed"]) for r in rows], dtype=float)
        prompt = np.asarray([r["prompt_id"] for r in rows])
        events = int(y.sum())
        for axis, column in AXES.items():
            D = np.asarray([int(r[column]) for r in rows], dtype=float)
            predictors = [np.ones(len(rows)), D]
            predictors.extend(np.asarray([float(r["gold_label"] == c) for r in rows])
                              for c in labels[1:])
            predictors.extend(np.asarray([float(r["generator_id"] == g) for r in rows])
                              for g in slots[1:])
            X = np.column_stack(predictors)
            model = sm.GEE(y, X, groups=prompt, family=sm.families.Binomial(),
                           cov_struct=sm.cov_struct.Independence()).fit(maxiter=150)
            beta = float(model.params[1])
            se = float(model.bse[1])
            p = float(model.pvalues[1])
            odds = math.exp(beta)
            ref_row = ref[(*key, axis)]
            if abs(odds - float(ref_row["gee_adjusted_OR"])) >= 1e-6:
                raise AssertionError((key, axis, "odds ratio differs"))
            if abs(p - float(ref_row["gee_p_unadjusted"])) >= 1e-6:
                raise AssertionError((key, axis, "p-value differs"))
            result = dict(zip(KEYS, key))
            result.update(human_axis=axis, n_cases=len(rows),
                prompt_clusters=len(set(prompt)), total_changed=events,
                event_rate=events/len(rows),
                disagree_n=int(D.sum()), disagree_changed=int((y*D).sum()),
                agree_n=int(len(rows)-D.sum()),
                agree_changed=int((y*(1-D)).sum()),
                robust_GEE_SE=se, gee_adjusted_OR=odds,
                OR_Wald95_low=math.exp(beta-1.96*se),
                OR_Wald95_high=math.exp(beta+1.96*se),
                gee_p_unadjusted=p, converged=bool(model.converged),
                low_event_flag=events<30,
                estimand="Conditional GOLD-class + generator-slot adjusted association; robust Prompt_ID GEE")
            output_rows.append(result)
    output_rows.sort(key=lambda x: tuple(str(x[k]) for k in (*KEYS, "human_axis")))
    if len(output_rows) != 60:
        raise AssertionError(f"Expected 60 fits, got {len(output_rows)}")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"PASS: 60 fitted GEE contrasts; minimum events={min(r['total_changed'] for r in output_rows)}; "
          f"low-event rows={sum(r['low_event_flag'] for r in output_rows)}; saved={output}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path,
                        default=root/"data/validity_2026_10")
    parser.add_argument("--out", type=Path,
                        default=root/"results/validity_2026_10/HJI_GEE_STABILITY_60_RECOMPUTED.csv")
    opts = parser.parse_args()
    audit(opts.data_dir, opts.out)
