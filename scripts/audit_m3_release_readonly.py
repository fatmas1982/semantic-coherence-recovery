#!/usr/bin/env python3
"""Read-only audit of the archived M3 release: no training, no new data."""
from pathlib import Path
import csv
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / "results/m3_historical_20261015"
manifest = base / "RELEASE_SHA256_MANIFEST.csv"
issues = []
with manifest.open(newline="", encoding="utf-8-sig") as f:
    records = list(csv.DictReader(f))
for row in records:
    path = ROOT / row["repo_path"]
    if not path.is_file():
        issues.append(("MISSING", row["repo_path"]))
        continue
    actual = path.read_bytes()
    if len(actual) != int(row["bytes"]):
        issues.append(("BYTE_MISMATCH", row["repo_path"]))
    if hashlib.sha256(actual).hexdigest().lower() != row["sha256"].lower():
        issues.append(("SHA256_MISMATCH", row["repo_path"]))
oof = list((base / "oof").glob("OOF_M3_*.csv"))
if len(oof) != 24:
    issues.append(("OOF_COUNT", str(len(oof))))
for file, expected in [
    ("M3_120_FOLD_EXECUTION_LEDGER.csv", 120),
    ("M3_720_GENERATOR_FOLD_EXECUTION_LEDGER.csv", 720),
]:
    path = base / "audits" / file
    with path.open(newline="", encoding="utf-8-sig") as f:
        n = sum(1 for _ in csv.DictReader(f))
    if n != expected:
        issues.append(("LEDGER_COUNT", f"{file}: {n}"))
folds = base / "audits/M3_120_FOLD_EXECUTION_LEDGER.csv"
with folds.open(newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
n_conflicts = sum("CONFLICT:" in (r.get("selected_epochs") or "") for r in rows)
print("Manifest entries:", len(records))
print("OOF files:", len(oof))
print("Fold records:", len(rows))
print("Multi-valued epochs in fold summaries:", n_conflicts)
for typ, path in issues:
    print(typ + ":", path)
if issues:
    sys.exit(1)
print("All checked archived files passed byte/hash and cardinality gates.")
