# Post-hoc GEE inference-stability audit — 12 October 2026

## Why this additional analysis was performed

The E1/E2 audit tests **within-case decoded-label sensitivity** to answer-code remapping (E1) or visible option-order changes (E2). A separate exploratory human–judge layer asks whether those changes are associated with the locked A1–A3 **pre-resolution human non-unanimity** flags. It yields **60** overlapping contrasts (20 executed perturbation comparisons × 3 human rating axes).

The original layer already reports: (1) crude changed-decision risk differences, (2) GOLD-class-standardised marginal risk differences with nominal 2,500-draw Prompt_ID-cluster bootstrap intervals, and (3) covariate-adjusted binomial logistic GEE odds ratios with Holm- and BH-adjusted p-values over the **single pre-existing family of 60 coefficient tests**.

Statistical peer review flagged that some binary outcomes were rare. A model can converge and return a robust sandwich SE even when *sparse changes or influential prompt clusters make Wald inference unstable*. We therefore ran a **post-hoc inferential precision and observed event-support diagnostic** of the *same 60 fits*. This is **not a new question, hypothesis family, LLM experiment, annotator study, causal test, or alternative significance screen**.

## Inputs and exact execution

Source data already present in this draft branch:
- \`data/validity_2026_10/paired_cases_part_01.csv\` through \`paired_cases_part_11.csv\` (10,408 overlapping **case-comparison** records; not independent observations).
- \`data/validity_2026_10/HJI_60_CORRECTED_CI_SEED_20261010.csv\` (archived, corrected 60-row HJI summary used to verify ORs and nominal p-values).

Code: \`code/validity/reanalyse_gee_stability_2026.py\`.

Output, now committed to GitHub: \`results/validity_2026_10/HJI_GEE_STABILITY_60.csv\`.

Run from the repo root, with compatible NumPy and statsmodels installed (for statistical version guidance see \`docs/requirements_hji_2026_10_12.txt\`):

\`\`\`bash
python code/validity/reanalyse_gee_stability_2026.py
\`\`\`

The script checks 20 paired comparisons and 60 fits, verifies GEE adjusted odds ratios and unadjusted p-values against the frozen reference to <1e-6, and emits \`results/validity_2026_10/HJI_GEE_STABILITY_60_RECOMPUTED.csv\`. Compare this recomputation to the committed output after a clean local installation. No GPU, model weights, external annotation, source texts, credentials or new judge calls are required.

## Statistical specification and reported columns

For each **fixed judge × target × E1/E2 variant × human axis**:
- Response: binary \`changed\`, i.e. whether the *same Case_ID's* decoded semantic-label prediction differs between that variant and the matched E1/rot0 control. Change can be correct→wrong, wrong→correct or wrong→different-wrong.
- Exposure: 0/1 indicator of *pre-resolution* rater non-unanimity on primary, grounding-boundary or severity axis.
- Controls: categorical **adjudicated GOLD target class** and six fixed anonymous generator slots.
- Inference: binomial logit GEE, working **Independence** correlation, robust sandwich inference grouped by **Prompt_ID**; at most 120 clusters per fit. The generator slots are **fixed chosen strata**, not a random effect or evidence for population-level generalisation across generators.
- For the exposure coefficient β: \`robust_GEE_SE\` is the sandwich SE on the **log-odds** scale. \`gee_adjusted_OR=exp(β)\`. Nominal \`OR_Wald95_low/high=exp(β ± 1.96 SErobust)\`; these **95% Wald intervals are neither multiplicity-adjusted nor calibrated for sparse outcomes**.
- \`total_changed\`, \`event_rate\`, disagreement/agree denominators and change counts, \`converged\`, and \`low_event_flag\` are per-fit diagnostics. The **<30 change** flag is an explicitly *ad hoc descriptive screen*, not a validated event-per-variable requirement, a rule for excluding data, or a statistical correction.

The original **class-standardised RD** only standardises by GOLD class, while GEE also adjusts for generator slot and uses a conditional OR scale. Their signs can differ (14/60 contrasts in this archive), and a GEE OR cannot be converted into a percentage-point RD by interpretation alone. The GEE stability file **does not recompute** the separately corrected 2,500-resample RD bootstrap CIs and does not affect those intervals.

## Key findings and interpretation

- All **60** GEE odds ratios and nominal p-values are numerically reproduced from the frozen paired-case archive; all fits report numerical convergence.
- The **same Qwen–T1–E2/rot1 comparison** has **15/720 changed decisions**; its three human-axis GEE fits therefore share **15 changed decisions**, **not 45 independent events**. Only these three rows trigger the <30-event descriptive flag.
- For its **primary** non-unanimity axis: OR = **2.806**, robust SE(log-OR) = **0.627**, nominal Wald 95% OR interval **[0.820, 9.599]**, nominal p ≈ **0.100**. This is *low-precision evidence*, not a reliable identified association.
- The single association passing the **original** 60-coefficient Holm correction is **Mistral–T2–E1/rot1–grounding boundary**: **65/474** changed decisions; adjusted OR = **2.550**, robust SE(log-OR) = **0.271**, nominal Wald OR interval **[1.499, 4.338]**; Holm-adjusted p ≈ **0.0333**. Its *distinct, marginal GOLD-class-standardised* RD = +0.0828, corrected **nominal prompt-cluster-bootstrap** CI [+0.0264, +0.1499]. Neither CI is a Holm-simultaneous interval.
- The 60 outputs are **correlated**, because each human axis and perturbation reuses frozen cases and prompt groups. Convergence and nominal robust Wald CIs do **not** rule out sparse-data bias, influential clusters, near separation, or finite-cluster undercoverage.

### Relation to paper and supplement

The October 12 updated main manuscript describes the **motivation and estimand** near Eq. (8), reports examples under the post-hoc sparse-event audit, and relates them to E1/E2 and the distinct RD analyses in the Discussion. Supplement **§S9.15** documents the exact 60-fit refitting method, formula, event-denominator definition, table/CSV provenance, limitations, and the corrected-HJI-CI lineage. Original table S79 remains unchanged: the new data file is its **separate precision/support companion**, not a replacement for its 60 GEE hypothesis results.

This versioned diagnostic was prompted by methodological review **after the original hypotheses and evaluations**. It does not create RQ5, prove a causal link between human disagreement and judge instability, correct rare-event bias or validate the operational human GOLD reference externally.
