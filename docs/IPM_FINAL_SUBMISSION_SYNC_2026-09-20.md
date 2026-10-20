# IP&M Final Submission Synchronization — R14 (2026-09-20)

This document synchronizes the public reproducibility repository with the final pre-submission audit of:

**Reliable Evaluation of Semantic-Coherence Failures in Small Language Model Outputs: Human Annotation, Computational Recovery, and LLM-Judge Sensitivity**

## Scientific freeze
No R14 synchronization step changes:
- FINAL GOLD v1.0 scientific case-level decisions;
- locked A1/A2/A3 pre-resolution ratings;
- Prompt_ID folds;
- T1-T4 target definitions or eligible populations;
- archived M0-M4 predictions or headline point estimates;
- post-hoc validity predictions.

R14 repairs editorial cross-references and synchronizes experiment-to-artifact mapping after manuscript compression.

## Final manuscript numbering
- Main tables: 1-16.
- Main figures: 1-2.
- Main equations: (1)-(8).
- Supplementary tables: S1-S46 with local suffixes, in document order.
- Supplementary figures: S1-S4.
- Supplementary equations: (S1)-(S12).

The authoritative experiment-to-artifact mapping for the final submission is:
`docs/IPM_FINAL_EXPERIMENT_REPRODUCIBILITY_MATRIX_R14.csv`.

## Public repository versus double-anonymized review
This GitHub repository is identity-bearing and public. It is therefore **not** the reviewer-facing access route during double-anonymized review. The anonymized submission uses a detached reviewer-facing reproducibility package with identifying collaborator provenance and the public repository URL removed. The editor-facing title page and cover letter provide this public repository location.

## Exactness boundaries
The frozen 720 generated outputs are authoritative for all reported analyses. Fresh regeneration is not claimed to be bit-for-bit identical for five historical generation checkpoints because every immutable revision/interface detail was not retained. Exact M0-M2 paper numbers are reproduced from archived OOF predictions; fresh M0-M2 retraining is a documented reconstruction because the original historical trainer was not retained. M3/M4 reportable OOF predictions and current validity/follow-up artifacts are retained and mapped in the final matrix.

## R14 deterministic error audit
`code/followup/P2_IPM_R14_DETERMINISTIC_ERROR_AUDIT.py` reproduces the non-cherry-picked case-selection rule used for Supplement Table S44B. Its frozen output is `results/followup/P2_IPM_R14_DETERMINISTIC_ERROR_AUDIT.csv`.
