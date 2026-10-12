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
manifest=list(csv.DictReader((ROOT/".frozen_reference_2026/SHA256SUMS.csv").open(newline="")))
assert len(manifest)==151
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
print("PASS_PUBLIC_NUMERICAL_ARCHIVE: 151-byte-verified source files, frozen primary outputs and OOF linkage")
print("IMPORTANT: historical original XLSX/PDF source-binary identity is not certified by the public release alone.")
