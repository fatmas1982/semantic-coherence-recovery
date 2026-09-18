# Reproducibility Guide

This guide separates **exact analysis reproduction** from **generation-stage reconstruction**.

## A. Exact paper-results reproduction

### A0. Extract the public release

After cloning the repository, run:

```bash
python UNPACK_RELEASE.py
```

The outer bundle is text-safe on GitHub and extracts the complete public analytic layer. `SHA256SUMS.csv` verifies every released file.

The exact original A1/A2/A3 and round-1 adjudication workbook binaries were recovered from the study archive and SHA-256 verified against the paper/supplement provenance record. To keep the GitHub release directly inspectable and diff-friendly, the public package releases **every sheet and every analytic field** from those workbooks as CSV under `data/annotation/historical_full_csv/`; the original source-binary hashes are preserved in `FULL_HISTORICAL_CSV_MANIFEST.csv`.

### A1. Frozen public inputs

Use:

- `data/publication/canonical_publication_dataset_720.csv`
- `data/frozen/baseline_csv_mirror/`
- `data/frozen/targeted_rereview_sheets/`
- `data/annotation/historical_full_csv/A1/Annotation.csv`
- `data/annotation/historical_full_csv/A2/Annotation.csv`
- `data/annotation/historical_full_csv/A3/Annotation.csv`
- `data/annotation/historical_full_csv/ROUND1_ADJ/Adjudication.csv`
- `data/annotation/locked_core_ratings/`

Core structural assertions:

```text
720 final cases
120 unique Prompt_ID clusters
6 task types
T1 N=720
T2 N=474
T3 N=460
T4 N=474
```

### A2. CPU baselines / frozen verification

Run:

`code/analysis/P2_54_Colab_01_Verify_Completed_Experiments.ipynb`

The resampling unit is `Prompt_ID`; all six outputs belonging to the same prompt remain together.

### A2b. Optional reconstructed M0/M1/M2 retraining

The historical CPU-baseline training executable was not retained. For a fresh reconstruction of the documented M0/M1/M2 specifications, run:

```bash
python code/baselines/07_retrain_cpu_baselines_reconstructed.py
```

This produces retrained predictions and explicitly compares them with the archived OOF. **Do not replace the reportable archived OOF values with reconstructed retraining values.**

### A3. M3 ModernBERT

Run:

`code/m3/P2_54_Colab_02_v3_M3_ONLY.ipynb`

Primary seed: `20260908`  
Stability seeds: `20260909`, `20260910`  
Bootstrap repetitions: `2000`  
Bootstrap seed: `20260908`

The reportable contextual encoder is ModernBERT-base at the repository revision recorded in the run manifest.

Expected primary condition-C Macro-F1:

```text
T1 0.6553
T2 0.7772
T3 0.7908
T4 0.6369
```

T4 QWK ≈ `0.5965`.

### A4. M4 Qwen3-8B forced-choice judge

Run:

`code/m4/P2_55_Colab_M4_ONLY_Forced_Choice_Qwen3_8B.ipynb`

Model:
`Qwen/Qwen3-8B`

Pinned revision:
`e8bbd8252970581ea5b08b6a5b3e668adaf3161a`

The final protocol is target-isolated and closed-set. It scores only valid answer codes for the active target; it does not freely generate taxonomy labels.

Expected condition-C Macro-F1:

```text
T1 0.741
T2 0.609
T3 0.530
T4 0.391
```

All 12 target×condition OOF files must retain the complete frozen population and have 100% output-contract compliance.

### A5. Follow-up analyses

Run:

`code/followup/P2_55_Colab_FOLLOWUP_ANALYSES_ALL_CODE.ipynb`

or:

```bash
python code/followup/P2_55_FOLLOWUP_ANALYSES_ALL_CODE.py \
  --results-dir data/computational/m3 \
  --output-dir reproduced_followup
```

These reproduce:
- exploratory task-conditioned source utility;
- Human-Easy vs Human-Hard uncertainty contrasts.

They do not retrain M3.

## A6. Post-hoc validity and sensitivity analyses

These analyses were added after the reference analysis layer was frozen. They test threats to interpretation and must not be described as preregistered confirmatory endpoints or external validation.

### CPU diagnostics

Run:

```bash
python code/validity/P2_81_CPU_VALIDITY_DIAGNOSTICS.py \
  --gold data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx \
  --base data/frozen/P2_CPU_Baselines_v1.0.xlsx \
  --m3-dir data/computational/m3 \
  --m4-dir data/computational/m4 \
  --semantic-dir data/computational/m3 \
  --out reproduced_validity_cpu \
  --run-token-audit
```

