#!/usr/bin/env python3
"""Reproduce the explicit-ambiguity exclusion sensitivity used in the IP&M manuscript.

Inputs are the public CSV mirrors of the three locked annotator Annotation sheets:
  data/annotation/historical_full_csv/A1/Annotation.csv
  data/annotation/historical_full_csv/A2/Annotation.csv
  data/annotation/historical_full_csv/A3/Annotation.csv

The script recomputes:
- nominal Krippendorff alpha and exact agreement for fine labels, collapsed families,
  and grounding boundary on all cases and after excluding any case explicitly
  flagged ambiguous by at least one annotator;
- ordinal Krippendorff alpha and exact agreement for severity on all cases,
  non-ambiguous cases, explicitly ambiguous cases, the majority-failure subset,
  and the majority-failure subset after ambiguity exclusion.

No adjudicated fields or model predictions are used. The analysis operates only on
locked pre-resolution A1/A2/A3 ratings.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

DEFAULT_A1 = Path("data/annotation/historical_full_csv/A1/Annotation.csv")
DEFAULT_A2 = Path("data/annotation/historical_full_csv/A2/Annotation.csv")
DEFAULT_A3 = Path("data/annotation/historical_full_csv/A3/Annotation.csv")
DEFAULT_OUT = Path("results/followup/P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.csv")

PAPER_EXPECTED = {
    ("Fine labels", "All cases"): (720, 0.707, 0.703147),
    ("Fine labels", "Non-ambiguous"): (684, 0.719, 0.713285),
    ("Families", "All cases"): (720, 0.758, 0.730530),
    ("Families", "Non-ambiguous"): (684, 0.770, 0.741196),
    ("Grounding boundary", "All cases"): (720, 0.744, 0.723208),
    ("Grounding boundary", "Non-ambiguous"): (684, 0.753, 0.729319),
    ("Ordinal severity", "All cases"): (720, 0.606, 0.783965),
    ("Ordinal severity", "Non-ambiguous"): (684, 0.621, 0.792742),
    ("Ordinal severity", "Explicitly ambiguous"): (36, 0.306, 0.559790),
    ("Ordinal severity", "Majority-failure subset"): (445, 0.501, 0.528338),
    ("Ordinal severity", "Majority-failure excluding explicit ambiguity"): (414, 0.512, 0.532075),
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--a1", type=Path, default=DEFAULT_A1)
    p.add_argument("--a2", type=Path, default=DEFAULT_A2)
    p.add_argument("--a3", type=Path, default=DEFAULT_A3)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument(
        "--skip-paper-check",
        action="store_true",
        help="Do not compare the recomputed results with the frozen manuscript values.",
    )
    return p.parse_args()


def read_annotation_csv(path: Path) -> Dict[str, Dict[str, str]]:
    required = {"case_id", "primary_label", "boundary_zone", "severity_score", "ambiguity_flag"}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
        rows: Dict[str, Dict[str, str]] = {}
        for row in reader:
            cid = (row.get("case_id") or "").strip()
            if not cid:
                continue
            if cid in rows:
                raise ValueError(f"{path}: duplicate case_id {cid}")
            rows[cid] = row
    if not rows:
        raise ValueError(f"{path}: no annotation rows found")
    return rows


def normalise_label(x: str) -> str:
    return (x or "").strip()


def collapsed_family(label: str) -> str:
    x = normalise_label(label)
    if x.startswith("SCF-"):
        return "Core SCF"
    if x.startswith("OVR-"):
        return "OVR"
    if x in {"HREF", "NONE"}:
        return x
    raise ValueError(f"Unexpected primary label: {x!r}")


def is_explicit_ambiguity(row: Dict[str, str]) -> bool:
    return normalise_label(row.get("ambiguity_flag", "")).lower() == "yes"


def exact_agreement(matrix: Sequence[Sequence[object]]) -> float:
    if not matrix:
        return math.nan
    return sum(1 for row in matrix if len(set(row)) == 1) / len(matrix)


def krippendorff_alpha_nominal(matrix: Sequence[Sequence[object]]) -> float:
    """Krippendorff's alpha with nominal disagreement and no missing ratings."""
    pooled: List[object] = []
    observed_num = 0.0
    observed_den = 0.0

    for row in matrix:
        vals = [v for v in row if v is not None and v != ""]
        m = len(vals)
        pooled.extend(vals)
        if m < 2:
            continue
        observed_den += m * (m - 1)
        for i, a in enumerate(vals):
            for j, b in enumerate(vals):
                if i != j and a != b:
                    observed_num += 1.0

    if observed_den == 0:
        return math.nan
    do = observed_num / observed_den

    counts = Counter(pooled)
    n = len(pooled)
    if n < 2:
        return math.nan
    expected_num = 0.0
    for a, ca in counts.items():
        for b, cb in counts.items():
            if a != b:
                expected_num += ca * cb
    de = expected_num / (n * (n - 1))
    return 1.0 - do / de if de > 0 else math.nan


