# Research Governance Release Candidate | 2026-10-12

Status: DRAFT, INDEPENDENTLY VERIFIED ONLY FOR SPECIFIED MODULES. Coauthor and institutional publication approval pending.

## Chronology and immutable-source boundary
1. The original 120 purposive prompt groups, six chosen checkpoints and 720 saved generations are the frozen elicitation source; five historical checkpoint inference processes cannot be bit-replayed.
2. A1-A3 contributed 2160 pre-resolution ratings; 423 cases received A4 round-1 adjudication, 29 a targeted same-senior re-review, and four case-level clerical normalizations; FINAL GOLD v1.0 remains authoritative.
3. Later theory-linked discourse examples and reference v1.3 publication-mapping wording are post-study documentary interpretation; they are not an independently validated replacement for GOLD v1.0.
4. Later M3 dual/size-matched server protocol was executed in 24 nested GPU runs, including all four dual held-out OOF case sets; earlier September M3 blocked figures are superseded for the current manuscript.
5. E1/E2 judge format perturbations and 60 human-judge comparisons are post-hoc; corrected RD bootstrap endpoints are versioned to PCG64 seed 20261010, 2500 Prompt_ID-cluster draws; GEE precision diagnostics analyse the same tests and do not add tests.

## Passed numerical checks (frozen predictions, not historical model reruns)
- GEE 60 robust precision job passed: https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38251424670
- HJI corrected 60-bootstrap CI and M3 dual 4-target case-level job passed: https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38285305872
- M3 case-level macro-F1: 0.591322526 / 0.671147712 / 0.681835701 / 0.573272610 for T1–T4, on 720/474/460/474 cases.
- Nested M3 parent GPU archive SHA256: 55b879ce51470d6c79933f3f32cc46e1bb4e28bc69693ea8b43ed9514adb2e96.
- Historical 86-fragment base transport SHA256: 69ce2a52c201424d8939d1a997dc3bd34854a2822131c6bc69a791b47635ce3e (does not cover later changes).

## Current claim-to-artifact and manuscript binding
- Current corrected 33-row experiment matrix: docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv.
- 100-table inventory: docs/MAIN_SUPPLEMENT_100_TABLE_INVENTORY_20261012.csv, containing exactly Main Tables 1–18 and Supplement S1–S82, with separate verification scopes.
- Main revised Word SHA256: c921de31a3dc56d946f137b795d4ecee04ad7977f3cb711cf1725fbdfe1802ce.
- Supplement revised Word SHA256: a0fedb866af27c7edce78fe9cb1f4f1ddca4cf99f18317a233b663d5139cb4c2.
- These revised Word files are controlled review artifacts and are NOT claimed to be deposited on the publicly named GitHub branch.

## Outstanding approval and governance conditions
- Comprehensive free-text note/comment privacy audit and contributor redistribution rights review were not completed. New reconciled M3 OOF CSV has no raw free text or annotation notes; this does NOT certify earlier historical public sheets.
- The institutional ethics policy/determination document was not supplied; no exemption number is invented.
- The six coauthors' approvals of exact text, CRediT roles and unrestricted distribution were not independently verified; private unsigned checklist prepared.
- The journal-specific peer-review model and whether masked reviewer access is necessary must be confirmed. A named public repo is not anonymous.
- FP16 original T1 reference versus paired E1/rot0 input-SHA mismatch persists with unknown unique cause; protocols remain separate.
- No frozen final article DOI, author-approved immutable release tag or merged PR is asserted. PR #2 stays DRAFT.

See docs/M3_DUAL_VERSION_RECONCILIATION_20261012.md and docs/RESEARCH_GOVERNANCE_17_ISSUE_CLOSURE_MATRIX_20261012.csv.
