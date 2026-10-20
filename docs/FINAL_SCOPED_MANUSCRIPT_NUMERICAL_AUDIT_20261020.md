# Final-scoped current manuscript numerical reconciliation — 20 October 2026

**Assessment: PARTIALLY VERIFIED / NOT SUBMISSION-FROZEN.** Scope is the author's 20 October `P2_MAIN_BRANCH_EVIDENCE_RECONCILED_20261020.docx` (SHA-256 `eaa9dcca8d7063a3e5de12b4c538925f0c98c58234d5057a29a46ca6b91ad4b2`) and companion `P2_SUPPLEMENT_BRANCH_EVIDENCE_RECONCILED_20261020.docx` (SHA-256 `9d7751c63702714f5214a671fb56480b8c4fd9d85443920780cec75ba23cdc57`). The corrected author-facing Word copies derived from them are not uploaded to `main` in this report.

## Exhaustive table inventory, not exhaustive scientific verification

The two 20 October candidate Word files contain **20 main / 80 supplement** tables, indexed by actual printed captions (not merely Word XML sequence). The complete [100-row current-scope table registry](FINAL_100_TABLE_SCOPED_VERIFICATION_MATRIX_20261020.csv) records:

- **5 tables** with scoped source-display matches: main Tables 10, 14, 17; supplement Tables S44C, S44E. The 60 matched values from main Tables 10/14/17 comprise selected summary values; CI resampling and every other table cell were not rerun.
- **3 tables** with archived export arithmetic/structure checks: S14B human pair reliability, S32A fold support, S37A task-stratified bootstrap.
- **1 table** with consistent 20/20 point estimates but unresolved historical confidence-interval lineage: Table S-E1E2.
- **91 tables** without a full current-version table-level numeric certification in this pass; many are conceptual/descriptive, so this is not a claim that 91 tables contain mistakes. An exact full-scope semantic, provenance and numerical audit remains needed.
- **0/100** tables received a *new complete source-to-every-cell numeric certification* from this audit. The already valid **scoped** source matches and CI runs must not be recharacterised as complete failure.

## Critical evidence — S-E1E2 20-row input-count/point-estimate comparison

From a direct case/metric comparison between the author candidate's **20 printed E1/E2 rows** and `results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv`, the **20/20** target denominators, number of changed decisions, changed percentages and delta macro-F1 point estimates match to the table's printed precision. Source CSV is the frozen-case-based 3,000-draw analysis and was re-executed successfully earlier in [GitHub Actions run 38612837716](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38612837716).

**Most historical confidence interval endpoints DO NOT MATCH the new 3,000-draw file at printed precision:**

| Table S-E1E2 interval field | Matches out of 20 using archived 3,000-draw source |
|---|---:|
| Changed-decision rate lower 95% endpoint | 2 |
| Changed-decision rate upper 95% endpoint | 4 |
| Delta macro-F1 lower 95% endpoint | 3 |
| Delta macro-F1 upper 95% endpoint | 3 |

[Exact comparison of all 20 rows](../results/validity_2026_10/SUPP_S_E1E2_250_VS_3000_EXACT_20_ROW_AUDIT_20261020.csv). The original author table labels its CI as **250 draws**, seed **20261009**, while the later full reproducibility run uses **3,000 draws** and the same recorded seed. Same seed does not render different replicate counts or code versions numerically identical.

To distinguish count-vs-implementation effects we **also ran** the later versioned case-paired analysis with **250** replicates, seed **20261009**, in clean GitHub Actions [run 39459397262](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39459397262). It completed successfully and checked the printed historical endpoints:

| Table S-E1E2 interval field | Matches out of 20 using newly executed 250-draw reanalysis |
|---|---:|
| Changed-decision rate lower | 5 |
| Changed-decision rate upper | 2 |
| Delta macro-F1 lower | 1 |
| Delta macro-F1 upper | 4 |

**Interpretive boundary:** Repeating the *later implementation* with 250 draws is not a reconstruction of the unknown historical 250-draw source implementation. The mismatch is **not proven to be caused solely by number of draws**; random-draw sequencing, bootstrap design/stratification, source implementation versions or runtime differences may also matter. **Do not silently replace** old endpoints or call the historic CI lineage verified. Original table values are preserved in the revised author copies, and the CI provenance exception is explicitly disclosed alongside them. To use a new set of 3,000-draw interval values as the journal reportable analysis, version and formally replace the old table after full cross-check and scientific sign-off.

## Additional editorial defect identified and repaired

The supplement's **80th Word table** (33 rows of archived M4 forced-choice reference Condition-C metrics by original generator stratum and M01 exclusion) was originally without a visible numbered table caption. The new author-facing candidate adds **Table S47**, with an explicit historical/partial-verification and noncausal interpretation boundary. Numeric table cells remain untouched. A manual page break that left most of the preceding page blank was removed in the revised copy. This is document-structure QA only, not a replay of the subgroup CIs.

The corrected author Word copies retain all **20 + 80 original table cell strings exactly**, and the new supplementary title does not imply causal generator preference.

## External audit status / governance

- Already passing executed checks: M3 dual OOF algebra (2,128 predictions), 60 GEE refits, 60 corrected HJI records, 20 E1/E2 paired results, and T1 FP16/E1 decisions. See `docs/BRANCH_REVIEW_STATISTICS_CONSOLIDATION_20261020.md`.
- Still unsettled: original 250-draw S-E1E2 CI lineage; all remaining full table source proofs; nested M3 inner-fold/train-dev-feature-fit test; failed attempt→success run genealogy where possible; approval for public sensitive archives; coauthor and journal final review.
- Independent external human validation remains prospective/deferred and must not be claimed completed.

**This report records manuscript author-copy inspection and newly executed CI on archived paired cases, not a fresh GPU inference or a human ethics authorization.**

## Delivered author-review DOCX candidate fingerprints (not deposited on GitHub)

The locally rendered/rechecked author-review copies resulting from this pass are:

| File | SHA-256 | Tables | Rendered pages |
|---|---|---:|---:|
| `P2_MAIN_NUMERICAL_RECONCILIATION_20261020.docx` | `19273cb00cfa90dff228ea7bf5484c1f09458a03d121bbdf5f25ca022f7dbb58` | 20 | 37 |
| `P2_SUPPLEMENT_NUMERICAL_RECONCILIATION_20261020.docx` | `06f8e7eb4afe948d730249ae9b62051b23452124871dc10a75774738b46245e3` | 80 | 51 |

The **exact cell text** of all 100 original tables was checked against the immediately preceding Word files and preserved. The supplemental Table S47 caption was added (not a data modification), and the manual page-break defect was corrected. The Word files are distributed as separate author-facing downloads in the working conversation and are **not** asserted to be stored in the public repository. The locally generated 100-row audit includes a SHA-256 of each source table's text; this GitHub registry is a reduced path/caption/status summary rather than the full local fingerprint ledger. The main/supplement were rendered; a professional independent editorial pass is not claimed.

