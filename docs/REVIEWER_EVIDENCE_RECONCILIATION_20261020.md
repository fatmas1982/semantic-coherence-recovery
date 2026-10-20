# 20 October 2026 — Reviewer evidence reconciliation (limited scope)

**Verdict: MAJOR REVISION / NOT FINAL PASS.**

The author-provided packages `P2_REVIEWER_CLOSURE_EVIDENCE_PACKAGE_20261019(2).zip` and `P2_RUN_PROVENANCE_MANUSCRIPT_RECONCILIATION(2).zip` were examined and both passed ZIP CRC. No model inference or retraining was conducted.

- Closure package: **100 manuscript/supplement tables (20 main, 80 supplement)** indexed; 4,103 populated cells extracted; **100/100 numerically UNVERIFIED**, not 100 validated; 23 reviewer-family issue rows.
- Run-reconciliation package: **56/56** server OOF inventory records in status `DATA_PASS_PROTOCOL_UNVERIFIED`. This means matching case ID, labels and valid predictions under this audit, **not** validated training or scoring protocols.
- **32** claim-to-artifact traceability candidates were recorded; manuscript-specific exact numerical matches remain `MANUSCRIPT_VALUES_NOT_SUPPLIED` in this package.
- **7** error-bearing logs with **22** error-pattern lines were reported; absence of a matching retry-to-success chain leaves recovery `UNVERIFIED_NO_PROVEN_ATTEMPT_TO_SUCCESS_LINK`.
- These diagnostics do not settle FP16 T1 baseline input-hash discrepancies, M3 nested model-selection leakage, E1/E2 permutation fidelity, clustered bootstrap or all 60 GEE refits. These gates remain OPEN.
- Existing authoritative historical experiments are not silently replaced with different October profiles or reconstructed baselines.
- Full personal-data release rights, ethics approvals and coauthor publication permissions require separate verification. External independent human validation remains deferred.

## Manuscript edit

Author-facing bounded evidence addenda were inserted into copies of the latest locally available `P2_MAIN_LLM_JUDGE_PROTOCOL_REVISED_20261017.docx` and companion supplement. Main 20 and supplement 80 numerical tables were preserved, without modifying results. Those Word copies were **not uploaded to main in this commit**; no claim that main now includes them. They must be reviewed and uploaded separately.

## Required follow-up

1. Recompute every reportable numerical table from exactly matching frozen case-level outputs and verify the reported input condition, model, target universe, seed and version.
2. Independently test nested fold train/dev/test separation and preprocessing fit boundaries, E1/E2 label-code inverse mapping, and all invalid/missing outcome handling.
3. Match every error log to a corresponding failed attempt and eventual terminal successful retry, where supported.
4. Refit confidence intervals and GEE models from raw paired data with pre/post-hoc boundaries and multiplicity families.
5. Reconcile manuscript, supplement, reviewer closure matrix and repository release notes without declaring a complete publication freeze beforehand.
