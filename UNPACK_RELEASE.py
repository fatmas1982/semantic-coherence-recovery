#!/usr/bin/env python3
from pathlib import Path
import base64
import hashlib
import tarfile
import tempfile

EXPECTED_SHA256 = "69ce2a52c201424d8939d1a997dc3bd34854a2822131c6bc69a791b47635ce3e"
EXPECTED_PARTS = 86
ROOT = Path(__file__).resolve().parent
PART_DIR = ROOT / "release_bundle"
PART_GLOB = "semantic_coherence_public_release.tar.xz.b64.part*"

parts = sorted(PART_DIR.glob(PART_GLOB))
if len(parts) != EXPECTED_PARTS:
    raise SystemExit(
        f"Expected {EXPECTED_PARTS} release fragments under {PART_DIR}, found {len(parts)}: "
        + ", ".join(p.name for p in parts)
    )

names = [p.name for p in parts]
expected_names = [f"semantic_coherence_public_release.tar.xz.b64.part{i:04d}" for i in range(1, EXPECTED_PARTS + 1)]
if names != expected_names:
    raise SystemExit("Release fragment sequence is incomplete or misordered.")

text = "".join(p.read_text(encoding="ascii").strip() for p in parts)
try:
    data = base64.b64decode(text, validate=True)
except Exception as exc:
    raise SystemExit(f"Base64 reconstruction failed: {exc}") from exc

got = hashlib.sha256(data).hexdigest()
if got != EXPECTED_SHA256:
    raise SystemExit(f"SHA-256 mismatch: expected {EXPECTED_SHA256}, got {got}")

with tempfile.NamedTemporaryFile(suffix=".tar.xz", delete=False) as tmp:
    tmp.write(data)
    temp_path = Path(tmp.name)

try:
    with tarfile.open(temp_path, "r:xz") as tf:
        try:
            tf.extractall(ROOT, filter="data")
        except TypeError:  # Python < 3.12
            tf.extractall(ROOT)
finally:
    temp_path.unlink(missing_ok=True)

print(f"PASS: reconstructed and extracted {len(parts)} fragments")
print(f"SHA-256: {got}")
print("Next: python code/analysis/reproduce_public_metrics.py")
