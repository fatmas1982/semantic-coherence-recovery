#!/usr/bin/env python3
"""Check the 33-row paper-to-artifact matrix against the unpacked checkout.

Checks existence, not numerical integrity or availability of archived GPU
trainer execution. Returns explicit UNCERTAIN instead of guessing at abbreviated
paths or a user's unpublished source workbook. Writes a non-sensitive CSV.
"""
from pathlib import Path
import csv,re
ROOT=Path(__file__).resolve().parents[2]
M=ROOT/"docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv"
OUT=ROOT/"results/EXPERIMENT_ARTIFACT_PATH_AUDIT_20261012.csv"
codepat=re.compile(r'code/[A-Za-z0-9_.\-/]+\.(?:py|ipynb)')
pathpat=re.compile(r'(?:data|results)/[A-Za-z0-9_./\-]+\.(?:csv|json|xlsx|txt)')
def unique(seq):
    return list(dict.fromkeys(seq))
with M.open(newline="",encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
assert len(rows)==33,(len(rows),"33 expected")
out=[]
for r in rows:
    codes=unique(codepat.findall(r["Code_or_notebook"]))
    c_exist=[p for p in codes if (ROOT/p).is_file()]
    src=unique(pathpat.findall(r["Primary_input"]))
    dest=unique(pathpat.findall(r["Primary_output"]))
    src_yes=[p for p in src if (ROOT/p).is_file()]
    dest_yes=[p for p in dest if (ROOT/p).is_file()]
    src_missing=[p for p in src if p not in src_yes]
    dest_missing=[p for p in dest if p not in dest_yes]
    code_missing=[p for p in codes if p not in c_exist]
    status="CODE_MISSING" if code_missing else "CODE_REFERENCES_PRESENT"
    if not codes:status="NO_EXACT_CODE_PATH_IN_MATRIX"
    result=dict(experiment=r["Experiment_or_claim"],reference=r["Paper_table_or_figure"],
                code_refs=len(codes),code_found=len(c_exist),
                explicit_input_refs=len(src),input_found=len(src_yes),
                explicit_output_refs=len(dest),output_found=len(dest_yes),
                code_status=status,
                missing_code="; ".join(code_missing),
                missing_inputs="; ".join(src_missing),
                missing_outputs="; ".join(dest_missing),
                execution_verification=r.get("Execution_verification_status",""),
                scope_warning="Existence-only check; shorthand artifact names and non-public source binaries are not verified")
    out.append(result)
assert len(out)==33
OUT.parent.mkdir(exist_ok=True)
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]))
    w.writeheader();w.writerows(out)
for row in out:
    print("COMPONENT",row["experiment"],"code",row["code_found"],"/",row["code_refs"],
          "direct_inputs",row["input_found"],"/",row["explicit_input_refs"],
          "direct_outputs",row["output_found"],"/",row["explicit_output_refs"])
print("EXACT_CODE_REFERENCES_TOTAL",sum(r["code_refs"] for r in out),
      "MISSING",sum(bool(r["missing_code"]) for r in out))
print("REFERENCED_SOURCE_FILES_MISSING",sum(bool(r["missing_inputs"]) for r in out))
print("REFERENCED_OUTPUT_FILES_MISSING",sum(bool(r["missing_outputs"]) for r in out))
print("EXPERIMENT_MATRIX",len(out),"CSV_REPORT",OUT)
