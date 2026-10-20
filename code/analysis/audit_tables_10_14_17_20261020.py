#!/usr/bin/env python3
"""Reproduce bounded 60-cell Table 10/14/17 archive-to-manuscript display check.
Run in a complete checkout:
 python code/analysis/audit_tables_10_14_17_20261020.py --out /tmp/p2-tables-audit
Optional --main-docx checks that the supplied Word file is the reviewed source revision.
This audit DOES NOT refit models, rebootstrap confidence intervals, or certify 100 tables.
"""
import argparse,csv,hashlib,json,math,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXPECTED_DOC_SHAS={"572d8d80f33c177650747515fafd678202571a44e95b273985d6a45a7d620389","c3bb4d3e021cf78cc8980b821a8bf59bd69d6e844c9ba3074b63930339d0fa28"}
p=argparse.ArgumentParser();p.add_argument("--main-docx",type=Path);p.add_argument("--out",type=Path,default=Path("p2_table_audit"))
args=p.parse_args()
if args.main_docx:
 h=hashlib.sha256(args.main_docx.read_bytes()).hexdigest()
 if h not in EXPECTED_DOC_SHAS: raise SystemExit("Different Word revision: reviewed expected numbers may have changed")
args.out.mkdir(parents=True,exist_ok=True)
def load(rel):
 with (ROOT/rel).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def sha(rel):
 h=hashlib.sha256()
 with (ROOT/rel).open("rb") as f:
  for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
 return h.hexdigest()
ledger=[]
def check(table,model,target,metric,printed,archive,source):
 ok=math.isfinite(archive) and abs(printed-archive)<=0.00050000001
 ledger.append(dict(table=table,model=model,target=target,metric=metric,paper_display=printed,archived_value=archive,absolute_difference=abs(printed-archive),status="PASS_DISPLAY_PRECISION" if ok else "FAIL_DISPLAY_PRECISION",source_path=source,source_sha256=sha(source)))
tgs=["T1","T2","T3","T4"]
path="PUBLIC_METRICS_RECOMPUTED.csv"
r={(x["model"],x["target"]):x for x in load(path)}
for model,vals in [("M3_C",[.655,.777,.791,.637]),("M4_C",[.741,.609,.530,.391])]:
 for target,printed in zip(tgs,vals):
  check("Table 10",model,target,"macro_f1",printed,float(r[model,target]["macro_f1"]),path)
for model,printed in [("M3_C",.597),("M4_C",.401)]:
 check("Table 10",model,"T4","qwk",printed,float(r[model,"T4"]["qwk"]),path)
cpu_path="results/server_runs/SERVER_RUN_20261007_A/EXPORTS/CPU_summary/ALL_METRICS.csv"
m3_path="results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_SUMMARY.csv"
cpu=load(cpu_path);m3={x["task"]:x for x in load(m3_path)}
printed14={"T1":[.559,.601,.008,.591,.630,.021],"T2":[.593,.646,.016,.671,.749,.014],"T3":[.519,.675,.015,.682,.781,.006],"T4":[.380,.518,.019,.573,.644,.014]}
for target in tgs:
 base=[x for x in cpu if x["group"]=="all" and x["experiment"].startswith("M1_"+target+"_")]
 dual=next(x for x in base if x["experiment"]=="M1_"+target+"_dual_r0_C")
 matched=[float(x["macro_f1"]) for x in base if "size_matched_r" in x["experiment"]]
 if len(matched)!=5:raise SystemExit("Expected five M1 size-matched repeats: "+target)
 values=[float(dual["macro_f1"]),statistics.mean(matched),statistics.stdev(matched),float(m3[target]["dual_macro_f1"]),float(m3[target]["matched_mean_macro_f1"]),float(m3[target]["matched_sample_sd"])]
 metrics=["dual","size_matched_mean","size_matched_sample_sd"]
 for i in range(6):
  model="M1" if i<3 else "M3"
  check("Table 14",model,target,metrics[i%3],printed14[target][i],values[i],cpu_path if i<3 else m3_path)
q={"T1":[.768,.735,.798],"T2":[.611,.570,.650],"T3":[.563,.516,.610],"T4":[.385,.351,.418]}
m={"T1":[.444,.409,.478],"T2":[.401,.378,.426],"T3":[.485,.439,.531],"T4":[.441,.402,.482]}
for judge,published in [("qwen",q),("mistral",m)]:
 for target in tgs:
  source=f"results/server_runs/SERVER_RUN_20261007_A/EXPORTS/experiments/M4_{judge}_fp16_offload_{target}_C/METRICS_AND_CLUSTER_CI.csv"
  row=next(x for x in load(source) if x["group"]=="all")
  for j,metric in enumerate(["macro_f1","ci_low","ci_high"]):
   check("Table 17",judge,target,metric,published[target][j],float(row[metric]),source)
  if target=="T4":check("Table 17",judge,target,"qwk",.463 if judge=="qwen" else .206,float(row["qwk"]),source)
mismatches=[]
hash_path="data/validity_2026_10/FP16_BASELINE_INPUT_HASH_COMPARISON.csv"
for row in load(hash_path):
 if row["target"]=="T1":
  mismatches.append({k:row[k] for k in ("judge","target","n","reference_macroF1","E1_rot0_macroF1","n_changed_decisions","n_different_input_hashes","n_different_token_counts","same_model_revision")})
  if int(row["n_different_input_hashes"])!=720:raise SystemExit("Changed T1 provenance; manual review required")
cols=list(ledger[0])
with (args.out/"TABLES_10_14_17_DISPLAY_CHECK.csv").open("w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(ledger)
status=("PASS_SELECTED_DISPLAY_CELLS_WITH_OPEN_T1_PROTOCOL_DISCREPANCY" if len(ledger)==60 and all(x["status"]=="PASS_DISPLAY_PRECISION" for x in ledger) else "FAIL")
summary={"status":status,"checked_values":len(ledger),"matching_values":sum(x["status"]=="PASS_DISPLAY_PRECISION" for x in ledger),"counts_by_table":{"Table 10":10,"Table 14":24,"Table 17":26},"T1_discrepancies":mismatches,"limits":["source-summary display comparison only","FP16 confidence intervals not independently bootstrapped","model-training protocol not replayed","not all 100 tables certified","external human validation deferred"]}
(args.out/"SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
if status=="FAIL":raise SystemExit(1)
