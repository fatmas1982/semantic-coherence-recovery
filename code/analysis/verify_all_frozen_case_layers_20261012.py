#!/usr/bin/env python3
"""Validate case-level linkage across historical human labels and M0–M4 OOF.

No training, generation, adjudication or new analysis is performed.
Only archival structure, target eligibility and frozen prediction completeness
are checked. Never print prompts, human notes or source text.
"""
from pathlib import Path
from collections import Counter,defaultdict
import csv
ROOT=Path(__file__).resolve().parents[2]
COUNTS={"T1":720,"T2":474,"T3":460,"T4":474}
def rows(path):
    with (ROOT/path).open(newline="",encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))
def unique(items,key):
    values=[r[key] for r in items]
    assert len(values)==len(set(values)),(key,"duplicates")
    return set(values)
gold=rows("data/publication/canonical_publication_dataset_720.csv")
raw=rows("data/raw/generated_outputs_720.csv")
assert len(gold)==len(raw)==720
gold_id=unique(gold,"Case_ID")
assert gold_id==unique(raw,"case_id")
assert len({r["Prompt_ID"] for r in gold})==120
assert all(n==6 for n in Counter(r["Prompt_ID"] for r in gold).values())
print("PASS: 720 frozen raw generations and publication cases agree; 120 clusters of 6")
for a in ["A1","A2","A3"]:
    ar=rows(f"data/annotation/historical_full_csv/{a}/Annotation.csv")
    assert len(ar)==720 and unique(ar,"case_id")==gold_id,a
print("PASS: three complete historical annotator sheets (720 decisions each)")
locked=rows("data/annotation/locked_core_ratings/locked_pre_resolution_core_ratings_long_2160.csv")
assert len(locked)==2160
assert set(r["case_id"] for r in locked)==gold_id
counts=Counter(r["case_id"] for r in locked)
assert all(n==3 for n in counts.values()) and len(counts)==720
print("PASS: frozen 2160 pre-resolution ratings, exactly three per case")
for target,n in COUNTS.items():
    base=rows(f"data/frozen/baseline_csv_mirror/{10+list(COUNTS).index(target):02d}_OOF_{target}.csv")
    expect=unique(base,"Case_ID")
    assert len(expect)==n and expect.issubset(gold_id)
    folds={r["Fold"] for r in base}
    assert len(folds)==5, (target,"folds",folds)
    def check(path,label,pred):
        dat=rows(path)
        assert len(dat)==n and unique(dat,"Case_ID")==expect,(label,target)
        assert all(r[pred] not in ("","NaN","nan") for r in dat), (label,target)
        assert {r["Case_ID"]:r["y_true"] for r in dat}=={r["Case_ID"]:r["y_true"] for r in base},(target,label,"GOLD conflict")
    for cond in "ABC":
        check(f"data/computational/m3/OOF_M3_{target}_{cond}_seed20260908.csv","M3_"+cond,"M3_pred")
        check(f"data/computational/m4/OOF_M4_FORCED_{target}_{cond}.csv","M4_"+cond,"M4_pred")
    for seed in ("20260909","20260910"):
        check(f"data/computational/m3/OOF_M3_{target}_C_seed{seed}.csv","M3_seed_"+seed,"M3_pred")
    print("PASS:",target,"cases",n,"M0-M2 + M3(5) + M4(3), same GOLD and no missing predictions")
print("PASS: all 4 frozen target case layers valid, including 20 M3 and 12 M4 archived OOF files")
