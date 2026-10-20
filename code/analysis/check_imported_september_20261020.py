#!/usr/bin/env python3
"""Validate imported Sept 2026 reviewer evidence *internal contracts only*.

It does not rerun the original 2,000-replicate bootstraps or source-model
training and MUST NOT be interpreted as complete manuscript table validation.
Run from the repo root: python code/analysis/check_imported_september_20261020.py
"""
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"results"/"followup"
def rows(name):
 with (BASE/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def near(a,b,tol=1e-9):return math.isfinite(float(a)) and math.isfinite(float(b)) and abs(float(a)-float(b))<=tol
summary={"scope":"archived file structure, arithmetic and case coverage only; no bootstrap redraws or historical training",
         "checks":{},"historical_release_note":"R14 2026-09-20 has 16 main tables; the 2026-10-20 main has 20 and must not be called R14-certified"}
boot=rows("P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SENSITIVITY.csv")
assert len(boot)==49, len(boot)
assert all(near(x["max_endpoint_shift"],max(abs(float(x["unstratified_low"])-float(x["task_stratified_low"])),abs(float(x["unstratified_high"])-float(x["task_stratified_high"])))) for x in boot)
assert all(x["zero_inclusion_changed"].strip().lower()=="false" for x in boot)
maxshift=max(float(x["max_endpoint_shift"]) for x in boot)
summary["checks"]["task_stratified_bootstrap_summary"]={"rows":len(boot),"max_endpoint_shift":maxshift,"zero_inclusion_status_changed":0,"status":"PASS_ARCHIVED_ARITHMETIC"}
fold=rows("P2_IPM_FOLD_BY_CLASS_AUDIT.csv")
exp={"T1":720,"T2":474,"T3":460,"T4":474}
assert len(fold)==20
assert min(int(r["min_class_n"]) for r in fold)==11
for task,n in exp.items():
 r=[x for x in fold if x["target"]==task]
 assert len(r)==5 and {int(x["fold"]) for x in r}==set(range(5))
 assert sum(int(x["rows"]) for x in r)==n
 assert sum(int(x["prompt_clusters"]) for x in r)==120
 for x in r:
  assert int(x["prompt_clusters"])==24
  valid=[int(x[k]) for k in ["class_0_n","class_1_n","class_2_n","class_3_n"] if x[k].strip()]
  assert sum(valid)==int(x["rows"])
  assert min(valid)==int(x["min_class_n"])
summary["checks"]["outer_fold_class_support"]={"rows":len(fold),"min_class_count":11,"cases_by_target":exp,"status":"PASS_ARCHIVED_COUNTS"}
pairs=rows("P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv")
assert len(pairs)==12 and len({(x["dimension"],x["pair"]) for x in pairs})==12
assert {x["pair"] for x in pairs}=={"A1-A2","A1-A3","A2-A3"}
assert all(int(x["N_cases"])==720 and int(x["N_prompt_clusters"])==120 for x in pairs)
summary["checks"]["pair_specific_reliability_summary"]={"rows":len(pairs),"status":"PASS_ARCHIVED_DIMENSIONS"}
ex=rows("P2_IPM_ADJUDICATION_INSTABILITY_EXCLUSION_SENSITIVITY.csv")
assert len(ex)==8 and {(x["target"],x["model"]) for x in ex}=={(t,m) for t in exp for m in ("M3","M4")}
for x in ex:
 assert int(x["n_full"])-int(x["n_retained"])==int(x["n_removed"])
 assert near(float(x["exclusion_macro_f1"])-float(x["full_macro_f1"]),x["delta"])
summary["checks"]["adjudication_instability_exclusion_summary"]={"rows":len(ex),"status":"PASS_ARCHIVED_ARITHMETIC"}
amb=rows("P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.csv")
assert len(amb)==11
assert any(x["N"]=="684" for x in amb) and any(x["N"]=="36" for x in amb)
summary["checks"]["ambiguity_exclusion_summary"]={"rows":len(amb),"status":"PASS_ARCHIVED_COVERAGE"}
err=rows("P2_IPM_R14_DETERMINISTIC_ERROR_AUDIT.csv")
assert len(err)==8
assert {(x["target"],x["human_stratum"]) for x in err}=={(t,s) for t in exp for s in ("easy","hard")}
summary["checks"]["deterministic_case_selection_export"]={"rows":len(err),"status":"PASS_ARCHIVED_STRUCTURE"}
sem=rows("P2_IPM_COMPUTATIONAL_SEMANTICS_ASSOCIATION_SUMMARY.csv")
assert len(sem)==2 and {int(x["N_rows"]) for x in sem}=={460,720}
summary["checks"]["semantic_structure_association_export"]={"rows":2,"status":"PASS_ARCHIVED_STRUCTURE"}
summary["status"]="PASS_IMPORTED_ARCHIVE_CONTRACTS_ONLY"
print(json.dumps(summary,indent=2,ensure_ascii=False))
