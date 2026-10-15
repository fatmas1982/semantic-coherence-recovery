# Submission-repository evidence gate — 15 October 2026

**Scope:** GitHub repository `fatmas1982/semantic-coherence-recovery` at commit `1411e7d55567b327be7a25a4b1f3776a4c1dc974`. This gate **excludes publishing the latest Q1-reviewed manuscript and supplement**, as explicitly requested by the author.

## What has been verified independently against GitHub's remote tree
- Exactly **24** historical M3 OOF CSV paths are present (four targets × one dual-blocked and five size-matched runs).
- The M3 120-fold ledger, 720 generator/fold ledger, archived-source manifest, and dual summary are present.
- The M3 worker, frozen GOLD pickle, configuration and metadata, plus the two previously uploaded (not latest Q1-reviewed) Word files are present.
- The release manifest lists 34 files. All listed paths exist; the recorded **byte counts match for 32/34 files**, while `RUN_CONFIG.json` and `SNAPSHOT.json` each differ by **one byte** from the release manifest. This is a real provenance-integrity mismatch and must not be silently ignored. Hash verification of every remote file has **not** been completed here.
- The 120-row fold summary writes a `CONFLICT:[...]` sentinel for the selected-epoch field in **all 120 records**. This reflects multiple generator-stratum values and is not a unique epoch per fold. Use the detailed 720-row generator/fold ledger for stratum-specific values; do not parse `CONFLICT` as an epoch or declare a single uniform epoch.
- Existing verification reports show near-exact GEE coefficient/p-value replay for 60 models. This does not make every reported manuscript table cell independently verified.

## Open submission gates
1. **P0:** Run `python scripts/audit_m3_release_readonly.py` on a clean checkout. Resolve both configuration-manifest byte/SHA mismatches using the actually released bytes, with the changes recorded. Do not alter frozen results.
2. **P0:** Use the 720-row stratum-scoped ledger when reporting chosen epochs. Describe the 120-row summary's `CONFLICT` values explicitly rather than treating them as incomplete training runs.
3. **P0:** Build a source-to-table claim map for every material quantitative result in the **latest manuscript**. The prior 288-item heuristic claim inventory has **194 marked SOURCE_MAPPING_REQUIRED** and 94 with only an explicit table/figure pointer, not a cell-level replay. The heuristic inventory is a worklist, not evidence that claims are wrong.
4. **P1:** Assess all archived inputs/outputs/code against a tested clean-run recipe, retaining historical rerun limitations.
5. **P1:** Keep code/data availability declarations scoped to the archived components, and do not claim external construct validity or external generalisation.

## Release verdict
**M3 files: present. Complete reproducibility and final submission provenance: NOT YET VERIFIED.** No new experiments, new source data or manuscript/supplement upload occurred as part of this gate. This gate is not a substitute for an independent scientific review.
