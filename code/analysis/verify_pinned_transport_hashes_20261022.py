#!/usr/bin/env python3
"""Verify 151 pinned public release files, not private source-binary identity."""
from pathlib import Path
import csv
import hashlib
import importlib.util
import io
import tarfile

ROOT = Path(__file__).resolve().parents[2]
assert (ROOT / "UNPACK_RELEASE.py").is_file(), "Run from code/analysis in project repository"
spec = importlib.util.spec_from_file_location("release_unpack", ROOT / "UNPACK_RELEASE.py")
assert spec is not None and spec.loader is not None
unpack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unpack)
with tarfile.open(fileobj=io.BytesIO(unpack.bundle_bytes()), mode="r:xz") as archive:
    contents = {entry.name: entry for entry in unpack.members_checked(archive) if entry.isfile()}
    assert "SHA256SUMS.csv" in contents
    fh = archive.extractfile(contents["SHA256SUMS.csv"])
    assert fh is not None
    rows = list(csv.DictReader(io.StringIO(fh.read().decode("utf-8-sig"))))
    assert len(rows) == 151, len(rows)
    for row in rows:
        path = row["path"]
        assert path in contents, ("missing pinned file", path)
        stream = archive.extractfile(contents[path])
        assert stream is not None
        payload = stream.read()
        assert len(payload) == int(row["bytes"]), ("wrong bytes", path)
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], ("hash mismatch", path)
print("PASS_ORIGINAL_PUBLIC_SPLIT_ARCHIVE_151_OF_151")
print("SCOPE: Immutable historical transport files only; modified worktree and private input-binary identities are separate checks.")
