#!/usr/bin/env python3
"""Recompute four archived M3 dual-block OOF macro-F1 scores without retraining.
Run from repository root: python code/analysis/verify_m3_dual_oof_20261020.py
Reads original case-level file and previously published task summary. Stdlib only.
"""
import csv,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):
 with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
cases=read(ROOT/"results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_OOF_ALL.csv")
summary={r["task"]:r for r in read(ROOT/"results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_SUMMARY.csv")}
exp={"T1":720,"T2":474,"T3":460,"T4":474}
out=ROOT/"results/validity_2026_10/M3_DUAL_OOF_RECOMPUTED_ON_LOCAL_RUN.csv"
out.parent.mkdir(exist_ok=True,parents=True)
rows=[]
for task,n in exp.items():
 v=[r for r in cases if r["task"]==task]
 ids={x["Case_ID"] for x in v}
 folds={}
 for x in v:folds.setdefault(x["Prompt_ID"],set()).add(x["fold"])
 overlap=sum(len(z)>1 for z in folds.values())
 classes=sorted({x["y_true"] for x in v}|{x["prediction"] for x in v})
 f1=[]
 for cl in classes:
  tp=sum(x["y_true"]==cl and x["prediction"]==cl for x in v)
  fp=sum(x["y_true"]!=cl and x["prediction"]==cl for x in v)
  fn=sum(x["y_true"]==cl and x["prediction"]!=cl for x in v)
  f1.append(2*tp/(2*tp+fp+fn) if tp else 0)
 score=sum(f1)/len(f1)
 published=float(summary[task]["dual_macro_f1"])
 status="PASS_OOF_ONLY" if len(v)==n==len(ids) and overlap==0 and len(folds)==120 and math.isclose(score,published,abs_tol=1e-12,rel_tol=0) else "FAIL"
 rows.append(dict(target=task,n=len(v),unique_case_ids=len(ids),prompt_clusters=len(folds),cross_fold_prompt_overlap=overlap,macro_f1_recomputed=score,macro_f1_published=published,absolute_difference=abs(score-published),status=status))
with out.open("w",encoding="utf-8",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for row in rows:print(row)
if any(row["status"]!="PASS_OOF_ONLY" for row in rows):raise SystemExit(1)
print("PASS OOF-only; does NOT verify inner CV training separation, dynamic leakage, historical retraining or uncertainty.")
