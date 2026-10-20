# Reviewer 5 — Human Annotation / Reliability revision

Date: 2026-09-19
Target: Information Processing & Management (IP&M)

This revision changes human-workflow documentation and adds frozen-data diagnostics only. No annotation was repeated or changed. FINAL GOLD v1.0, A1–A3 locked workbooks, Prompt_ID folds, T1–T4 populations, M0–M4 predictions, and all frozen computational point estimates remain unchanged.

Implemented:
- documented A4 as a separate senior-adjudication role rather than a fourth independent IAA rater;
- recorded that A4 received the same locked Guide but did not complete the A1–A3 18-case calibration;
- documented the A4 information boundary for the 423 queued cases: case evidence plus submitted A1–A3 annotations, without direct contact with A1–A3, checkpoint identity, computational results, or expected study outcomes;
- clarified the A1–A3 18-case calibration percentages (93.8%, 90.3%, 87.0%) as documentary training diagnostics; the preserved package does not retain a field-by-field numerator/denominator sufficient to reconstruct them independently, so they are not treated as IAA, pass/fail scores, or inferential statistics;
- explicitly described fine-label alpha=.703 as a framework-level coefficient rather than evidence that all 15 sparse labels are individually reliable;
- made the adjudication queue fully reproducible: disagreement in any of six structured fields (primary label, secondary label, boundary zone, severity score, HREF subtype, ambiguity flag) reproduces exactly 423 queued and 297 non-queued cases; evidence notes/spans, anchors, timestamps, and free text are not queue triggers;
- corrected the 29-case provenance to a project-lead Guide-consistency audit followed by same-adjudicator targeted re-review (27 revised, 2 confirmed), not independent adjudicator reliability;
- added pair-specific pre-resolution reliability from locked A1–A3 ratings only;
- added the limitation that annotation-session timing, breaks, and fatigue were not prospectively logged;
- anonymized rater profile details in the blinded Supplement.

Pair-specific results:
- fine-label exact/Cohen kappa: A1-A2 80.0%/.734; A1-A3 79.0%/.718; A2-A3 73.6%/.661;
- family kappa: .730-.733;
- grounding-boundary kappa: .720-.731;
- severity exact agreement: 67.6%-77.1%; within-one agreement: 89.0%-94.6%; pair-specific QWK: .737-.856;
- 95% CIs use 2,000 task-stratified Prompt_ID-cluster bootstrap resamples, seed 20260804.

Reproducibility assets:
- code/followup/P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.py
- results/followup/P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv
- results/followup/P2_IPM_ADJUDICATION_QUEUE_RULE_AUDIT.csv

Private full-name/affiliation/ORCID provenance is intentionally not uploaded to the public repository or blinded journal package.

Not performed because Reviewer #5 marked them not required:
- re-annotation of the 720 cases;
- a fourth main-round annotator;
- a new independent second adjudicator;
- a new calibration round.