def krippendorff_alpha_ordinal(
    matrix: Sequence[Sequence[int]], order: Sequence[int] = (0, 1, 2, 3)
) -> float:
    """Krippendorff's ordinal alpha using marginal-frequency ordinal distance."""
    pooled: List[int] = []
    for row in matrix:
        pooled.extend(int(v) for v in row if v is not None and v != "")

    counts = Counter(pooled)
    index = {category: i for i, category in enumerate(order)}

    def delta(a: int, b: int) -> float:
        if a == b:
            return 0.0
        ia, ib = sorted((index[a], index[b]))
        cumulative = sum(counts.get(order[j], 0) for j in range(ia, ib + 1))
        cumulative -= (counts.get(a, 0) + counts.get(b, 0)) / 2.0
        return cumulative * cumulative

    observed_num = 0.0
    observed_den = 0.0
    for row in matrix:
        vals = [int(v) for v in row if v is not None and v != ""]
        m = len(vals)
        if m < 2:
            continue
        observed_den += m * (m - 1)
        for i, a in enumerate(vals):
            for j, b in enumerate(vals):
                if i != j:
                    observed_num += delta(a, b)

    if observed_den == 0:
        return math.nan
    do = observed_num / observed_den

    n = len(pooled)
    if n < 2:
        return math.nan
    expected_num = 0.0
    for a, ca in counts.items():
        for b, cb in counts.items():
            if a != b:
                expected_num += ca * cb * delta(a, b)
    de = expected_num / (n * (n - 1))
    return 1.0 - do / de if de > 0 else math.nan


def pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def alpha_text(x: float) -> str:
    return f"{x:.6f}".rstrip("0").rstrip(".")


def build_matrix(case_ids: Iterable[str], raters: Sequence[Dict[str, Dict[str, str]]], field: str):
    return [[normalise_label(r[cid][field]) for r in raters] for cid in case_ids]