Released outputs cover the anonymous generator-signature probe, metadata-only diagnostics, strict M1 dual blocking, source-bearing-only B->C restriction, ModernBERT token audit, manual top-similarity review, and reference point-estimate reproduction checks.

### Strict M3 dual blocking

Run `code/validity/P2_81_GPU_M3_DUAL_BLOCKED_MODERNBERT.ipynb`.

The held-out cell is unseen by both Prompt_ID fold and anonymous generator stratum. Dual-blocked macro-F1 is 0.553/0.675/0.701/0.601 for T1–T4. This is an internal invariance sensitivity analysis within the observed six-stratum corpus, not external validation.

### M4 protocol sensitivity

Run `code/validity/P2_81_GPU_M4_PROTOCOL_SENSITIVITY_QWEN3_8B.ipynb`.

The archived P1/identity reference predictions must reproduce exactly before prompt/code perturbations are interpreted. The experiment holds the Qwen revision, target population, evidence condition, chat/scoring rule, and forced-choice mechanism fixed.

### Complete T4 mapping sensitivity

Run `code/validity/P2_84_GPU_M4_T4_COMPLETE_PERMUTATIONS.ipynb`.

All six bijections between A/B/C and severity 1/2/3 are evaluated under each frozen P1/P2 rubric phrasing (12 variants). The observed macro-F1 range is 0.206–0.413 and QWK range is 0.006–0.401. These are descriptive protocol-sensitivity summaries; variants are not a random sample and no best-performing mapping is selected.

Full interpretation and artifact paths are documented in `docs/VALIDITY_EXPERIMENTS_2026-09.md`.

## B. Regenerating the 720 SLM responses

If you want to reconstruct the generation stage:

```bash
python code/generation/01_prepare_generation_plan.py \
  --prompt-bank data/prompts/paper2_prompt_bank_120.csv \
  --model-registry data/provenance/paper2_model_registry_6.csv \
  --config data/provenance/paper2_generation_config_GENCFG_v1.json \
  --output reconstructed_generation_plan_720.csv
```

Then, in a suitable Transformers environment:

```bash
python code/generation/02_generate_model_outputs_reconstructed.py \
  --plan reconstructed_generation_plan_720.csv \
  --output-dir regenerated_outputs \
  --models M01 M02 M03 M04 M06
```

For historical M05/RWKV compatibility, use the dedicated environment and runner described in:
`code/generation/02b_generate_rwkv_m05.py`.

Finally:

```bash
python code/generation/12_check_generation_completeness.py \
  --input regenerated_outputs/generated_outputs.csv
```

### Generation warning

This is a **best-effort reconstruction**, not a bit-for-bit historical replay. Exact immutable model revisions and every applied chat-template/tokenizer/stopping detail were not retained for five of the six generation checkpoints. Therefore regenerated text can differ even when the public checkpoint name and decoding profile match.

The paper's reported human/computational results are tied to the frozen outputs in:

`data/raw/generated_outputs_720.csv`

## C. Re-running the annotation workflow

Prepare fresh blinded sheets from the frozen 720 outputs:

```bash
python code/annotation/03_prepare_annotator_sheets.py \
  --generated data/raw/generated_outputs_720.csv \
  --output-dir new_annotation_round
```

Annotators must use:

`docs/Paper2_Annotator_Manual_v1.2_final_hybrid_locked.pdf`

Validate each completed workbook:

```bash
python code/annotation/05_validate_annotations.py \
  --input new_annotation_round/annotator_sheet_A1.csv
```

Merge three independently completed sheets:

```bash
python code/annotation/04_merge_annotations.py \
  --inputs A1.csv A2.csv A3.csv \
  --output merged_locked_ratings.csv
```

Core reliability:

```bash
python code/annotation/06_human_reliability.py \
  --ratings merged_locked_ratings.csv \
  --output-dir human_reliability_outputs
```

The blank `completed_annotation_sheet_A*` files inside the early generation archive are templates; do not mistake them for the historical locked ratings. The actual full historical workbooks are released under `data/annotation/historical_full_csv/`.

For paper-result verification, the shortest route is frozen outputs → full/locked human provenance → FINAL GOLD → archived baseline/M3/M4 OOF → reported metrics. Fresh generation and reconstructed M0–M2 retraining are optional sensitivity/reconstruction paths, not prerequisites for reproducing the reported numbers.
