# Repository submission evidence gate — 15 October 2026

**Scope:** public repository `fatmas1982/semantic-coherence-recovery`. **Latest Q1-reviewed manuscript and supplement were intentionally NOT uploaded**, by author's explicit instruction.

## Verified repository content
- The 24 historical M3 OOF CSV files are present, together with the 120-fold, 720 generator/fold, dual summary, source manifest, M3 worker, run configuration and GOLD pickle.
- The original release manifest lists 34 file paths. It matched 32/34 uploaded byte counts; the other two files were previously uploaded with a final newline that the original source archive lacked.
- **Correction applied:** `RELEASE_SHA256_MANIFEST.csv` now records the actual published byte counts and SHA-256 hashes for `RUN_CONFIG.json` (309 bytes, `250ff840e2a6a4298050dd19c63ba5bb756c8ce8c5e37cae32d42aade0271cd8`) and `SNAPSHOT.json` (432 bytes, `c2bb606c3d71ba6b282be6de4e7704463b737d824ddcd989f1e5fd6fb9f813d9`). This reconciles the manifest to published bytes; it does **not** alter frozen experimental data. The other 32 entries have not been independently downloaded from the public remote and SHA-replayed in this review.
- The 120-row fold ledger records `CONFLICT:[...]` for `selected_epochs` in all 120 rows. These are **multi-valued generator-specific epochs**, not evidence of failed training. The 720-row generator/fold ledger is the correct source of stratum-specific epochs.
- A read-only repository checker is published at `scripts/audit_m3_release_readonly.py`. Run it after a fresh checkout to validate 34 SHA-256 digests and row/file cardinalities.

## Still-open submission conditions
1. Run the new checker in a clean checkout and archive its output. Publishing the checker does **not** mean it has been executed against the remote checkout.
2. Reconcile the latest manuscript's material quantitative claims with source-level results and aggregation code. The previous heuristic ledger of 288 paragraphs contains 194 `SOURCE_MAPPING_REQUIRED` statuses and 94 with cross-references only. These are **not** proven numerical errors.
3. Do not collapse generator-dependent `selected_epochs` into a misleading single fold value.
4. Maintain qualified statements about M0–M4 fresh retraining, external validity, GOLD-conditioned targets and construct validity.
5. Do not describe the repository's two older `EXISTING_EVIDENCE_ONLY` Word files as the newest Q1-reviewed manuscript and supplement.

## Conclusion
**M3 release publication verified; manifest byte discrepancy repaired; comprehensive independent replay, full source-to-table mapping, and final Q1 readiness remain OPEN.** This record does not claim new experiments or datasets.
