# NLP / LLM-Evaluation audit corrections — 12 October 2026

## Release discipline
This is a **post-hoc within-corpus reproducibility correction**, not new model inference, new annotation, a preregistered trial, or external evaluation. Preserve the original October 9 notebook and original archived prediction exports as historical artifacts. The baseline and CI findings below are reconciliations of **already executed predictions**.

## Critical corrections (C1–C6)

**C1. Estimand.** FP16 and archived NF4 evaluator claims concern **constrained single-token next-token forced-choice classification**: the rubric maps semantic labels to codes A/B(/C); each code is validated as one tokenizer token; the log-softmax from the last prompt position is restricted to the allowed token IDs; the maximum-scoring allowed code is decoded to a semantic label. Scores/margins are uncalibrated. No complete assistant response is generated.

**C2. Mistral checkpoint.** The original notebook used dynamic `revision=None`, but the *executed server manifest* `mistral_fp16_offload_pinned.json` states immutable revision `c170c708c41dac9275d15a8fff4eca08d52bab71` and Transformers 4.57.6. The new `code/validity/P2_COLAB_JUDGE_TWO_SENSITIVITY_20261012_PINNED_PATCH.ipynb` pins exactly that revision. **This is a code-reproduction patch only**; historical raw prediction files have not been regenerated.

**C3. Reference versus E1/rot0.** The archived *initial reference* FP16 run is not the E1/rot0 control. An exact Case_ID join of `reports/PREDICTIONS.csv` from `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(2).zip` with `SERVER_JUDGE_SENSITIVITY_20261009_A_BUNDLE.zip` shows:
- Mistral T1: reference macro-F1 0.4440087005 versus E1/rot0 0.4276082638; **9/720** decisions differ, and **720/720** input SHA-256 hashes differ. Token counts differ for all 720.
- Qwen T1: reference 0.7679227038 versus E1/rot0 0.7707529147; **4/720** decisions differ, and **720/720** input hashes differ (token counts unchanged).
- **All T2/T3/T4 cases match exactly** in input SHA-256 and decoded predictions for both judges. Revisions match for all eight judge-target comparisons.
- This localises the divergence to **T1 serialization/inference-input content**. The retained artifacts do **not** identify the unique textual/formatting root cause; no causal cause is asserted.
See `data/validity_2026_10/FP16_BASELINE_INPUT_HASH_COMPARISON.csv`. E1/E2 paired comparisons use **only** E1/rot0, never the earlier reference invocation.

**C4. Timeline correction.** The historical notebook's phrases “pre-registered” and “not yet executed” are pre-run *planning comments*. Subsequently completed CSV artifacts prove the experiments were executed later; E1/E2 were **post-hoc**, not preregistered. Historical file retained unchanged; versioned pinned notebook adds an explicit correction notice.

**C5. HJI bootstrap.** The archived 60-row GEE odds ratios, coefficients, p-values, Holm correction and point-standardised risk differences reproduce unchanged from frozen paired cases with **working-independence** binomial GEE, robust Prompt_ID-clustered sandwich inference and GOLD class plus generator-slot adjustments. By contrast, the archival 95% *bootstrap CI endpoints* did not exactly reproduce using the old released script at either stated candidate seed 20261009 or 20261010. We therefore explicitly **supersede** only those interval endpoints, not the inferential point estimates.
- New deterministic implementation in `code/validity/reanalyse_hji_gee_2026.py`; run it with `--bootstrap-reps 2500 --seed 20261010`.
- NumPy default PCG64; resample all Prompt_ID clusters with replacement 2,500 times in first-seen cluster order; fix original target-specific class weights, omit unsupported arm×class bootstrap strata and renormalise weights. Analyses condition on frozen case predictions.
- Revised 60-row file `data/validity_2026_10/HJI_60_CORRECTED_CI_SEED_20261010.csv`; archived historical `CLASS_ADJUSTED_HUMAN_JUDGE_60_CONTRASTS.csv` remains unchanged.
- Holm surviving Mistral/T2/E1/rot1/grounding-boundary estimate: class-standardised RD **+0.08283756**, *corrected percentile interval* **[+0.02641892, +0.14990499]**, adjusted GEE odds ratio **2.54986675**, Holm p **0.03328668**. Original archival percentile interval [0.021751,0.149859] is historical; no claim of bit-identity to that prior bootstrap draw sequence is made.
- Software used for the revised run: Python 3.13, NumPy 2.3.5, pandas 2.2.3, statsmodels 0.14.6, SciPy 1.17.0, scikit-learn 1.8.0. Check runtime portability and lock versions for archived-point-estimate regression tests.

**C6. Table references.** The current supplementary protocol tables are **S54 (serialization), S55 (rubrics), S56 (answer-code maps), S57 (specifications), S58 (runtime/training checks)**. Superseded references `S34–S34D` and `S34C/S34D` point to a different post-renumbering table and have been corrected in the October 12 manuscript files.

## Other NLP interpretation corrections
- T3 is an operational GOLD family prediction target and correlates with grounding status (Cramér’s V=0.728 on 460 eligible cases); not proof of disentangled semantic mechanism.
- T2–T4 are GOLD-eligibility-conditioned diagnostics, not an executed end-to-end cascade.
- Dual blocking alters generator/label/development mix; total-row-count matching does not isolate a single shortcut effect.
- FP16 versus NF4, Qwen versus Mistral and M3 versus M4 are different full measurement protocols, not identified model-family superiority tests.
- The HJI 60-test family is correlated, post-hoc and observational. GEE odds ratios and class-standardised marginal risk differences answer different questions.
- For M3/T4, 97.5% within-one has an arithmetic constant-3 within-one comparator of 408/474=86.1%; per-class F1 and QWK remain necessary.
- Calibration-history percentage claims remain documentary when source row-level numerators/denominators are unavailable. Gold adjudication is not independent human validation.

## Usage

```bash
python code/validity/reanalyse_e1e2_pairs_2026.py --bootstrap-reps 3000
python code/validity/reanalyse_hji_gee_2026.py --bootstrap-reps 2500 --seed 20261010
```

These scripts recompute statistics **from stored predictions**. Rerunning inference requires original frozen inputs, GPU resources and a pinned compatible library/runtime; it is not promised bit-identical.

**No external annotators or new benchmark experiments were run or are required for this correction package.**
