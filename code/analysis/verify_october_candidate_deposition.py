#!/usr/bin/env python3
"""Fail-closed audit of the author's October candidate files after GitHub checkout.

This is a deposition/integrity gate, not a claim of rerunning training.
Run: python code/analysis/verify_october_candidate_deposition.py
"""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "release" / "2026-10"
MANIFEST = ARTIFACTS / "RELEASE_CANDIDATE_SHA256_MANIFEST.csv"

def main():
    if not MANIFEST.is_file():
        raise SystemExit("FAIL: candidate manifest is not deposited on main")
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig", newline="")))
    if not rows:
        raise SystemExit("FAIL: empty candidate manifest")
    names = [r["file_name"] for r in rows]
    if len(names) != len(set(names)):
        raise SystemExit("FAIL: duplicate artifact manifest paths")
    failures = []
    for entry in rows:
        rel = Path(entry["file_name"])
        if rel.is_absolute() or ".." in rel.parts or len(rel.parts) != 1:
            failures.append("unsafe path " + str(rel))
            continue
        item = ARTIFACTS / rel
        if not item.is_file():
            failures.append("MISSING " + str(rel))
            continue
        actual = hashlib.sha256(item.read_bytes()).hexdigest()
        if actual != entry["sha256"].lower():
            failures.append("HASH_MISMATCH " + str(rel))
        if item.stat().st_size != int(entry["size_bytes"]):
            failures.append("SIZE_MISMATCH " + str(rel))
    for mandatory in [
        "IPM_MAIN_GOVERNANCE_RECONCILED.docx",
        "IPM_SUPPLEMENT_GOVERNANCE_RECONCILED.docx",
        "P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(2).zip",
    ]:
        if mandatory not in names:
            failures.append("NOT_IN_MANIFEST " + mandatory)
    if failures:
        raise SystemExit("FAIL: candidate release not self-contained:\n" + "\n".join(failures))
    print(f"PASS: {len(rows)} release candidates present with matching sizes and SHA-256")
    print("WARNING: full paper results, intervals and GPU/CPU training have NOT been independently reproduced")

if __name__ == "__main__":
    main()
