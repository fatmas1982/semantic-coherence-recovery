#!/usr/bin/env python3
"""Publish explicitly approved October candidate into main (authenticated local clone).

Run from a computer with authenticated Git access:
  python scripts/publish_october_candidate.py --source /path/to/IPM_PUBLIC_RELEASE_HANDOFF_WITH_PUBLISHER_20261012.zip

Fails before pushing if the candidate is missing, invalid or if the checkout is
not clean/updated. Does not certify scientific correctness of manuscript claims.
"""
import argparse
import csv
import hashlib
import io
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "release" / "2026-10"

def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout.strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    a = ap.parse_args()
    remote = run("git", "remote", "get-url", "origin")
    if "fatmas1982/semantic-coherence-recovery" not in remote:
        raise SystemExit("Wrong origin repository")
    if run("git", "branch", "--show-current") != "main":
        raise SystemExit("Checkout main first")
    if run("git", "status", "--porcelain"):
        raise SystemExit("Working tree is not clean")
    run("git", "fetch", "origin", "main")
    if run("git", "rev-parse", "HEAD") != run("git", "rev-parse", "origin/main"):
        raise SystemExit("Local main is not up-to-date with origin/main")
    with zipfile.ZipFile(a.source) as outer:
        archive_names = [name for name in outer.namelist()
                         if name.startswith("IPM_REPRODUCIBILITY_GOVERNANCE_RELEASE_CANDIDATE_")
                         and name.endswith(".zip")]
        if len(archive_names) != 1:
            raise SystemExit("Expected exactly one candidate archive inside handoff")
        candidate = outer.read(archive_names[0])
    files = {}
    with zipfile.ZipFile(io.BytesIO(candidate)) as z:
        manifest_name = "RELEASE_CANDIDATE_SHA256_MANIFEST.csv"
        raw_manifest = z.read(manifest_name)
        manifest = list(csv.DictReader(io.StringIO(raw_manifest.decode("utf-8-sig"))))
        if len(manifest) != 14:
            raise SystemExit(f"Expected 14 candidate files, found {len(manifest)}")
        for row in manifest:
            name = row["file_name"]
            if not name or name != Path(name).name or name in {".", ".."} or name in files:
                raise SystemExit("Invalid or duplicate name: " + repr(name))
            payload = z.read(name)
            if (hashlib.sha256(payload).hexdigest() != row["sha256"].lower()
                    or len(payload) != int(row["size_bytes"])):
                raise SystemExit("Digest or size mismatch: " + name)
            files[name] = payload
    DEST.mkdir(parents=True, exist_ok=True)
    for name, payload in files.items():
        (DEST / name).write_bytes(payload)
    (DEST / "RELEASE_CANDIDATE_SHA256_MANIFEST.csv").write_bytes(raw_manifest)
    run("python", "code/analysis/verify_october_candidate_deposition.py")
    run("git", "add", "release/2026-10")
    if not run("git", "diff", "--cached", "--name-only"):
        print("Already deposited and validated")
        return
    run("git", "commit", "-m", "data: publish SHA-256 verified October research candidate")
    run("git", "push", "origin", "main")
    print("PUBLISHED", run("git", "rev-parse", "HEAD"))
    print("Check Actions, then independently audit all manuscript tables before final release.")

if __name__ == "__main__":
    main()
