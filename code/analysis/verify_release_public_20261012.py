#!/usr/bin/env python3
"""Reproducibility gate for public archival CSVs, not unavailable original XLSX.

Do not mistake recorded source-binary SHA256 values for publicly downloadable
original workbook binaries. Check historical binaries when provided locally,
otherwise retain explicit NOT_VERIFIED_SOURCE_BINARY rather than claim success.
"""
from pathlib import Path
import csv,hashlib
import subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
sources=ROOT/"SOURCE_BINARY_HASHES.csv"
with sources.open(encoding="utf-8-sig",newline="") as f: reg=list(csv.DictReader(f))
expected={
 "P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx":
   "ccc910b7bafbfa9607e93ef2eba8605f56f7ed87460ef74892d4877c7db4de65",
 "P2_CPU_Baselines_v1.0.xlsx":
   "4502e71bd6d1b6d2941b0b10650caaa433d7188bf958017d2fc646d328a31163"
}
for filename,sha in expected.items():
    row=next((r for r in reg if r["source_file"]==filename),None)
    assert row is not None and row["sha256"]==sha
    loc=ROOT/"data/frozen"/filename
    if loc.is_file():
        observed=hashlib.sha256(loc.read_bytes()).hexdigest()
        assert observed==sha,("historical source binary mismatch",filename)
        print("PASS_SOURCE_BINARY_SHA256",filename)
    else:
        print("NOT_VERIFIED_SOURCE_BINARY",filename,"source SHA recorded; original binary not distributed")
# CI builds an isolated frozen tree; ordinary \`python UNPACK_RELEASE.py\` does not.
# Prefer the historical tree for full 151/151 checks. A standard worktree may
# deliberately preserve newer files at colliding paths and is audited separately.
frozen = ROOT / ".frozen_reference_2026"
reference = frozen if (frozen / "SHA256SUMS.csv").is_file() else ROOT
with (reference / "SHA256SUMS.csv").open(newline="") as f:
    manifest = list(csv.DictReader(f))
assert len(manifest) == 151
matches = []
mismatches = []
for entry in manifest:
    target = reference / entry["path"]
    actual = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
    if actual == entry["sha256"] and target.stat().st_size == int(entry["bytes"]):
        matches.append(entry["path"])
    else:
        mismatches.append(entry["path"])
if reference == frozen:
    assert not mismatches, ("frozen reference archive changed", mismatches)
    print("PASS_FROZEN_REFERENCE_SHA256_151_OF_151")
else:
    print("WORKTREE_FROZEN_MANIFEST_MATCH", len(matches), "/ 151")
    if mismatches:
        print("NONFROZEN_PRESERVED_CURRENT_FILES", len(mismatches),
              "— NOT 151/151 archive-bitwise certification")

for path in ("data/publication/canonical_publication_dataset_720.csv",
 "data/raw/generated_outputs_720.csv",
 "data/annotation/locked_core_ratings/locked_pre_resolution_core_ratings_long_2160.csv",
 "data/annotation/historical_full_csv/A1/Annotation.csv",
 "data/annotation/historical_full_csv/A2/Annotation.csv",
 "data/annotation/historical_full_csv/A3/Annotation.csv"):
    assert (ROOT/path).is_file(),path
for command in [
 [sys.executable,str(ROOT/"code/analysis/reproduce_public_metrics.py")],
 [sys.executable,str(ROOT/"code/analysis/verify_all_frozen_case_layers_20261012.py")]
]:
    subprocess.run(command,cwd=ROOT,check=True)
print("PASS_PUBLIC_NUMERICAL_ARCHIVE: frozen primary outputs and OOF linkage; "
      f"frozen manifest matched {len(matches)}/151 in reference {reference.relative_to(ROOT)}")
print("IMPORTANT: historical original XLSX/PDF source-binary identity is not certified by the public release alone.")
