#!/usr/bin/env python3
"""Safely verify and unpack the immutable 86-part historical reference archive.

Historical files are checked in .frozen_reference_2026/ and copied into the
working checkout ONLY when the target path does not yet exist.  Never replace
a newer checked-in release document or script with the 2026 historical copy.

This is an archived-prediction analysis reproducer, not historical training.
"""
from __future__ import annotations
import base64
import csv
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / ".frozen_reference_2026"
PART_DIR = ROOT / "release_bundle"
PREFIX = "semantic_coherence_public_release.tar.xz.b64.part"
EXPECTED_PARTS = 86
EXPECTED_HASH = "69ce2a52c201424d8939d1a997dc3bd34854a2822131c6bc69a791b47635ce3e"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(name: str) -> Path:
    name = name.replace("\\", "/")
    p = PurePosixPath(name)
    if not name or p.is_absolute() or ".." in p.parts or not p.parts:
        raise ValueError(f"Unsafe archive member: {name!r}")
    return Path(*p.parts)


def run() -> None:
    pieces = sorted(PART_DIR.glob(PREFIX + "*"))
    expected = [PREFIX + f"{i:04d}" for i in range(1, EXPECTED_PARTS + 1)]
    if [x.name for x in pieces] != expected:
        raise AssertionError("Expected all 86 ordered release transport fragments")
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in pieces)
    binary = base64.b64decode(encoded, validate=True)
    if hashlib.sha256(binary).hexdigest() != EXPECTED_HASH:
        raise AssertionError("Historical immutable transport SHA256 mismatch")
    STAGE.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".tar.xz", delete=False) as f:
        f.write(binary)
        filename = Path(f.name)
    try:
        with tarfile.open(filename, "r:xz") as tf:
            for member in tf.getmembers():
                safe_path(member.name)
                if not (member.isfile() or member.isdir()):
                    raise ValueError(f"Unexpected non-regular tar member: {member.name}")
            tf.extractall(STAGE, filter="data")
    finally:
        filename.unlink(missing_ok=True)
    manifest = STAGE / "SHA256SUMS.csv"
    with manifest.open(newline="", encoding="utf-8-sig") as f:
        entries = list(csv.DictReader(f))
    if len(entries) != 151:
        raise AssertionError(f"Expected 151 frozen-file manifest rows, got {len(entries)}")
    copied, matches, conflicts = [], [], []
    for r in entries:
        rel = safe_path(r["path"])
        source = STAGE / rel
        destination = ROOT / rel
        if not source.is_file():
            raise AssertionError(f"Historical manifest input missing: {rel}")
        got = sha256(source)
        if got.lower() != r["sha256"].strip().lower() or source.stat().st_size != int(r["bytes"]):
            raise AssertionError(f"Historical manifest checksum or size mismatch: {rel}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(source, destination)
            copied.append(str(rel))
        elif destination.is_file() and sha256(destination) == got:
            matches.append(str(rel))
        else:
            conflicts.append({"path":str(rel),"archived_sha256":got,
                              "existing_sha256":sha256(destination) if destination.is_file() else "NOT_A_FILE"})
    report = {"transport_sha256":EXPECTED_HASH, "manifest_verified":151,
              "new_files_copied":len(copied),"same_files":len(matches),
              "newer_checkout_files_preserved":len(conflicts),"preserved_conflicts":conflicts}
    (ROOT / "UNPACK_PROVENANCE_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("PASS: immutable historical archive verified: 86 fragments, 151 manifest entries")
    print(f"PASS: safe integration: copied={len(copied)}, unchanged={len(matches)}, preserved_collisions={len(conflicts)}")
    if conflicts:
        print("ARCHIVED-VERSUS-CHECKOUT COLLISIONS (preserved; historical copy in .frozen_reference_2026):")
        for c in conflicts:
            print(" -",c["path"])
    print("Next: python code/analysis/reproduce_public_metrics.py")


if __name__ == "__main__":
    run()
