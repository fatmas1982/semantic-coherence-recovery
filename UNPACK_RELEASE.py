#!/usr/bin/env python3
"""Verify the immutable base bundle and add missing files without overwriting checkout files.

Use --historical-dir PATH for a separate pristine extraction, or --verify-only
for integrity validation. The default preserves all existing files, including
newer release documentation, and extracts missing historical files only.
"""
from pathlib import Path
import argparse
import base64
import csv
import hashlib
import io
import tarfile

EXPECTED_SHA256 = "69ce2a52c201424d8939d1a997dc3bd34854a2822131c6bc69a791b47635ce3e"
EXPECTED_PARTS = 86
ROOT = Path(__file__).resolve().parent
PART_DIR = ROOT / "release_bundle"
PART_PREFIX = "semantic_coherence_public_release.tar.xz.b64.part"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bundle_bytes():
    paths = sorted(PART_DIR.glob(PART_PREFIX + "*"))
    expected = [PART_DIR / (PART_PREFIX + f"{i:04d}") for i in range(1, EXPECTED_PARTS + 1)]
    if paths != expected:
        raise SystemExit(f"Expected {EXPECTED_PARTS} ordered parts; found {len(paths)}")
    try:
        data = base64.b64decode(
            "".join(p.read_text(encoding="ascii").strip() for p in paths),
            validate=True,
        )
    except (ValueError, base64.binascii.Error) as exc:
        raise SystemExit(f"Base64 assembly failed: {exc}") from exc
    if digest(data) != EXPECTED_SHA256:
        raise SystemExit("Archive SHA-256 mismatch")
    return data


def members_checked(tf):
    members = tf.getmembers()
    names = set()
    for member in members:
        p = Path(member.name)
        if (not member.name or p.is_absolute() or ".." in p.parts
                or member.issym() or member.islnk()
                or not (member.isfile() or member.isdir())):
            raise SystemExit(f"Unsafe archive member: {member.name!r}")
        if member.name in names:
            raise SystemExit(f"Duplicate archive member: {member.name}")
        names.add(member.name)
    return members


def extract_safe(tf, members, destination, preserve_existing=True):
    destination.mkdir(parents=True, exist_ok=True)
    written = skipped = 0
    for m in members:
        target = destination.joinpath(*Path(m.name).parts)
        # Do not follow symlinks already present in the filesystem.
        ancestors = [destination, *list(target.parents)[:-1]]
        if any(a.is_symlink() for a in ancestors) or target.is_symlink():
            raise SystemExit(f"Refusing symlink path: {target}")
        if m.isdir():
            if target.exists() and not target.is_dir():
                raise SystemExit(f"Directory collision: {target}")
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists():
            if not target.is_file():
                raise SystemExit(f"File collision: {target}")
            if preserve_existing:
                skipped += 1
                continue
        target.parent.mkdir(parents=True, exist_ok=True)
        stream = tf.extractfile(m)
        if stream is None:
            raise SystemExit(f"Cannot read archived file: {m.name}")
        # Exclusive creation prevents overwriting a concurrent change.
        with target.open("xb") as out:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        written += 1
    return written, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--historical-dir", type=Path,
                    help="Extract original files into this separate, initially empty directory")
    args = ap.parse_args()
    raw = bundle_bytes()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:xz") as tf:
        members = members_checked(tf)
        if args.verify_only:
            for m in members:
                if m.isfile():
                    stream = tf.extractfile(m)
                    if stream is None:
                        raise SystemExit(f"Unreadable entry: {m.name}")
                    while stream.read(1024 * 1024):
                        pass
            print(f"PASS: archive SHA-256 and {len(members)} safe readable entries")
            return
        if args.historical_dir:
            dest = args.historical_dir.resolve()
            if dest == ROOT or ROOT in dest.parents:
                # Dedicated subdirectory under repo is permitted, but not repo root.
                pass
            if dest == ROOT or (dest.exists() and any(dest.iterdir())):
                raise SystemExit("Historical destination must be a new or empty directory")
        else:
            dest = ROOT
        written, skipped = extract_safe(tf, members, dest)
    print(f"PASS: {EXPECTED_PARTS} fragments; SHA-256: {digest(raw)}")
    print(f"Extracted missing files: {written}; preserved existing files: {skipped}")
    print("For pristine historical copy: python UNPACK_RELEASE.py --historical-dir /tmp/semantic-frozen-base")


if __name__ == "__main__":
    main()
