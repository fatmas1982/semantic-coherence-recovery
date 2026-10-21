# E1/E2 historical-bootstrap forensic outcome and corrected S-E1E2 intervals (21 Oct 2026)

> **Decision: SCOPED REPRODUCIBLE POST-HOC CI SUPERSESSION. Not a 100-table or final-paper scientific certification.** The old 250-draw CI series is preserved as a historical, **not exactly re-reproduced**, output. The corrected author-facing Supplement Table S-E1E2 uses the clean-room-reproduced 3,000-draw paired E1/E2 computational bootstrap, without changing case denominators, decisions, macro-F1 point estimates or T4 QWK.

## Evidence and reproducibility findings

1. [Original 250-draw crosswalk](../results/validity_2026_10/SUPP_S_E1E2_250_VS_3000_EXACT_20_ROW_AUDIT_20261020.csv) records the **20/20** original E1/E2 table cases, changed counts/rates, and delta macro-F1 point estimates matching the 3,000-draw reanalysis, but most historical percentile CI endpoints differ.
2. [250-draw reanalysis CI run](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39459397262) **successfully executed**, but found matches to the historical table in only **5/20 changed-rate lower endpoints, 2/20 changed-rate upper endpoints, 1/20 delta-macro-F1 lower endpoints, and 4/20 delta-macro-F1 upper endpoints**. Successful execution is not a PASS of historical interval equivalence.
3. [3,000-draw independent clean-checkout run](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39481665207) reproduced **all 20 rows × 18 archived numerical fields** of [`E1E2_PAIRED_RECOMPUTED.csv`](../results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv), with **zero drift**. Its original Git blob SHA is `bb53ca9621c6b5c53b5ff5c31e4984f59990319b`.
4. A second archived file, [`E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv`](../data/validity_2026_10/E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv), has the same 20 delta macro-F1 point estimates but differing low and high endpoints in **all 20 pairs** versus the clean-room-reproduced 3,000-draw CSV. The maximum unrounded absolute endpoint difference found between these two 3,000-draw files was approximately **0.00336324**. Their exact historical code/data-order cause remains unresolved.
5. [Corrected public crosswalk](../results/validity_2026_10/S_E1E2_CORRECTED_CI_3000_20261021.csv) contains the old and corrected intervals for all 20 rows, with exact target/judge/variant keys. The [new clean-main CI verifier](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39597031663) concluded **PASS_SCOPED_20ROW_DISPLAY_CROSSWALK**: **68 of the 80 displayed CI endpoints changed, 0 of 20 delta-macro-F1 interval zero-inclusion statuses flipped**, and **20/20 displayed paired point-estimate/count checks passed**.
   
## Exact statistical scope

The selected bootstrap takes **3,000 resamples with replacement of complete Prompt_ID clusters** within each frozen judge×target×E1/E2 perturbation, seeded **20261009** in `code/validity/reanalyse_e1e2_pairs_2026.py`. It reports 2.5th and 97.5th percentiles of the resampled fraction of changed decoded decisions and of delta macro-F1, holding the archived baseline/perturbed predictions, case membership and labels fixed. These intervals **do not** account for re-generating outputs, retraining evaluation models, alternate frozen folds or external data validity. The 20 comparisons reuse cases/clusters and are exploratory; percentiles are not multiplicity-adjusted simultaneous intervals.

A nominally identical seed and replicate count alone **cannot certify** equality to a different historical interval file. The 250-draw original source implementation and its possible differing RNG stream/group ordering/software provenance have **not** been conclusively recovered or causally isolated. This record **does not claim** that changing the number of draws was the sole reason for differing CIs.

## Author-facing Word artifacts corrected (not yet in public GitHub)

The prior manuscript and supplement were updated in-place at their methodological/provenance paragraphs, rather than merely appending an unrelated note; the current S-E1E2 20-row table was revised.

| Author-facing artifact | SHA-256 | QA scope |
|---|---|---|
| `P2_MAIN_E1E2_CI_CORRECTED_20261021.docx` | `8ad4bbb1b7592b6c1e64ab47f0de111c43331d59fcdb6e1e889cd3b871433ea1` | 20/20 table cell strings unchanged; revised E1/E2 methods and inference qualification; 37 rendered pages |
| `P2_SUPPLEMENT_E1E2_CI_CORRECTED_20261021.docx` | `6d4cc0bb84295e5f3c82c4da80f8165dd7bed2963452a405bea7b41de2d97f46` | Table S-E1E2 CI display updated (20 rows); 79/79 other supplement table strings unchanged; 52 rendered pages |

The Word files and historical-versus-corrected CI crosswalk are author-facing local deliverables. They are **not deposited by this GitHub documentation commit**, and no coauthor/ethics/publication approval is presumed.

## Reviewer closure and open tasks

- **PASS (bounded):** current 3,000-draw paired reanalysis from the published case-level data, corrected 20-row CI display agreement, and unchanged 20 case/point-estimate/QWK values.
- **OPEN:** exact historical 250-draw source chain; explanation of alternate 3,000-draw CI lineage; all other tables beyond previously tested scoped values; full run-level/inner-CV checks and rights/coauthor approval.
- **Do not relabel older R14 16-table submission audit as validation of the current 20-main/80-supplement-table revision.**

**Verdict: SCOPED S-E1E2 CI CORRECTION RELEASE CANDIDATE; overall manuscript remains PARTIALLY VERIFIED / MAJOR REVISION.**
