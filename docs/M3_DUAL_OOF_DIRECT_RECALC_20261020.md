# Direct M3 dual-block OOF recalculation — 20 October 2026

The four archived M3 dual-block `macro-F1` values were independently recomputed directly from the **case-level** `results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_OOF_ALL.csv` and compared against the separate published `P2_81_M3_DUAL_BLOCKED_SUMMARY.csv`.

| Target | Cases | Prompt clusters | Cross-fold prompt overlap | Recalculated macro-F1 | Absolute delta |
|---|---:|---:|---:|---:|---:|
| T1 | 720 | 120 | 0 | 0.5913225257153932 | 0 |
| T2 | 474 | 120 | 0 | 0.671147712324077 | 0 |
| T3 | 460 | 120 | 0 | 0.68183570135006 | 0 |
| T4 | 474 | 120 | 0 | 0.5732726099821898 | 0 |

No duplicate Case_ID was found within any target, and no same Prompt_ID was assigned to more than one **reported test fold** for a target. This verifies frozen OOF case linkage and metric algebra, **not** internal train/dev separation, absence of feature-fit leakage, nested epoch selection, original GPU execution, or raw-run retry provenance.

**Sources:** `results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_OOF_ALL.csv`; `results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_SUMMARY.csv`.

**Code:** `code/analysis/verify_m3_dual_oof_20261020.py`.

**Executed output:** `results/validity_2026_10/M3_DUAL_OOF_INDEPENDENT_RECALC_20261020.csv` (computed directly from repository file contents).

The manuscript plus supplement **100 scientific tables** have still *not* undergone full numeral-by-numeral source checks. This independent confirmation concerns only four M3 dual-block summary point estimates. The broader decision remains MAJOR REVISION / PARTIAL VERIFICATION. External independent human validation remains deferred.
