# M3 24-run / 720-cell archived-output audit (21 October 2026)

**Scope:** case-level scoring and exported execution-metadata consistency only. Derived from the author-supplied `IPM_M3_GITHUB_PUBLICATION_20261015(1).zip`. This is not a GPU training replay.

All 24 run-level prediction CSVs (four dual and 20 size-matched) were assessed. Recorded audit outcomes: 24/24 task-level OOF macro-F1 recomputations agreed with summary; 720/720 fold×generator cells agreed with the execution ledger, with no recorded cell metadata inconsistencies. There were 120 outer-fold records. The five size-matched repetitions share test populations and the learning seed and **are not independent replications**.

| Task | Dual macro-F1 | Mean size-matched macro-F1 |
|---|---:|---:|
| T1 | 0.5913225257153932 | 0.6300083576662007 |
| T2 | 0.671147712324077 | 0.7487689410431113 |
| T3 | 0.68183570135006 | 0.7814619927410072 |
| T4 | 0.5732726099821898 | 0.6435848819370128 |

The retrospective `(4)` GPU ZIP differs by digest from authoritative `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(2).zip` and contains incomplete predictions: **7 complete, 1 partial, 16 empty** run archives. Never substitute its partial outputs for the above reference.

**Unverified:** actual train/dev/test membership passed into historical GPU fit, timing of epoch selection, train-only feature fit, provenance of resumed parts. Static code and exported selected-epoch metadata do not close these gates.

**Release classification:** PASS archived numerical OOF + ledger-consistency only; nested training provenance remains OPEN. No models were retrained and no raw personal data were added by this report.