def compute_rows(raters: Sequence[Dict[str, Dict[str, str]]], case_ids: Sequence[str]):
    ambiguous = {
        cid for cid in case_ids if any(is_explicit_ambiguity(r[cid]) for r in raters)
    }
    non_ambiguous = [cid for cid in case_ids if cid not in ambiguous]
    ambiguous_ids = [cid for cid in case_ids if cid in ambiguous]

    majority_failure = [
        cid
        for cid in case_ids
        if sum(1 for r in raters if normalise_label(r[cid]["primary_label"]) != "NONE") >= 2
    ]
    majority_failure_non_amb = [cid for cid in majority_failure if cid not in ambiguous]

    rows = []

    def add_nominal(analysis: str, subset_name: str, ids: Sequence[str], field: str, transform=None, note=""):
        raw = build_matrix(ids, raters, field)
        matrix = [[transform(v) for v in row] for row in raw] if transform else raw
        rows.append({
            "analysis": analysis,
            "subset": subset_name,
            "N": len(ids),
            "exact_agreement": pct(exact_agreement(matrix)),
            "alpha": alpha_text(krippendorff_alpha_nominal(matrix)),
            "note": note,
        })

    add_nominal("Fine labels", "All cases", case_ids, "primary_label", note="Published reference estimate")
    add_nominal("Fine labels", "Non-ambiguous", non_ambiguous, "primary_label",
                note=f"Excludes {len(ambiguous)} cases with any explicit ambiguity flag")
    add_nominal("Families", "All cases", case_ids, "primary_label", transform=collapsed_family,
                note="Published reference estimate")
    add_nominal("Families", "Non-ambiguous", non_ambiguous, "primary_label", transform=collapsed_family,
                note=f"Excludes {len(ambiguous)} cases with any explicit ambiguity flag")
    add_nominal("Grounding boundary", "All cases", case_ids, "boundary_zone",
                note="Published reference estimate")
    add_nominal("Grounding boundary", "Non-ambiguous", non_ambiguous, "boundary_zone",
                note=f"Excludes {len(ambiguous)} cases with any explicit ambiguity flag")

    def add_severity(subset_name: str, ids: Sequence[str], note: str):
        matrix = [
            [int(float(r[cid]["severity_score"])) for r in raters]
            for cid in ids
        ]
        rows.append({
            "analysis": "Ordinal severity",
            "subset": subset_name,
            "N": len(ids),
            "exact_agreement": pct(exact_agreement(matrix)),
            "alpha": alpha_text(krippendorff_alpha_ordinal(matrix)),
            "note": note,
        })

    add_severity("All cases", case_ids, "Published reference estimate")
    add_severity("Non-ambiguous", non_ambiguous,
                 f"Excludes {len(ambiguous)} cases with any explicit ambiguity flag")
    add_severity("Explicitly ambiguous", ambiguous_ids, "Cases with any explicit ambiguity flag")
    add_severity("Majority-failure subset", majority_failure, "At least two non-NONE primary ratings")
    add_severity("Majority-failure excluding explicit ambiguity", majority_failure_non_amb,
                 "Majority-failure subset after excluding explicit ambiguity")

    return rows


def check_against_paper(rows: Sequence[Dict[str, object]]) -> None:
    for row in rows:
        key = (str(row["analysis"]), str(row["subset"]))
        if key not in PAPER_EXPECTED:
            continue
        exp_n, exp_exact, exp_alpha = PAPER_EXPECTED[key]
        obs_n = int(row["N"])
        obs_exact = float(str(row["exact_agreement"]).rstrip("%")) / 100.0
        obs_alpha = float(row["alpha"])
        if obs_n != exp_n or abs(obs_exact - exp_exact) > 0.0006 or abs(obs_alpha - exp_alpha) > 0.0000015:
            raise AssertionError(
                f"Frozen-paper check failed for {key}: "
                f"observed N={obs_n}, exact={obs_exact:.6f}, alpha={obs_alpha:.6f}; "
                f"expected N={exp_n}, exact≈{exp_exact:.3f}, alpha≈{exp_alpha:.6f}"
            )


def main() -> None:
    args = parse_args()
    raters = [read_annotation_csv(args.a1), read_annotation_csv(args.a2), read_annotation_csv(args.a3)]

    case_sets = [set(r) for r in raters]
    if not (case_sets[0] == case_sets[1] == case_sets[2]):
        raise ValueError("A1/A2/A3 case_id sets are not identical")
    case_ids = sorted(case_sets[0])
    if len(case_ids) != 720:
        raise ValueError(f"Expected 720 common cases; found {len(case_ids)}")

    rows = compute_rows(raters, case_ids)
    if not args.skip_paper_check:
        check_against_paper(rows)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["analysis", "subset", "N", "exact_agreement", "alpha", "note"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.out}")
    for row in rows:
        print(
            f"{row['analysis']}: {row['subset']} | N={row['N']} | "
            f"exact={row['exact_agreement']} | alpha={row['alpha']}"
        )


if __name__ == "__main__":
    main()
