# IP&M R14 final submission sync

Date: 2026-09-20

This note synchronizes the public reproducibility repository with the R14 final pre-submission manuscript/supplement numbering. It changes no frozen scientific result, label, fold, model prediction, or estimator.

## Current manuscript numbering

- Human nominal reliability: Main Table 7.
- Severity reliability: Main Table 9.
- Reference Condition-C evaluator performance: Main Table 10.
- Paired evaluator contrasts: Main Table 11.
- Evidence-condition results: Main Table 12.
- Human-machine difficulty: Main Table 13.
- Strict M3 prompt+generator dual blocking: Main Table 14.
- M4 protocol sensitivity: Main Table 15.
- Robustness/generalisation synthesis: Main Table 16.
- Task-stratified computational-bootstrap sensitivity: Supplement Table S37A.

The canonical experiment-to-artifact mapping is in `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv`.

## Availability boundary

The public repository is identity-bearing. The double-anonymized reviewer manuscript therefore withholds the repository URL; the separate title page/submission metadata may provide it to the editorial office. The frozen data/code/results release remains public at the repository root.

## Scientific freeze

R14 is a cross-reference, numbering, presentation, and submission-synchronization pass only. It does not alter FINAL GOLD, A1-A3 locked ratings, Prompt_ID folds, T1-T4 definitions/populations, M0-M4 predictions, or headline numerical results.

## R12/R14 deterministic error-audit artifacts

The final robustness/error-analysis tables are now mapped to:
- `code/followup/P2_IPM_R12_ROBUSTNESS_ERROR_AUDIT.py`
- `results/followup/P2_IPM_R12_M3_CLASS_DIAGNOSTICS.csv`
- `results/followup/P2_IPM_R12_DETERMINISTIC_ERROR_SELECTION.csv`

These are post-hoc reporting diagnostics over frozen M3 predictions and pre-resolution human fields; no model is retrained and no favourable case is selected manually.

## R14.1 figure-restoration correction

The R14 DOCX packaging pass accidentally removed the drawing paragraph that invokes Figure 1 while leaving the image binary, relationship, caption, note, and surrounding scientific text intact. R14.1 restores the original Figure 1 drawing paragraph from the prior verified manuscript. This is a presentation/package correction only: no scientific text, FINAL GOLD field, result, table value, equation, reference, fold, model prediction, or supplement content changed.
