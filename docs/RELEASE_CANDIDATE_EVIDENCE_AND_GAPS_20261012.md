# Research release-candidate: reproducibility evidence and exact remaining scope (2026-10-12)

**GOVERNANCE STATUS: NOT A 100% CERTIFIED FINAL RELEASE; DRAFT BRANCH.** This document is a controlled verification ledger, not proof of coauthor approval or institutional ethics clearance.

## Clean-room checks directly observed
- Frozen transport: all 86 ordered Base64 fragments decode to the expected SHA-256 tarball; all 151 file paths in the original frozen-file SHA256 manifest match when checked *inside the immutable staging copy*.
- Safe unpack: current checkout files with newer versions remain unchanged; historical versions stay in `.frozen_reference_2026/`, and `UNPACK_PROVENANCE_REPORT.json` identifies any name collision.
- Frozen human corpus: 720 raw outputs agree by Case_ID with the 720-row canonical reference; 120 Prompt_ID clusters, six outputs per cluster. A1/A2/A3 each contain 720 historical annotations; long pre-resolution ratings contain 2160 records, three per case.
- Archived computational OOF: all four target populations have unique matched Case_ID and y_true across M0/M1/M2 baseline OOF, 12 main M3 A/B/C OOF, 8 additional M3 C stability-seed OOF and 12 M4 A/B/C OOF.
- Frozen public primary metrics re-computed from archived case predictions; original model training/re-generation not repeated.
- M3 dual-blocking archive: 2128 held-out case decisions for four target populations and archived 24 nested dual/size-matched run hashes. The **size-matched 20 run-level OOF CSVs are retained in the local source nested GPU ZIP, not in this public GitHub branch**.
- E1/E2 human-judge: 10408 overlapping paired case-comparison rows in 11 CSV parts; 20 comparisons, 60 axis-specific HJI contrasts. Clean CI executes all corrected PCG64/2500-draw intervals. Separate clean CI refits all 60 GEE contrast precision diagnostics.
- Experiment matrix: 33 claims, with original paper-to-table links and 34 referenced code locations inspected. A path-existence audit is not an all-stage experiment rerun.

## Known unavailable or not independently certified items
1. The original historical GOLD/CPU-baseline XLSX binaries, original annotation manual PDF, and targeted rereview source XLSX are listed by source SHA256 but are **not bundled as original binaries** within the 151-file public transport. Their CSV/text derivatives support archived numerical checks; the original-binary hash check is not independently executable without those source files. Avoid any claim that these original binaries can be downloaded in the public archive.
2. The original CPU M0–M2 trainer and exact revisions/serialization/stopping history for five generation checkpoints were not retained; reconstructive reruns do not establish bit-identical historical execution.
3. M3 leave-one-task-out per-case OOF and several exploratory outputs are released as summary diagnostics or limited subsamples; existence of a table is not evidence of access to every original test-level log and raw output.
4. The archived 24-run M3 size-matched case files have been extracted locally for authorized coauthor audit, but have not all been deposited under the GitHub branch; current public M3 dual OOF and summary cover the dual held-out cells.
5. FP16 original T1 reference inputs and paired E1/rot0 inputs differ in recorded hashes; precise serialization root cause remains unidentified; both variants must retain separate protocol labels.
6. Historical annotation free-text privacy and rights redistribution, coauthor CRediT/signoffs, ethics policy/determination and journal-specific blind-review requirements remain subject to human verification. A regex privacy preflight is **not** a replacement for legal/privacy review.
7. There has been no single full end-to-end clean-GPU execution of all historical M0–M4 training, judge inference, sensitivity analyses and paper/appendix statistical outputs. Successfully passing selected archived-output gates is not equivalent to that claim.

## Authoritative resources
- Current 33-row experiment claim mapping: `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv`.
- Current paper caption inventory: `docs/MAIN_SUPPLEMENT_100_TABLE_INVENTORY_20261012.csv`.
- M3 numeric lineage and source hashes: `docs/M3_DUAL_VERSION_RECONCILIATION_20261012.md`.
- 17-issue governance state: `docs/RESEARCH_GOVERNANCE_17_ISSUE_CLOSURE_MATRIX_20261012.csv`.
- Source-binary presence clarification: `SOURCE_BINARY_HASHES.csv`.
- Current release candidate source/Word hashes: `docs/SUBMISSION_CANDIDATE_SHA256_20261012.md`.
- CI: [frozen-base archive integrity](https://github.com/fatmas1982/semantic-coherence-recovery/actions/workflows/base-release-clean-room.yml), [all GEE stability fits](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38251424670), [M3 & corrected HJI 60 intervals](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38285305872).

**Publication gate:** Do not merge, label `final/fully verified`, create an immutable journal release DOI, or declare unrestricted annotation permissions until the outstanding items are resolved or explicitly documented as permanent, accepted limitations and the authorized coauthors approve the deposit.
