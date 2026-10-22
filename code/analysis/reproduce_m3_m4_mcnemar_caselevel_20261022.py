#!/usr/bin/env python3
"""Recompute M3/M4 paired correctness McNemar tests from release OOF case files.

Usage: from repository root after python UNPACK_RELEASE.py:
    python code/analysis/reproduce_m3_m4_mcnemar_caselevel_20261022.py
"""
from __future__ import annotations

import csv
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "T1": (720, 114, 161, 275, "0.005443"),
    "T2": (474, 144, 70, 214, "<.001"),
    "T3": (460, 179, 47, 226, "<.001"),
    "T4": (474, 186, 80, 266, "<.001"),
}


def read_unique(path: Path, pred_col: str):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"Case_ID", "Prompt_ID", "y_true", pred_col}
        if not required.issubset(reader.fieldnames or []):
            raise AssertionError(f"Missing required columns: {path}")
        rows = list(reader)
    by_id = {row["Case_ID"]: row for row in rows}
    if not rows or len(by_id) != len(rows):
        raise AssertionError(f"Missing or duplicate case IDs: {path}")
    return by_id


def two_sided_binomial_p(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / (2 ** n))


def main():
    for target, (n_expected, cw_expected, wc_expected, nd_expected, print_p) in EXPECTED.items():
        root = ROOT / "data" / "computational"
        m3 = read_unique(
            root / "m3" / f"OOF_M3_{target}_C_seed20260908.csv", "M3_pred"
        )
        m4 = read_unique(root / "m4" / f"OOF_M4_FORCED_{target}_C.csv", "M4_pred")
        if len(m3) != n_expected or set(m3) != set(m4):
            raise AssertionError(f"{target}: incomplete/mismatched case universe")
        cw = wc = 0
        for case_id, r3 in m3.items():
            r4 = m4[case_id]
            if (
                r3["Prompt_ID"] != r4["Prompt_ID"]
                or int(r3["y_true"]) != int(r4["y_true"])
            ):
                raise AssertionError(f"{target}: gold/prompt mismatch {case_id}")
            truth = int(r3["y_true"])
            m3_ok = int(r3["M3_pred"]) == truth
            m4_ok = int(r4["M4_pred"]) == truth
            cw += int(m3_ok and not m4_ok)
            wc += int(not m3_ok and m4_ok)
        p = two_sided_binomial_p(cw, wc)
        p_ok = p < .001 if print_p == "<.001" else abs(p - float(print_p)) < 5e-7
        if (cw, wc, cw + wc) != (cw_expected, wc_expected, nd_expected) or not p_ok:
            raise AssertionError(f"{target}: discrepancy with Supplement S61")
        print(f"{target}: n={n_expected} M3_only={cw} M4_only={wc} "
              f"discordant={cw + wc} exact_two_sided_p={p:.17g} PASS")
    print("PASS: 4/4 case-level McNemar comparisons")


if __name__ == "__main__":
    main()
