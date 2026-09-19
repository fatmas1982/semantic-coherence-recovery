# IP&M submission-preparation update — 2026-09-18

This branch preserves the frozen reference analyses and adds one post-hoc contextualisation requested during Information Processing & Management submission preparation.

## Frozen layers unchanged
- FINAL GOLD v1.0 is unchanged.
- Frozen Prompt_ID folds are unchanged.
- M0–M4 reference predictions and all previously reported validity analyses are unchanged.
- No model was retrained and no new LLM-judge run was selected.

## Added: annotator-to-adjudicated-reference target concordance
The locked A1–A3 decisions are projected onto the same FINAL GOLD-defined T1–T4 target populations used for computational evaluation. For T2–T4, an annotator decision outside the target-valid label set is counted as a strict miss and target-valid coverage is reported separately. Confidence intervals use 2,000 Prompt_ID-cluster bootstrap resamples (seed 20260908).

Strict macro-F1 ranges across A1–A3:
- T1: 0.863–0.957
- T2: 0.835–0.936
- T3: 0.847–0.930
- T4: 0.644–0.858
- T4 strict QWK: 0.488–0.854

These values are **not an independent human ceiling or a new IAA estimate**, because FINAL GOLD v1.0 was constructed from the same A1–A3 layer plus senior adjudication.

The independent second-adjudicator audit proposed during review planning was not performed because an additional senior linguist was not available. This limitation is stated explicitly in the IP&M manuscript.
