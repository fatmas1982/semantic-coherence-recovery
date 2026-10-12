#!/usr/bin/env python3
"""Clean-run check of the reconciled, archived M3 dual-blocked case predictions.

This tests result reproduction conditional on saved predictions, NOT fresh
ModernBERT retraining or independence of the size-matched subsets.
"""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
from sklearn.metrics import f1_score
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/"results/validity/m3_dual_block"
rows=list(csv.DictReader((P/"P2_81_M3_DUAL_BLOCKED_OOF_ALL.csv").open()))
s=list(csv.DictReader((P/"P2_81_M3_DUAL_BLOCKED_SUMMARY.csv").open()))
expected={"T1":720,"T2":474,"T3":460,"T4":474}
assert len(rows)==sum(expected.values())==2128
assert len(s)==4
assert len({(x["task"],x["Case_ID"]) for x in rows})==2128
for x in s:
    t=x["task"]
    assert t in expected
    subset=[r for r in rows if r["task"]==t]
    assert len(subset)==expected[t]
    assert len({r["Prompt_ID"] for r in subset})==120
    assert set(r["generator_stratum"] for r in subset)==set("012345")
    assert len({r["Case_ID"] for r in subset})==expected[t]
    assert all(r["input_zip"]==f"experiments/M3_{t}_dual_r0_C.zip" for r in subset)
    f1=f1_score([int(r["y_true"]) for r in subset],[int(r["prediction"]) for r in subset],average="macro",zero_division=0)
    assert abs(f1-float(x["dual_macro_f1"]))<1e-10,(t,f1,x["dual_macro_f1"])
    assert x["status"]=="VERIFIED_FROM_FROZEN_CASE_PREDICTIONS_20261012"
    print("PASS",t,"n",len(subset),"prompts",120,"macro-F1",format(f1,".12f"))
print("PASS: 2128 OOF predictions, 4 targets; no generative model inference or training")
