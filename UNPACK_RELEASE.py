#!/usr/bin/env python3
from pathlib import Path
import base64, hashlib, tarfile, tempfile
EXPECTED_SHA256 = "aae397bcc3d4042488866853dd048ea43479a87bc8e4ed4c4e0fb394ddb421fc"
ROOT = Path(__file__).resolve().parent
PART_DIR = ROOT / "release_bundle"
parts = sorted(PART_DIR.glob("semantic_coherence_public_release.tar.gz.b64.part*"))
if not parts:
    raise SystemExit(f"No release parts found under {PART_DIR}")
text = "".join(p.read_text(encoding="ascii").strip() for p in parts)
data = base64.b64decode(text, validate=True)
got = hashlib.sha256(data).hexdigest()
if got != EXPECTED_SHA256:
    raise SystemExit(f"SHA-256 mismatch: {got}")
with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
    tmp.write(data); temp_path = Path(tmp.name)
with tarfile.open(temp_path, "r:gz") as tf:
    tf.extractall(ROOT)
temp_path.unlink(missing_ok=True)
print(f"PASS: extracted {len(parts)} parts; SHA-256={got}")
print("Run: python code/analysis/reproduce_public_metrics.py")
