# E1/E2 forensic bootstrap audit and explicit confidence-interval correction (20 October 2026)

**Disposition: corrected, clean-room-reproducible 3,000-resample uncertainty lineage selected for the revised AUTHOR DOCX; old intervals preserved, historical root cause not fully demonstrated. The rest of the paper is NOT certified for submission.**

## What actually failed to reproduce

The frozen historical Supplement **Table S-E1E2** has 20 paired comparisons of judge perturbations (Qwen/Mistral × T1–T4 × E1/E2 rotations). Its previous presentation described 250 paired `Prompt_ID`-cluster bootstrap draws, seed `20261009`. The 20 case denominators, 20 changed-decision counts, changed-decision rates, and point `Δmacro-F1` all agree with the archived case-level recomputation.

Merely reusing the seed and reducing `--bootstrap-reps` to 250 on the **later** `code/validity/reanalyse_e1e2_pairs_2026.py` implementation did *not* reproduce the old percentile CIs. The [successful 250-draw forensic CI](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39459397262) yielded exact printed-endpoint coincidences (out of 20) of:

| Historical CI bound | Matches using later 250-draw implementation |
|---|---:|
| Change-rate CI lower | 5/20 |
| Change-rate CI upper | 2/20 |
| Δmacro-F1 CI lower | 1/20 |
| Δmacro-F1 CI upper | 4/20 |

These are **matching endpoint counts, not validation failures of the resampling design**. The original 250-draw historical RNG/resampling implementation has **not** been independently recovered and proven bit-equivalent. It would be scientifically invalid to claim that the discrepancy was caused solely by the number of draws.

A second, **separate 3,000-draw CSV** also exists: `data/validity_2026_10/E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv`. Comparing this to the independently executable `results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv`, 20/20 point estimates matched exactly but **20/20 contrasts had differing Δmacro-F1 CI endpoints**, with maximum absolute endpoint difference **0.00336324195174241**. Identical recorded seed and sample size are not sufficient evidence of an identical random resample sequence or inference implementation. The exact historical difference in code/order/seed-state is *unresolved*.

## Clean-room confirmation of chosen corrected lineage

On [GitHub Actions run 39481665207](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39481665207), a fresh Python 3.12 environment executed:
`python code/validity/reanalyse_e1e2_pairs_2026.py --data-dir data/validity_2026_10 --out /tmp/e1e2_3000_clean --bootstrap-reps 3000 --seed 20261009`.

The separately versioned verification `code/analysis/verify_e1e2_3000_reanalysis_20261020.py` compared **18 numerical fields × 20 complete contrasts** to the previously published archived output `results/validity_2026_10/E1E2_PAIRED_RECOMPUTED.csv` (Git blob SHA `bb53ca9621c6b5c53b5ff5c31e4984f59990319b`) and reported **PASS: 20/20 exact comparisons within 1e-12; 0 drift fields**. The [output artifact](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39481665207) preserves this clean-run status. No model/LLM was called and no historical source table was overwritten by the workflow.

This demonstrates exact replay of the **declared, deposited** 3,000-draw resampling implementation on frozen predictions. It does *not* prove the historical 250-draw RNG provenance nor provide independent validation of frequentist coverage or cross-domain validity.

## Manuscript correction decision

An explicitly versioned **author-facing main and supplement Word revision** was made. The previous 250-draw S-E1E2 CI bounds were **replaced openly with the reproducible 3,000-draw bounds**, while retaining the old bounds in a row-level change record and preserving all other frozen experimental results. The authors' old files were not modified in place.

[20-row machine-readable before/after CI ledger](../results/validity_2026_10/E1E2_20_ROW_250_TO_VERIFIED_3000_CORRECTION_20261020.csv), derived from the original manuscript crosswalk and the verified 3,000-draw CSV. All 20 original numerator/denominator and point Δmacro-F1 values remain; the corrected CI bounds are rounded only for the **published display**. **0/20 comparisons changed whether the reported Δmacro-F1 percentile interval excludes zero.** Thus the observed interval-zero-exclusion pattern is stable, though inference is exploratory, conditional on archived case-level predictions, and not multiplicity-adjusted.

**Word editing / QA:** main manuscript 20/20 table-cell texts unchanged; supplement **79/80** tables unchanged and **one** original 21-row table (S-E1E2) deliberately corrected in its CI columns for the 20 data rows. The 20 E1/E2 point estimates and all QWK values in that table are preserved. Main and Supplement rendered as **37** and **52** pages, respectively, with the modified table spread over supplement pages 39–41 and visually inspected.

| Author-facing artifact (not committed to main) | SHA-256 |
|---|---|
| `P2_MAIN_E1E2_BOOTSTRAP_REANALYSIS_3000_REVISED_20261020.docx` | `6919d8b9f61f41b473c6dcd5f437100ee46458fef940240a6b32da369d5038fb` |
| `P2_SUPPLEMENT_E1E2_BOOTSTRAP_REANALYSIS_3000_REVISED_20261020.docx` | `b62aa7c55100f1ab40145819b299e5c7631a3f53d4a84ecb4151246e57395443` |

The original 250-draw S-E1E2 table text remains recoverable from the previous revision and the comprehensive before/after ledgers; the word-file SHA values permit unambiguous author review. **These binary Word copies are local artifacts and have not been deposited to the public GitHub `main` by this report.**

## Protocol and statistical qualifications

- Source: `data/validity_2026_10/paired_cases_part_01..11.csv` (10,408 overlapping comparison rows; not 10,408 independent observations), 20 paired contrasts, 120 `Prompt_ID` clusters per target, sample full clusters with replacement.
- Resampling: independent pseudo-random generator reset *per contrast* via `np.random.default_rng(20261009)`; `np.quantile(..., .025/.975)` percentile bounds; the code's declared grouping and scoring are documented in `code/validity/reanalyse_e1e2_pairs_2026.py`. A separate file may use a different random stream or order.
- Revisions were **post-hoc corrections** and should not be relabeled preregistered, confirmatory, architecture-ranking, or causal tokenizer analyses.
- Existing M4 FP16-reference-vs-E1/rot0 T1 prompt-newline audit remains a separate provenance question. The corrected E1/E2 reanalysis uses **E1/rot0 as its internal paired control**, not the original byte-distinct FP16 Table 17 reference.
- Not implied by this audit: validity of *all* 100 tables, exact historical model inference, model-selection/leakage closure, rare-event GEE bias correction, or approval to publish human-level data.

**Release gate:** E1/E2 interval lineage now reproducible in the stated corrected form and the old unresolved 250-run provenance explicitly disclosed; all other study-level reviewer/publication gates remain evaluated separately. **Not submission-ready as a whole.**
