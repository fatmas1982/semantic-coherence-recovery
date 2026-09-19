# Reviewer 3 — Measurement / Construct Validity revision

Date: 2026-09-19
Target: Information Processing & Management (IP&M)

This revision changes interpretation/reporting only. FINAL GOLD v1.0, locked A1–A3 ratings, computational targets, folds, M0–M4 predictions, and all previously reported computational metrics remain unchanged.

Implemented changes:
- replaced language that could imply construct truth (e.g., “human-validated”) with “human-adjudicated, reliability-characterised” or equivalent operational wording;
- explicitly separated reliability evidence from construct-validity evidence;
- clarified that the three axes are operationally/analytically separated, not statistically independent or orthogonal latent constructs;
- clarified that Table 7 is a post-study reporting clarification and was not part of the locked annotator instrument;
- stated near the annotation framework that complete coding is forced operational coverage and does not establish taxonomy completeness because no outside-taxonomy/uncodable pathway was prespecified;
- contextualised full-sample severity alpha (.784) with the majority-failure sensitivity alpha (.528) in the abstract and main text;
- added a main-text measurement-validity argument and Supplementary Table S11B mapping each evidence source to supported and unsupported inferences;
- extended the existing explicit-ambiguity sensitivity with ordinal-severity results in Supplementary Table S16A: removing the 36 explicitly ambiguous cases changes fine/family/boundary/full-severity alpha from .703/.731/.723/.784 to .713/.741/.729/.793; majority-failure severity alpha changes from .528 to .532;
- audited FINAL GOLD terminology to retain its status as a senior-adjudicated publication reference rather than an independent external gold standard.

Reproducibility assets:
- code: `code/followup/P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.py`
- result table: `results/followup/P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.csv`
- public inputs: `data/annotation/historical_full_csv/A1/Annotation.csv`, `A2/Annotation.csv`, and `A3/Annotation.csv` after running `UNPACK_RELEASE.py`.

The script recomputes the nominal ambiguity sensitivity reported in Supplementary Table S16 and the ordinal-severity extension reported in Supplementary Table S16A, and performs a frozen-paper reproduction check against the published point estimates.

No re-annotation, taxonomy replacement, external criterion dataset, new model, or model retraining was performed.
