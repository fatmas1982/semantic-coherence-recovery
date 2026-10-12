# October 2026 IP&M validity follow-up — archived E1/E2 and human–judge analysis

> **2026-10-12 reproducibility correction:** The frozen 60-contrast HJI odds ratios and Holm p-values are unchanged; however historical bootstrap percentile CI endpoints are superseded by the deterministic PCG64-seed-20261010 recalculation. Use `data/validity_2026_10/HJI_60_CORRECTED_CI_SEED_20261010.csv` and `docs/NLP_LLM_EVAL_CORRECTIONS_2026_10_12.md`. The published original `CLASS_ADJUSTED_HUMAN_JUDGE_60_CONTRASTS.csv` remains as a historical export and must not be described as exactly reproduced by the revised CI script. The historical sensitivity notebook is retained, alongside a separately versioned Mistral-revision-pinned notebook.


**Status:** post-hoc, within-corpus, case-paired **analysis of frozen predictions**. Not preregistered; no new annotators, outside corpus, fresh LLM inference, or causal mechanism identification.

## What is included

- \`data/validity_2026_10/paired_cases_part_01.csv\` through \`part_11.csv\`: **10,408** case-level observations constituting **20** judge × target × perturbation comparisons. Each observation includes only case/prompt identifiers, coded GOLD labels, paired recorded predictions, binary human disagreement indicators from A1–A3, generator stratum and uncalibrated next-token score-gap summaries; **no source text, evidence notes or annotator identity mapping**.
- \`data/validity_2026_10/CLASS_ADJUSTED_HUMAN_JUDGE_60_CONTRASTS.csv\`: published 60 exploratory comparisons, with adjusted GEE ORs and Holm/BH corrections.
- \`data/validity_2026_10/E1E2_DECISION_AND_MARGIN_DIAGNOSTICS.csv\`: 20 paired decision-direction and margin summaries.
- \`data/validity_2026_10/E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv\`: 20 paired macro-F1 contrasts from cluster bootstrap.
- \`code/validity/reanalyse_e1e2_pairs_2026.py\`: recompute paired class-level changes and macro-F1 from saved predictions, with Prompt_ID cluster bootstrap.
- \`code/validity/reanalyse_hji_gee_2026.py\`: recompute all 60 GEE associations, class-standardised risk differences and multiplicity corrections.

## Additional precision/support audit (2026-10-12)

See [GEE_STABILITY_POSTHOC_AUDIT_2026_10_12.md](GEE_STABILITY_POSTHOC_AUDIT_2026_10_12.md) for scientific motivation, exact covariates/working covariance, event-count interpretation, limits of nominal Wald OR intervals and linkage to the *same* 60 Holm/BH tests. Script: `code/validity/reanalyse_gee_stability_2026.py`; output: `results/validity_2026_10/HJI_GEE_STABILITY_60.csv`. These are precision diagnostics, not extra discoveries or new LLM calls.

## Requirements

Python 3.10+; \`pandas\`, \`numpy\`, \`scipy\`, \`scikit-learn\`, \`statsmodels\` (document installed versions when reproducing).

## Recompute on frozen case data

Run from the repository root:

\`\`\`bash
python code/validity/reanalyse_e1e2_pairs_2026.py --bootstrap-reps 3000
python code/validity/reanalyse_hji_gee_2026.py --bootstrap-reps 2500
\`\`\`

Both scripts create files under \`results/validity_2026_10/\`. Point estimates and GEE p-values match the historical CSV, but the revised 95% percentile CI endpoints are supplied in the corrected 20261010 CSV; historical CI draw ordering was not exactly reproducible. Nonparametric percentile bootstrap intervals can vary at the last digits if draw ordering or random-generator versions differ. Report the actual software environment and compare point estimates independently.

## Inferential specification

- **E1:** answer-code-to-category bijections altered; **E2:** visible option-order altered.
- An E1 code-rotation-0 baseline is paired with each alternative code/option-order prediction for the exact same Case_ID.
- Baseline \`pred_base\` and perturbed \`pred_pert\` are mapped back to **semantic class labels before comparison**.
- Changed-case indicator: 1 if \`pred_base != pred_pert\`.
- Macro-F1 is computed on each target's **gold-defined eligible cases**. T1=720, T2=474, T3=460, T4=474, under the study's fixed eligibility rules; this is not an end-to-end deployed classifier.
- Bootstrap resamples **Prompt_ID clusters with replacement**, retaining all eligible generator outputs within each sampled prompt.
- For each of 20 paired comparisons × 3 human axes (primary, boundary, severity), the association with change is examined.
- Marginal class-standardised risk difference (percentage-point contrast) is distinct from the conditional GEE odds ratio.
- GEE uses a **working independence** correlation structure with robust cluster-sandwich uncertainty by \`Prompt_ID\`, adjusting for adjudicated GOLD class and generator ID. This is the precise reported specification; an **exchangeable** working correlation leads to different estimates.
- Holm adjustment covers all 60 exploratory GEE hypothesis tests; one contrast remains below .05 (Mistral–T2–E1–grounding boundary; adjusted p≈0.0333).

## Scientific and reproducibility boundaries

1. These are **archived-prediction** reanalyses, not a full judge generation pipeline. The archived October execution notebook is supplied above. The original server-prediction ZIP contains additional log-probability and model-revision details; the standalone reanalysis scripts do not rerun either model or claim bit-identical fresh generation.
2. Differences between Qwen and Mistral include chat-template and implementation details, so these records do not isolate architecture or token priors as a cause.
3. Next-token log-probability score gaps are **not calibrated semantic confidence**.
4. The 60 comparisons are *post-hoc, correlated and exploratory*. Passing Holm does not establish a causal effect or out-of-corpus transportability.
5. The A1–A3 flags are from **frozen pre-adjudication ratings**; GOLD categories are from the separately adjudicated operational reference, not an independent external human criterion.
6. Archived M4 NF4 Qwen runs differ from the later FP16 E1/E2 Qwen and Mistral implementations.
7. Raw human names, linkage of named annotators to A1/A2/A3, unpublished evidence notes and server access credentials are **not included** in this follow-up release.

## Pre-release checks

- 11 case parts concatenate to **10,408** rows with no duplicate (judge,target,experiment,variant,case_id).
- 20 comparison groups and 60 human-axis tests.
- Published GEE ORs and p-values reproduce with the **working independence** specification and robust clustered errors.
- Existing source study corpus and reference release are not modified; these files provide a supplementary, versioned post-hoc layer.

The reviewed manuscript/supplement and source statistical archives remain subject to normal coauthor verification and the journal's submission requirements. This release does not claim an independent external validation study.
