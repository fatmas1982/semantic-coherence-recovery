#!/usr/bin/env python3
"""Derive legacy R8 CSV names from public archived inputs without model inference.
The historical M4 shard *byte identity* is not claimed; original GOLD XLSX must
be supplied in a private local worktree and MUST NOT be pushed to public GitHub.
"""
from pathlib import Path
import csv
import hashlib
import shutil
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / "data/frozen/baseline_csv_mirror"
m4_all = ROOT / "results/validity/m4_protocol/P2_81_M4_PROTOCOL_SENSITIVITY_OOF_ALL.csv"
m4_dir = ROOT / "reproduced_ipm_followup/reconstructed_m4_oof_from_aggregate"
assert m4_all.is_file() and base.is_dir()
m4_dir.mkdir(parents=True, exist_ok=True)
entries = []
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

for i in (1, 2, 3, 4):
    src = base / f"{9+i:02d}_OOF_T{i}.csv"
    dst = base / f"OOF_T{i}.csv"
    assert src.is_file(), src
    if dst.exists():
        assert sha(src) == sha(dst), ("would overwrite changed alias", dst)
    else:
        shutil.copyfile(src, dst)
    entries.append({"record_type": "BYTE_IDENTICAL_ALIAS", "destination": str(dst.relative_to(ROOT)),
                    "input_source": str(src.relative_to(ROOT)),
                    "cases": sum(1 for _ in src.open(encoding="utf8")) - 1,
                    "sha256_destination": sha(dst), "identity_note": "exact CSV copy"})

df = pd.read_csv(m4_all, dtype={"Case_ID": str, "Prompt_ID": str})
assert len(df) == 9460 and df.source_file.nunique() == 18
assert not df.duplicated(["source_file", "Case_ID"]).any()
expected = {"T1": 720, "T2": 474, "T3": 460, "T4": 474}
for name, group in df.groupby("source_file", sort=True):
    assert "/" not in name and name.startswith("OOF_M4_SENS_T") and name.endswith(".csv")
    target = name.split("_")[3]
    assert target in expected and len(group) == expected[target]
    dest = m4_dir / name
    group.drop(columns=["source_file"]).to_csv(dest, index=False, encoding="utf-8")
    entries.append({"record_type": "RECONSTRUCTED_FROM_AGGREGATE",
                    "destination": str(dest.relative_to(ROOT)),
                    "input_source": str(m4_all.relative_to(ROOT)),
                    "cases": len(group), "sha256_destination": sha(dest),
                    "identity_note": "logical records matched aggregate source_file; historical shard bytes not recovered"})
with (m4_dir / "FOLLOWUP_INPUT_DERIVATION_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(entries[0]))
    writer.writeheader()
    writer.writerows(entries)
print("PASS_ARCHIVED_FOLLOWUP_INPUT_DERIVATION", len(entries),
      "files: 4 unchanged baseline aliases and 18 logically reconstructed M4 shards")
print("PRIVATE_GOLD_REQUIRED_LOCALLY_ONLY", ROOT / "data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx")
