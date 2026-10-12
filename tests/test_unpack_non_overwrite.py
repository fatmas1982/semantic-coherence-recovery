#!/usr/bin/env python3
"""Regression test: unpacking must not overwrite current release files."""
from pathlib import Path
import hashlib
import shutil
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    (root / "release_bundle").mkdir()
    for part in (SOURCE / "release_bundle").glob("*.part*"):
        shutil.copy2(part, root / "release_bundle" / part.name)
    shutil.copy2(SOURCE / "UNPACK_RELEASE.py", root / "UNPACK_RELEASE.py")
    # Simulate newer checkout documents which must not be overwritten.
    docs = root / "docs"
    docs.mkdir()
    sentinels = {
        "docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv": b"new experiment-to-table matrix\n",
        "docs/REPRODUCIBILITY.md": b"new reproducibility guide\n",
        "docs/RELEASE_VERIFICATION.json": b"{\"new\": true}\n",
    }
    for name, data in sentinels.items():
        (root / name).write_bytes(data)
    def snapshot():
        return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in root.rglob("*") if p.is_file()}
    def run(*args):
        subprocess.run([sys.executable, str(root / "UNPACK_RELEASE.py"), *args],
                       cwd=root, check=True)
    before = snapshot()
    run("--verify-only")
    assert snapshot() == before, "--verify-only modified files"
    run()
    assert all((root / n).read_bytes() == val for n, val in sentinels.items()), "New docs overwritten"
    after = snapshot()
    run()
    assert snapshot() == after, "Second default invocation was not idempotent"
    historical = root / "pristine"
    run("--historical-dir", str(historical))
    assert all((root / n).read_bytes() == val for n, val in sentinels.items())
    assert (historical / "docs" / "REPRODUCIBILITY.md").exists()
    assert (historical / "docs" / "REPRODUCIBILITY.md").read_bytes() != sentinels["docs/REPRODUCIBILITY.md"]
    print("PASS: verification-only, non-overwrite, idempotence, pristine historic extraction")
