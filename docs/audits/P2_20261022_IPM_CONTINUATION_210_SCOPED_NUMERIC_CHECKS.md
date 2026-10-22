# IP&M review-candidate continuation — additional verified numeric displays and open gates

**22 October 2026. DECISION: 210/210 scoped numerical display/derived checks PASS; full 100-table source-to-every-cell certification remains OPEN. Manuscript is NOT submission-frozen.**

## Exact Word inputs
- Main `P2_IPM_MAIN_PEER_REVIEW_DRAFT_20261022.docx`, SHA-256 `9499084538694e81294b7b857459d6f92cf3ea27ca49a9f206c7bfe5c5d6be07`.
- Supplement `P2_IPM_SUPPLEMENT_PEER_REVIEW_DRAFT_20261022.docx`, SHA-256 `fc770d92c0d069211e571d7045bf54b185a17f0508049856b499066d9f545999`.
- Compared directly to the author-attestation-aligned predecessor: **20/20 Main and 80/80 Supplement table-cell text grids identical**. No scientific result changed by this audit.

## New independent source and arithmetic checks
**132/132 additional checks PASS**, based on user-supplied locked analysis bundles, not fresh model training:
- **104/104** comparisons: archived `P2_55_M4_FORCED_CHOICE_RESULTS(1).zip` `M4_FORCED_METRICS.csv`, `M4_FORCED_ABLATION_DELTAS.csv`, `M4_FORCED_VS_M3_PAIRED.csv`, against **Main Tables 14, 15; Supplement Tables 60, 63**, plus Supplement Table 61's four published discordant count sums and four **two-sided exact McNemar p-values** recomputed via the binomial distribution. Critical boundary: **the discordant counts themselves were not recounted from joined raw M3/M4 case predictions**, only the stated count arithmetic and exact p-values were checked.
- **28/28** comparisons: protocol-variant summaries in **Main Table 18**, using `P2_81_M4_PROTOCOL_SENSITIVITY_RESULTS(1).zip` for T1–T3 (4 variants per target) and `P2_84_M4_T4_COMPLETE_PERMUTATION_RESULTS(2).zip` for T4 (**12 complete permutations**, not superseded 6-variant intermediate). Checked P1 identity, P2 minus P1 identity, variant mean, SD, minimum, maximum and count.

Earlier author-side verification reproduced **72/72** M0–M2 displayed F1/CI values (Main Table 13 and Supplement Table 59) and **6/6** pre-resolution human multi-rater CIs (Supplement Table 30). **Cumulative enumerated 210/210 checks**, explicitly including duplicated display entries and arithmetic checks, not 210 independent observations or full table-cell validation.

## 100-table and privacy boundary
A row/column/cell manifest inventories **100/100** Word tables, **4,103 nonempty cells**. The 210 checks partially touch **9** table indices across both Word documents. The other **91** tables have not undergone new direct source-per-cell verification in this cumulative crosswalk, though some older scoped checks are recorded separately. Every checked table also has unverified content: **DO NOT SAY nine complete tables are source-verified**. The prior heuristic 100-table structural/syntax scan is not a replacement for scientific validation.

Current `main` tree contains **4,960** tracked files and **5,078** recursive tree entries (untruncated). This was a **filename/path metadata** review only, plus selected text/workflow/notebook reviews. No blanket code-secret, personal-data, licensing or full Git history scan is claimed. No directly stored DOCX comments/tracked revisions were found in current manuscript/supplement files, nor a direct personal GitHub/ORCID URL match in their text; this does not certify double-anonymity. One inspected notebook mentions an external server hostname; this is not itself proof of credential leakage.

## Human attestations and editorial gates
The corresponding author states rights to all relevant data/code/third-party materials, applicable ethics exemption, all coauthor approval and IP&M journal target. This is author-attested, not a fabricated ethics certificate. **Current manuscript lacks confirmed exact statements on competing interests, funding and CRediT;** the submitted file/version-specific author declaration, exact author contact/title page, current journal anonymity requirements and exclusive submission must be finalized. ScienceDirect's exact IP&M-specific Guide for Authors returned 403 during this audit; conditional Elsevier double-anonymized guidance is not proof that IP&M currently uses that route.

## Unclosed scientific gates
Complete 100-table source-to-every-cell validation; M3 nested feature-fit/train-dev lineage; original historical M0–M2 trainer limitations; full judge inference replay; raw case-based McNemar discordant recount; complete server retry/lineage; rare-event GEE sensitivity; entire public repository content privacy scan; current-HEAD fresh CI and archive/install verification; exact-version coauthor final signoff. No release DOI, final tag or IP&M submission was made.

**Safest release label:** `REVIEW_DRAFT_SCOPED_VALIDATION_20261022` — NOT `100_PERCENT_FINAL`.
