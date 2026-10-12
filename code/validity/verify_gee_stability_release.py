#!/usr/bin/env python3
"""Regression gate for the frozen, post-hoc GEE precision audit.

Tests all 60 uniquely keyed fits against the repository's immutable published
diagnostic rows. Float comparisons use absolute tolerance because result CSV
formatting and numerical BLAS details may vary in the final decimal.
"""
from pathlib import Path
from collections import Counter
import csv
import math
import sys

ROOT=Path(__file__).resolve().parents[2]
ARCHIVE=ROOT/"results/validity_2026_10/HJI_GEE_STABILITY_60.csv"
RECOMPUTED=ROOT/"results/validity_2026_10/HJI_GEE_STABILITY_60_RECOMPUTED.csv"
DATADIR=ROOT/"data/validity_2026_10"
KEYS=("judge","target","experiment","variant","human_axis")
EXACT=("n_cases","prompt_clusters","total_changed","disagree_n","disagree_changed",
       "agree_n","agree_changed","converged","low_event_flag")
NUMERIC=("event_rate","robust_GEE_SE","gee_adjusted_OR","OR_Wald95_low",
         "OR_Wald95_high","gee_p_unadjusted")

def load(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def get_key(row):
    return tuple(row[x] for x in KEYS)
def norm(x):
    return str(x).strip().lower()

a,b=load(ARCHIVE),load(RECOMPUTED)
assert len(a)==len(b)==60,(len(a),len(b))
aidx={get_key(x):x for x in a}
bidx={get_key(x):x for x in b}
assert len(aidx)==len(bidx)==60
assert aidx.keys()==bidx.keys(),(aidx.keys()-bidx.keys(),bidx.keys()-aidx.keys())
for k in aidx:
    old,new=aidx[k],bidx[k]
    for f in EXACT:
        assert norm(old[f])==norm(new[f]),(k,f,old[f],new[f])
    for f in NUMERIC:
        x,y=float(old[f]),float(new[f])
        assert math.isfinite(x) and math.isfinite(y) and math.isclose(x,y,rel_tol=1e-7,abs_tol=1e-8),(k,f,x,y)
parts=sorted(DATADIR.glob("paired_cases_part_*.csv"))
assert len(parts)==11,len(parts)
case_rows=[r for p in parts for r in load(p)]
assert len(case_rows)==10408,len(case_rows)
assert len({(x["judge"],x["target"],x["experiment"],x["variant"],x["case_id"]) for x in case_rows})==10408
groups=Counter((x["judge"],x["target"],x["experiment"],x["variant"]) for x in case_rows)
assert len(groups)==20
low=[x for x in b if norm(x["low_event_flag"])=="true"]
assert len(low)==3
assert {(r["judge"],r["target"],r["experiment"],r["variant"],int(r["total_changed"])) for r in low}=={
 ("qwen_fp16_offload","T1","E2","rot1",15)}
print("PASS: 60/60 refitted GEE rows; all coefficients, SEs and Wald CIs within tolerance")
print("PASS: 10408 paired case rows; 20 comparisons; 11 parts; 3 low-event flags from one Qwen contrast")
