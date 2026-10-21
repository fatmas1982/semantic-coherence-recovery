#!/usr/bin/env python3
"""Check corrected S-E1E2 display crosswalk against the canonical clean-room E1/E2 CSV.
The source CSV comes from a successful 3000-draw rerun; this checks its
display transcription, original historical numbers and count/point identity.
No original 250-draw bootstrap provenance, model inference, or 100-table
manuscript certification is asserted.
"""
import csv,math,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
read=lambda p:list(csv.DictReader((root/p).open(encoding="utf-8-sig",newline="")))
r=read("results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv")
v=read("results/validity_2026_10/S_E1E2_CORRECTED_CI_3000_20261021.csv")
m={(x["judge"].split("_")[0],x["target"],x["experiment"],x["variant"]):x for x in r}
assert len(r)==len(m)==len(v)==20
nchanged=0;flips=0;problems=[]
for x in v:
 k=tuple(x[z] for z in ("judge","target","experiment","variant"))
 y=m.get(k)
 if y is None:problems.append(str(k)+": no source");continue
 fmt=lambda a,n:format(float(a),f".{n}f")
 target=[
 fmt(float(y["changed_ci_low"])*100,1),
 fmt(float(y["changed_ci_high"])*100,1),
 fmt(y["delta_ci_low"],3),
 fmt(y["delta_ci_high"],3),
 ]
 displayed=[x["revised_changed_ci_low"],x["revised_changed_ci_high"],x["revised_delta_ci_low"],x["revised_delta_ci_high"]]
 norm=lambda a:float(a)
 if any(norm(p)!=norm(q) for p,q in zip(target,displayed)):problems.append(str(k)+": displayed CI mismatch")
 if int(x["paper_n"])!=int(y["n"]) or int(x["changed_n"])!=int(y["changed_n"]):problems.append(str(k)+": count mismatch")
 if norm(x["changed_percent"])!=norm(fmt(float(y["changed_rate"])*100,1)) or norm(x["delta_macro_f1"])!=norm(fmt(y["delta_macroF1"],3)):problems.append(str(k)+": point mismatch")
 if int(y["bootstrap_reps"])!=3000 or int(y["seed"])!=20261009:problems.append(str(k)+": protocol mismatch")
 old=[x["original_changed_ci_low"],x["original_changed_ci_high"],x["original_delta_ci_low"],x["original_delta_ci_high"]]
 ne=sum(float(a)!=float(b) for a,b in zip(old,displayed))
 nchanged+=ne
 if ne!=int(x["changed_display_endpoints"]):problems.append(str(k)+": modified-boundary count mismatch")
 if bool(float(old[2])<=0<=float(old[3]))!=bool(float(displayed[2])<=0<=float(displayed[3])):flips+=1
 assert x["delta_zero_inclusion_changed"]=="false"
if nchanged!=68 or flips!=0:problems.append(f"expected 68 changed endpoints and 0 zero-inclusion flips; got {nchanged}/{flips}")
report={"status":"PASS_SCOPED_20ROW_DISPLAY_CROSSWALK" if not problems else "FAIL","comparison_rows":len(v),"changed_display_endpoints":nchanged,"delta_zero_inclusion_flips":flips,"problems":problems,"scope":"Source CSV display+arithmetic only, not the historical 250 CI method nor complete manuscript"}
print(json.dumps(report,indent=2))
if problems:raise SystemExit(1)
