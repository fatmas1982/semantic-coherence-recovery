# Reviewer 4 — Statistical / Experimental Design revision

Date: 2026-09-19
Target: Information Processing & Management (IP&M)

R5 implements all Reviewer #4 actions except those explicitly marked not required. No model was retrained and no frozen point estimate, target population, fold assignment, or FINAL GOLD label was changed.

Implemented:
- computational bootstrap intervals are now explicitly described as Prompt_ID-cluster sampling uncertainty conditional on frozen folds and archived OOF predictions, not full retraining/fold-selection uncertainty;
- exact McNemar p-values were removed from Main-text headline inference and retained only as a supplementary unclustered sensitivity diagnostic;
- an explicit target-wise multiplicity policy was added: no family-wise adjustment across distinct prespecified T1–T4 estimands, with interpretation focused on magnitude, interval width/direction, and robustness rather than binary significance;
- row-level Wilson intervals were removed from purposively constructed FINAL GOLD distribution tables;
- Table S39 now reports output rows N and Prompt_ID clusters K;
- a post-hoc task-stratified computational-bootstrap sensitivity was executed from frozen OOF predictions: zero-inclusion status changed for 0 intervals and the maximum endpoint shift was 0.013;
- a fold-by-class audit was executed: every target class is present in every outer fold after eligibility filtering, with the smallest fold-class cell equal to 11 cases.

Reproducibility:
- code/followup/P2_IPM_STATISTICAL_DESIGN_SENSITIVITY.py
- results/followup/P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SENSITIVITY.csv
- results/followup/P2_IPM_FOLD_BY_CLASS_AUDIT.csv

Not performed because Reviewer #4 marked them not required:
- increasing bootstrap repetitions to 10,000;
- retraining M3 inside bootstrap replicates;
- conventional power analysis;
- adding new models.
