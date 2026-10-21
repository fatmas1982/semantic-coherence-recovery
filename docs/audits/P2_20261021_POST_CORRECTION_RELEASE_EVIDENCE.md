# P2 post-correction evidence consolidation — 21 October 2026

Status: **SCOPED VERIFIED / NOT SUBMISSION-FROZEN**. This entry consolidates author-side verification; it is NOT a new training run, a blanket 100-table numerical certification, or an assertion of ethical/data-release clearance.

## E1/E2 current reportable statistical protocol
The **current 20 E1/E2 perturbation contrasts** report 95% percentile confidence intervals from **3,000 paired Prompt_ID-cluster bootstrap draws**, seed **20261009**, conditional on archived paired predictions, using `results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv`. Source: `docs/E1E2_BOOTSTRAP_FORENSIC_AND_TABLE_CORRECTION_20261021.md`. Historical **250-draw CI endpoints are superseded**, retained strictly in the retrospective crosswalk, not reportable. A separate historical 3,000-draw endpoint lineage differed slightly and is not silently merged. Independent clean-room numerical checks and the corrected display crosswalk are previously archived: 20/20 source comparisons; 68/80 displayed CI endpoints changed; zero of 20 delta-macro-F1 CI zero-inclusion statuses changed. Intervals are descriptive, not multiplicity-adjusted simultaneous coverage and do not incorporate new judge inference or training.

## Latest author DOCX copies (author artifacts, NOT deposited here)
Both October 21 E1/E2-corrected Word files were revised to add an explicit current-protocol paragraph, retaining all original 20 main and 80 supplement scientific table-cell strings. Their author-side SHA-256 hashes:
- Main `P2_MAIN_E1E2_3000_REPORTING_CONFIRMED_20261021.docx`: `31e811aafe1515318c30a7646ee30e4ad04ff0b5b3462e5179567674d2422a98`;
- Supplement `P2_SUPPLEMENT_E1E2_3000_REPORTING_CONFIRMED_20261021.docx`: `3c2b96633132d2d14d5c7175098bde38b1ca87cc27df1a176b8969701c15beb4`.
Other 2,000-draw bootstrap descriptions remain intentionally unchanged because they concern different estimands. The author binaries were NOT put on this public branch.

## M3 review scope
The supplied `IPM_M3_GITHUB_PUBLICATION_20261015(1).zip` carries 24 complete case-level OOF exports (four dual plus 20 size-matched). Direct case-level macro-F1 recomputation and a 720 fold×generator cell ledger crosscheck were reported as PASS. The four authoritative M3 dual macro-F1 values are 0.5913225257153932, 0.671147712324077, 0.68183570135006, 0.5732726099821898. These reproduce *archived scoring and test split accounting*, not historical inner train/dev/feature-fit execution. The distinct `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(4).zip` is a partial historical run and must not replace source lineage `(2).zip` (SHA256 `55b879ce51470d6c79933f3f32cc46e1bb4e28bc69693ea8b43ed9514adb2e96`).

## Reviewer/table release gates
23 reviewer families inventoried; 100 tables indexed (20 main, 80 supplement). Selected already-executed scoped checks remain valid, but **no complete source-to-every-cell 100-table certification has been claimed**. Historical inner-CV execution, full table-level numerical source links, version-linked failed-to-success run genealogy, independent human validation (deferred), coauthor approval, and publication/data-governance checks remain open.

## Publishing boundary
Only this de-identified, evidence-level textual consolidation is deposited here. Historical raw prompt/output collections, reviewer notes, server archives, and binary DOCX/ZIP audits were intentionally not bulk-published without privacy, rights, and duplication inspection.

**Decision:** Retain verified 3,000-draw E1/E2 current intervals; preserve historic 250-draw lineage as a disclosed superseded record. No unverified manuscript-wide PASS.
