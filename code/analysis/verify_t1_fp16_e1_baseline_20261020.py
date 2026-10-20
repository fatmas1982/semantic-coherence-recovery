#!/usr/bin/env python3
"""Reconcile archived T1 FP16 reference vs E1/rot0 predictions from main-line CSVs.

Run from repo root:
  python code/analysis/verify_t1_fp16_e1_baseline_20261020.py

This reads archived predictions; it does NOT rerun tokenizers, reconstruct
2,880 historical prompt hashes, or causally attribute changes to a newline.
"""
import csv,json,math
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
PAIRED=ROOT/"data/validity_2026_10"
SRV=ROOT/"results/server_runs/SERVER_RUN_20261007_A/GPU/M4_NEW"
JUDGES={
"qwen_fp16_offload": dict(changed=4,fp16=.7679227037948411,e1=.7707529147241724),
"mistral_fp16_offload": dict(changed=9,fp16=.4440087005037559,e1=.4276082638141963),
}
def csvrows(path):
 with path.open(encoding="utf-8-sig",newline="") as f:
  yield from csv.DictReader(f)
def macro_f1(rows):
 classes=[0,1]
 ret=[]
 for cls in classes:
  tp=sum(x["gold"]==cls and x["pred"]==cls for x in rows)
  fp=sum(x["gold"]!=cls and x["pred"]==cls for x in rows)
  fn=sum(x["gold"]==cls and x["pred"]!=cls for x in rows)
  ret.append(2*tp/(2*tp+fp+fn) if tp else 0.)
 return sum(ret)/len(ret)
reference=defaultdict(dict)
for path in sorted(PAIRED.glob("paired_cases_part_*.csv")):
 for row in csvrows(path):
  if row["target"]!="T1" or row["experiment"]!="E1" or row["variant"]!="rot1" or row["judge"] not in JUDGES:continue
  j=row["judge"];case=row["case_id"]
  assert case not in reference[j],f"Duplicate E1 case: {j} {case}"
  reference[j][case]=dict(gold=int(row["gold_label"]),pred=int(row["pred_base"]),prompt=row["prompt_id"])
assert len(reference)==2
findings=[]
for judge,expected in JUDGES.items():
 path=SRV/judge/f"OOF_{judge}_T1_C.csv"
 fp16={}
 for row in csvrows(path):
  case=row["Case_ID"]
  assert case not in fp16,f"Duplicate FP16 case {judge}:{case}"
  fp16[case]=dict(gold=int(row["y_true"]),pred=int(row["pred"]),prompt=row["Prompt_ID"])
 old=reference[judge]
 assert len(old)==len(fp16)==720
 assert set(old)==set(fp16),f"Case universe mismatch for {judge}"
 for case,ref in old.items():
  assert ref["gold"]==fp16[case]["gold"],f"Gold mismatch {case}"
  assert ref["prompt"]==fp16[case]["prompt"],f"Prompt mismatch {case}"
 changed=sorted(case for case in old if old[case]["pred"]!=fp16[case]["pred"])
 ref_f1=macro_f1(list(fp16.values()));e1_f1=macro_f1(list(old.values()))
 assert len(changed)==expected["changed"],f"Unexpected changed count {judge}"
 assert math.isclose(ref_f1,expected["fp16"],abs_tol=1e-12,rel_tol=0),(judge,"FP16",ref_f1)
 assert math.isclose(e1_f1,expected["e1"],abs_tol=1e-12,rel_tol=0),(judge,"E1",e1_f1)
 findings.append(dict(judge=judge,case_universe=720,changed_n=len(changed),changed_case_ids=changed,fp16_macro_f1=ref_f1,e1_rot0_macro_f1=e1_f1,case_and_gold_match=True))
print(json.dumps({"status":"PASS_ARCHIVED_DECISION_AND_MACROF1_RECALCULATION","checks":findings,
"NOT_RETESTED":["historical 2,880 SHA reconstructions","tokenizer-level length differences","GPU inference rerun","causal contribution of newline"]},indent=2))
