#!/usr/bin/env python3
"""Exact independent clean-run CHECK of archived 3000-resample E1/E2 CI lineage.
No new model inference. CLI: --fresh path/to/newly_recalculated.csv.
Compares a fresh invocation of the *archived* versioned reanalysis script
against the repository's archived original 3000-row-by-contrast output.
Do not mistake successful matching for independent bootstrap-method validation.
"""
import csv,argparse,json,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--fresh",required=True,type=Path);p.add_argument("--out",type=Path,default=Path("audit_e1e2_3000"));args=p.parse_args()
args.out.mkdir(parents=True,exist_ok=True)
REF=Path("results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv")
HIST=Path("data/validity_2026_10/E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv")
def reader(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def key(x):return tuple(x[k] for k in ("judge","target","experiment","variant"))
reference={key(x):x for x in reader(REF)}
fresh={key(x):x for x in reader(args.fresh)}
historical={key(x):x for x in reader(HIST)}
if len(reference)!=len(fresh)!=20:raise SystemExit("All sources require 20 unique contrasts")
numeric_fields=["n","n_prompt_clusters","changed_n","changed_rate","changed_ci_low","changed_ci_high","base_macroF1","pert_macroF1","delta_macroF1","delta_ci_low","delta_ci_high","correct_to_wrong","wrong_to_correct","wrong_to_wrong_changed","median_baseline_margin_changed","median_baseline_margin_unchanged","bootstrap_reps","seed"]
audit=[];errors=[]
for k in sorted(reference):
 x=reference[k];y=fresh.get(k);z=historical.get(k)
 if y is None or z is None:raise SystemExit("missing key "+str(k))
 d=[]
 for col in numeric_fields:
  a=float(x[col]);b=float(y[col])
  if not (math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=0,abs_tol=1e-12)):d.append(col)
 if d:errors.append({"key":k,"fields":d})
 audit.append({"judge":k[0],"target":k[1],"experiment":k[2],"variant":k[3],
 "reexecuted_equal_archived":not bool(d),
 "delta_f1_point_equal_other_3000":math.isclose(float(x["delta_macroF1"]),float(z["delta_macroF1"]),rel_tol=0,abs_tol=1e-12),
 "delta_ci_low_diff_between_3000_archives":float(x["delta_ci_low"])-float(z["ci_low"]),
 "delta_ci_high_diff_between_3000_archives":float(x["delta_ci_high"])-float(z["ci_high"])})
with (args.out/"E1E2_REANALYSIS_3000_LINEAGE_CHECK.csv").open("w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=list(audit[0]));w.writeheader();w.writerows(audit)
report={"status":"PASS_EXACT_ARCHIVED_REANALYSIS_3000_ONLY" if not errors else "FAIL_RECOMPUTATION_DRIFT",
"rows":len(audit),"numeric_columns_per_row":len(numeric_fields),"matches":sum(x["reexecuted_equal_archived"] for x in audit),
"archived_secondary_3000_ci_rows_different":sum(abs(x["delta_ci_low_diff_between_3000_archives"])>1e-12 or abs(x["delta_ci_high_diff_between_3000_archives"])>1e-12 for x in audit),
"max_secondary_ci_endpoint_abs_diff":max(max(abs(x["delta_ci_low_diff_between_3000_archives"]),abs(x["delta_ci_high_diff_between_3000_archives"])) for x in audit),
"errors":errors,
"limitations":["Only verifies deterministic replay of the published reanalysis implementation, not original historical 250 CI algorithm",
"Two 3000-output families are not byte-equivalent in CI endpoints; source precedence documented separately",
"Does not verify any external sample or LLM generation"]}
(args.out/"SUMMARY.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8");print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
