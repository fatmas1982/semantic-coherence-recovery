# Targeted manuscript-to-source audit — 20 October 2026

## Scope and direct outcome
Using the manuscript whose SHA-256 is `572d8d80f33c177650747515fafd678202571a44e95b273985d6a45a7d620389`, the paper's **Table 10 (10 selected displayed point estimates), Table 14 (24 dual and matched-control values), and Table 17 (26 FP16 values, including archived bootstrap interval endpoints)** were checked against matching source CSVs **directly fetched from this repository**. **60/60 selected printed numbers matched the archived sources at 3-decimal display precision; 0 displayed-value mismatches.** Table 14 M1 matched-control mean and sample SD were newly computed from five archived summary entries in `CPU_summary/ALL_METRICS.csv`. Other quantities were compared to existing calculated outputs.

**This is not validation of the underlying CI resampling or training protocol.** It is neither 60 new independent experiments nor validation of all 100 tables. The table population in the closure inventory remains **20 main / 80 supplement**; most entries and all full table source-to-data certifications remain open.

## Verifiable files
- Executed 60-row source-to-paper comparison: `results/validity_2026_10/MAIN_TABLES_10_14_17_MANUSCRIPT_SOURCE_AUDIT_20261020.csv`.
- Table 17 source-only audit (same FP16 values separately): `results/validity_2026_10/MAIN_TABLE17_FP16_SOURCE_MATCH_20261020.csv`.
- Reproducer: `python code/analysis/audit_tables_10_14_17_20261020.py --out output_dir`. Pass `--main-docx path/to/word.docx` to require the exact reviewed author-copy SHA, which is either the source revision above or the post-addendum revision `c3bb4d3e021cf78cc8980b821a8bf59bd69d6e844c9ba3074b63930339d0fa28`. Both Word author copies are **local release candidates, not deposited by this markdown commit**.
- Sources: `PUBLIC_METRICS_RECOMPUTED.csv`; `results/server_runs/SERVER_RUN_20261007_A/EXPORTS/CPU_summary/ALL_METRICS.csv`; `results/validity/m3_dual_block/P2_81_M3_DUAL_BLOCKED_SUMMARY.csv`; the eight `M4_{qwen,mistral}_fp16_offload_T{1..4}_C/METRICS_AND_CLUSTER_CI.csv` files under `results/server_runs/SERVER_RUN_20261007_A/EXPORTS/experiments/`.
- Grounding of Table 14 M3 dual point estimates additionally supported by case-level independent OOF recomputation `results/validity_2026_10/M3_DUAL_OOF_INDEPENDENT_RECALC_20261020.csv`.

## T1 FP16 reference is not input-equivalent to E1/rot0: input formatting identified; model-decision causality open

The separate deposited `data/validity_2026_10/FP16_BASELINE_INPUT_HASH_COMPARISON.csv` shows this exact discrepancy:

| Judge | FP16 original T1 macro-F1 | E1/rot0 T1 macro-F1 | Changed predictions | Different input hashes | Different token counts |
|---|---:|---:|---:|---:|---:|
| Qwen FP16 | 0.7679227037948411 | 0.7707529147241724 | 4 / 720 | 720 / 720 | 0 / 720 |
| Mistral FP16 | 0.4440087005037559 | 0.4276082638141963 | 9 / 720 | 720 / 720 | 720 / 720 |

The comparison records **same model revision** within each judge. Different input hashes alone do not diagnose a specific root cause; they do show that reference/input exactness is not established. Therefore **E1/rot0 T1 must not be represented as the byte-identical FP16 reference**, nor treated as a demonstrated pure answer-code manipulation relative to that original reference until its input serialization, chat template, tokenization and scoring/decoding contract are independently reconciled. In the other targets T2–T4, the archived comparison records 0 differing input hashes and 0 changed predictions; this does not certify uninspected protocol layers.

## Manuscript changes
Three careful post-table disclosure paragraphs have been inserted after Tables 10, 14 and 17 in the revised main manuscript; a matching retrospective, limited-scope section was appended to the supplement. **All cell text and 20+80 tables are unchanged** in these author-facing Word copies; neither original statistical tables nor GOLD were silently rewritten.

## Other still-open gates
- All other table families / exact manuscript-to-case-level result links
- Nested ModernBERT train/dev/test and preprocessing-fit boundaries
- M4 exact prompt serialization and option-map inversion for all E1/E2 variants
- Source-matched cluster-bootstrap CI refits and all 60 GEE tests, including small-event concerns
- Historical failure-to-retry provenance and rights/ethics/PII release clearance

**Verdict: MAJOR REVISION / targeted 60-cell verification PASS with critical T1 protocol equivalence OPEN.** External independent human validation remains intentionally future work.

## Clean GitHub Actions confirmation

- Workflow: `.github/workflows/audit-targeted-manuscript-tables.yml`
- Run [39430171858](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39430171858) on main commit `9f01afcacfac39756f3548096e789fd22628c930`.
- Job `compare-archived-summaries` concluded **SUCCESS**. The job log reported `PASS_SELECTED_DISPLAY_CELLS_WITH_OPEN_T1_PROTOCOL_DISCREPANCY`.
- Artifact: `targeted-table-check-results` (CSV comparison output and JSON status) was produced and retained with the workflow run. This is an independent **clean checkout execution of the bounded script**, NOT a new model run or independent verification of confidence interval derivation.


## Historical serialization resolution incorporated (20 October 2026)

The previously open **cause of the T1 input-hash divergence** had in fact already been addressed by [the historical serialization reconstruction, dated 15 October](T1_HISTORICAL_SERIALIZATION_RESOLVED_20261015.md). This audit reports 2,880/2,880 exact in-protocol input-hash reconstructions; it isolates the cross-protocol wording layout to one newline between “Do not classify the subtype.” and “Choose only A or B.”. **This prior evidence was missed in the earlier October 20 narrative and has now been explicitly reconciled.** Qwen T1: 0/720 changes in token counts, four different decisions; Mistral T1: 720/720 token-count differences, nine different decisions. There were no zero-token outputs implied by those numbers.

Status split: **PASS (archived provenance report): byte-level origin of differing T1 prompt hashes explained**; **OPEN: causal attribution of changed model decisions to newline alone** and fresh prospectively controlled whitespace sensitivity. The 2,880 provenance checks do not constitute a fresh experiment rerun in this documentation update. In both protocols, original performance figures are retained; E1/rot0 is the internally paired control, not a clone of FP16 Reference.
