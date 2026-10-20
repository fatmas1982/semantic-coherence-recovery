# Reviewer closure evidence — 19 October 2026

**Status: open / not final PASS.** This supplement to the consolidated ledger is limited to **source inspection and evidence indexing**. It does **not** independently recalculate all tables in the two 2026-10-17 DOCX manuscripts.

## Source-file audit
- Author-provided main DOCX: 20 tables; supplement DOCX: 80 tables.
- 100 tables have been extracted for table-level reconciliation, with 4,103 nonempty cells logged in the local downloadable package.
- The SHA-256 of each attached DOCX and each of eight locally available prior validation ZIPs is recorded in the downloadable package accompanying this audit (not yet uploaded here).
- 23 distinct experiment/reviewer concern families were indexed in the accompanying `REVIEWER_FAMILY_STATUS_20261019.csv`.

## Model-engineering review closure
The reviewer-raised concerns about data splits, generator shortcuts, size-matched controls, input/prompt provenance, completeness, source hashes, GPU exceptions, missingness, OOF contract compliance, rare-event inference, M4 FP16 reference vs E1/E2 controls and reproducible code are reflected in the index. **Exact original reviewer ZIP output and code-change crosswalk are not independently confirmed** by this present pass; an unverified row must not be presented as complete.

## Paper/supplement boundaries
The main article and supplement retain explicit post-hoc design status and do not claim architectural ranking, external semantic validity or causal generator-specific effects. The final table-by-table numeric claim audit is still open; do not automatically replace historical reference metrics with dual-blocking or FP16 later-run estimates.

## Required release evidence
A complete closure requires a public reproducible script, exact source/input/target/protocol keys, case-level outputs, independent metric recomputation, CI/test audit where applicable, versioned hashes, and a table+paragraph-location bridge to the author DOCX. A prior archive or earlier assistant summary alone is not a full reproduction.

**Original result files and manuscript binaries were not modified. No approval/ethics/publication-final claim is made.**
