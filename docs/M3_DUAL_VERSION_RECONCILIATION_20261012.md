# M3 dual-blocking reconciliation — 12 October 2026

## Authoritative archived protocol and version

The most recent manuscript Table 15 and Supplement S75 use the **complete GPU archive** from `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(2).zip` (SHA-256 `55b879ce51470d6c79933f3f32cc46e1bb4e28bc69693ea8b43ed9514adb2e96`), protocol `M3_nested_selection_dual_and_size_matched_v1`, condition C, model ModernBERT-base revision `c0e44438c79d5a72972fe8b14dbbc822418356c9`, seed 20260908.

For each target, extracted `experiments/M3_T[1-4]_dual_r0_C.zip` and five `M3_T[1-4]_size_matched_r[0-4]_C.zip` nested execution archives. All 24 nested runs contain complete `reports/PREDICTIONS.csv`, `METRICS_AND_CLUSTER_CI.csv`, `COVERAGE.csv`, `MANIFEST.json`, and 30 fold×generator result parts; every archive reports `status=complete`. Recomputed **macro-F1 from each archived y_true/pred pair**, independently of the summary CSV. Each of the 24 scores matches its own summary to machine precision; the five size-matched repetitions share held-out observations and learning seed and are **not independent replications**.

| Task | Cases | Recomputed dual macro-F1 | Five size-matched mean | Legacy GitHub summary (superseded for present manuscript) |
|---|---:|---:|---:|---:|
| T1 | 720 | 0.591322526 | 0.630008358 | 0.553360 |
| T2 | 474 | 0.671147712 | 0.748768941 | 0.675329 |
| T3 | 460 | 0.681835701 | 0.781461993 | 0.700646 |
| T4 | 474 | 0.573272610 | 0.643584882 | 0.600978 |

The prior 0.553/0.675/0.701/0.601 sequence appeared in the original September validity/release summaries from a previous blocked implementation. **The specific row-level data and executed protocol responsible for those earlier numbers have not been independently reconstructed here**; it is unjustified to claim their cause was a specific bug or stochastic seed. Retain them only in this version-history note, not as the submission-authoritative dual-blocked estimates.

## Released evidence, scope and caveat

- `P2_81_M3_DUAL_BLOCKED_OOF_ALL.csv`: 2,128 case-level entries across T1=720/T2=474/T3=460/T4=474, assembled exactly from the archived `reports/PREDICTIONS.csv`; includes de-identified case/prompt ID, frozen labels, recorded decisions, fold and anonymous generator slot; **no raw model output, annotator comments or source text**.
- `P2_81_M3_DUAL_BLOCKED_SUMMARY.csv`: reconciled four-target summary, five-repeat size-matched means/SD, protocol metadata and archive hashes.
- `M3_DUAL_24_ARCHIVE_RECOMPUTATION_AUDIT_20261012.csv`: each of 24 execution archives with SHA256 of the nested ZIP and original `reports/PREDICTIONS.csv`, recorded case count, score, model revision and parent-source SHA256.
- Root archived source bundle **is not modified or distributed by this patch**. The target-level frozen case CSVs and hashes provide downstream verification, but the released OOF-only clean-room test cannot independently refit ModernBERT or recover five size-matched controls without the original nested GPU archive.
- Table S75 originally reports macro-F1, matched-control variability and subgroup uncertainty conditional on this executed protocol; exclude causal generator-signature claims. The five subset repetitions are dependent by common held-out cases/seed.
- The previous public `OOF_ALL.csv` and `SUMMARY.csv` names resolved to an inaccessible 155-byte placeholder string instead of usable CSV at this branch revision; they have now been replaced with actual case predictions and summary. Distinguish artifact availability issues from scientific output validity.

**Do not silently amend GOLD or legacy run archives.** No SLM generation, ModernBERT training, human reannotation, or new test data were generated in this reconciliation.
