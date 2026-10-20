#!/usr/bin/env python3
"""Bounded 2026-10-20 verification of two author-provided audit ZIPs.
Usage: python code/analysis/reconcile_oct20_reviewer_packages.py CLOSURE.zip RUN_PROVENANCE.zip --out output_dir
Does NOT recompute source model metrics or certify manuscript values.
"""
import argparse,csv,io,json,zipfile,hashlib
from collections import Counter
from pathlib import Path
P=argparse.ArgumentParser()
P.add_argument("closure_zip",type=Path);P.add_argument("run_zip",type=Path);P.add_argument("--out",type=Path,default=Path("oct20_reviewer_report"))
def rows(z,p):return list(csv.DictReader(io.StringIO(z.read(p).decode("utf-8-sig"))))
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
a=P.parse_args();a.out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.closure_zip) as c,zipfile.ZipFile(a.run_zip) as r:
 assert c.testzip() is None and r.testzip() is None,"ZIP CRC failure"
 tables=rows(c,"TABLE_BY_TABLE_VERIFICATION_MATRIX.csv")
 review=rows(c,"REVIEWER_EXPERIMENT_CLOSURE_MATRIX.csv")
 oof=rows(r,"SERVER_OOF_RECALCULATED_AND_VALIDATED.csv")
 trace=rows(r,"CLAIM_TO_ARTIFACT_TRACEABILITY.csv")
 errors=rows(r,"RUN_ERROR_PROVENANCE.csv")
 decisions=Counter(x["decision"] for x in tables)
 statuses=Counter(x["status"] for x in oof)
 recovery=Counter(x["recovery_status"] for x in errors)
 failures=[]
 if len(tables)!=100:failures.append("unexpected table count")
 if any("UNVERIFIED" not in x["decision"] for x in tables):failures.append("one or more tables claim an unexpected closure state; inspect manually")
 if len(oof)!=56:failures.append("unexpected OOF inventory count")
 for row in oof:
  for col in ("missing_reference_ids","extra_run_ids","label_mismatches","missing_or_invalid_predictions","invalid_pred_labels"):
   if int(row[col])!=0:failures.append(row["path"]+": "+col)
  if row["status"]!="DATA_PASS_PROTOCOL_UNVERIFIED":failures.append(row["path"]+": changed verification semantics")
 result={"status":"FAIL" if failures else "PASS_INVENTORY_ONLY","table_count":len(tables),"table_status":dict(decisions),
 "reviewer_issue_count":len(review),"oof_count":len(oof),"oof_status":dict(statuses),
 "claim_trace_count":len(trace),"error_pattern_rows":len(errors),"error_recovery_status":dict(recovery),
 "source_sha256":{a.closure_zip.name:sha(a.closure_zip),a.run_zip.name:sha(a.run_zip)},
 "failed_invariants":failures,
 "not_verified":["all manuscript table metrics","M3 train-dev-test replay","judge prompt permutation","historical run recovery","bootstrap and GEE statistical refit","publication rights"]}
 (a.out/"OCT20_REVIEWER_INVENTORY_AUDIT.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,indent=2))
 if failures:raise SystemExit(1)
