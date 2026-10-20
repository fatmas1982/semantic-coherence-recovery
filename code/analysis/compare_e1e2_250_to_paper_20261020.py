#!/usr/bin/env python3
"""Compare freshly executed 250-draw E1/E2 results with printed historical Supplement S-E1E2.

The historical table is frozen in:
results/validity_2026_10/SUPP_S_E1E2_250_VS_3000_EXACT_20_ROW_AUDIT_20261020.csv
This comparison does not assert that the October reanalysis implementation
is necessarily byte-identical to the historical 250-draw implementation.
It uses the *same frozen case pairs* and the *later archived Python reanalysis*
with a different --bootstrap-reps argument. Mismatches remain disclosures.
"""
from pathlib import Path
import argparse,csv,json,math
p=argparse.ArgumentParser()
p.add_argument("--fresh",type=Path,required=True,help="Output of 250-draw reanalysis")
p.add_argument("--paper-crosswalk",type=Path,default=Path("results/validity_2026_10/SUPP_S_E1E2_250_VS_3000_EXACT_20_ROW_AUDIT_20261020.csv"))
p.add_argument("--out",type=Path,default=Path("audit_e1e2_250"))
args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
def rows(path):
 with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
fresh={(x["judge"].split("_")[0],x["target"],x["experiment"],x["variant"]):x for x in rows(args.fresh)}
out=[]
for x in rows(args.paper_crosswalk):
 k=(x["judge"],x["target"],x["experiment"],x["variant"])
 if k not in fresh:raise SystemExit("Missing 250-draw group: "+str(k))
 y=fresh[k]
 assert y["bootstrap_reps"]=="250"
 fields={
 "changed_ci_low":(float(x["paper_changed_ci_low"]),100*float(y["changed_ci_low"]),1),
 "changed_ci_high":(float(x["paper_changed_ci_high"]),100*float(y["changed_ci_high"]),1),
 "delta_ci_low":(float(x["paper_delta_ci_low"]),float(y["delta_ci_low"]),3),
 "delta_ci_high":(float(x["paper_delta_ci_high"]),float(y["delta_ci_high"]),3),
 }
 flags={z:round(src,d)==round(paper,d) for z,(paper,src,d) in fields.items()}
 out.append({"judge":k[0],"target":k[1],"experiment":k[2],"variant":k[3],
   **{z+"_paper":a for z,(a,b,d) in fields.items()},
   **{z+"_recomputed250":b for z,(a,b,d) in fields.items()},
   **{z+"_equal_printed":flags[z] for z in fields}})
assert len(out)==20
with (args.out/"E1E2_250_VS_HISTORIC_TABLE_COMPARISON.csv").open("w",encoding="utf-8",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
counts={z:sum(x[z+"_equal_printed"] for x in out) for z in fields}
report={"status":"SCOPED_250DRAW_COMPARISON_COMPLETED","rows":len(out),"matches_out_of_20":counts,
"protocol":"Archived case pairs, later versioned reanalysis implementation, 250 RNG draws, seed 20261009",
"interpretation":"CI mismatches indicate algorithm/environment/original lineage ambiguity; no automatic manuscript replacements",
"no_claims":["Original historical 250-draw source implementation exactly replayed","All 100 manuscript tables verified","Model inference reproduced"]}
(args.out/"SUMMARY.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
