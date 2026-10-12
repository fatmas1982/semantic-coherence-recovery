# Semantic Coherence Recovery — Reproducibility Release

**Reliable Evaluation of Semantic-Coherence Failures in Generated Text: Human Annotation, Computational Recovery, and LLM-Judge Sensitivity**

This repository is the public reproducibility package for the study. It is organized around a strict distinction between **exact numerical reproduction**, **historical bit-for-bit reruns**, and **fresh reconstructed reruns**.

## Release status

**DRAFT / PARTIALLY VERIFIED — independent execution evidence is available only for named modules; the full corrected manuscript-plus-supplement release is not yet frozen or coauthor-approved.** Historical runtime boundaries are documented explicitly where the original executable environment or immutable model revision was not retained. The original transport bundle remains immutable; post-hoc validity files added after that freeze live under `code/validity/` and `results/validity/`.

## IP&M statistical precision follow-up (2026-10-12; draft PR #2)

The **post-hoc 60-fit GEE stability audit** does not introduce new judge inference or additional tests. It refits the previously reported working-independence logistic GEEs on the frozen 10,408 paired case-comparison rows, verifies their original coefficients/p-values, and reports changed-event counts, robust log-OR SEs and *nominal* Wald 95% OR intervals. One Qwen–T1–E2 comparison has just 15 changed outcomes (the same events across three human axes). These diagnostics do **not** correct small-event bias or change the one original 60-test Holm result. See [rationale, methods and limitations](docs/GEE_STABILITY_POSTHOC_AUDIT_2026_10_12.md), [analysis code](code/validity/reanalyse_gee_stability_2026.py), and [archived 60-row output](results/validity_2026_10/HJI_GEE_STABILITY_60.csv). The completed manuscript/supplement Word edits are separate, coauthor-review artifacts and are not represented as merged into this repository.

## Current M3 and governance reconciliation

The completed later M3 dual-blocked macro-F1 values are 0.591/0.671/0.682/0.573, superseding initial September values for this comparison. See [run-level hashes and case-level rationale](docs/M3_DUAL_VERSION_RECONCILIATION_20261012.md). Review [experiment-to-table traceability](docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv) and [100-table caption inventory](docs/MAIN_SUPPLEMENT_100_TABLE_INVENTORY_20261012.csv). The corrected HJI percentile file is authoritative; historical CIs remain superseded. Coauthor, institutional and data-release approvals have not been independently verified.

## Quick start

```bash
git clone https://github.com/fatmas1982/semantic-coherence-recovery.git
cd semantic-coherence-recovery
python UNPACK_RELEASE.py
python code/analysis/reproduce_public_metrics.py
```

`UNPACK_RELEASE.py` reconstructs the complete release from the 86 text-safe transport fragments under `release_bundle/`, verifies the archive SHA-256, and extracts the organized code/data/paper tree.

## What is released

- the 120-prompt diagnostic bank and 720-row six-model generation plan;
- all 720 frozen SLM outputs used in the study;
- generation provenance/configuration and transparent regeneration code;
- the locked annotation manual;
- complete sheet-by-sheet CSV mirrors of the three final historical annotator workbooks (A1/A2/A3), including primary/secondary labels, boundary, severity, ambiguity, evidence-span/note, anchor and metadata fields;
- complete sheet-by-sheet CSV mirrors of the separate round-1 senior-adjudication workbook;
- locked pre-resolution core ratings, FINAL GOLD publication layer, frozen five-fold assignments, M0/M1/M2 archived OOF predictions, and targeted re-review materials;
- a reconstructed M0/M1/M2 training script for fresh sensitivity reruns, clearly separated from the archived reportable OOF values;
- M3 ModernBERT reportable A/B/C OOF predictions, stability runs, ablations, LOTO summary, leakage/source/difficulty analyses;
- M4 Qwen3-8B target-isolated forced-choice A/B/C OOF predictions and comparison outputs;
- follow-up task-conditioned source-utility and predictive-uncertainty analyses;
- post-hoc generator-signature, metadata-only, strict dual-blocking, source-bearing-only, token/truncation, and manual semantic-similarity validity diagnostics;
- Qwen3-8B template/answer-code protocol perturbations, including exact reproduction of the archived reference run;
- exhaustive T4 answer-code sensitivity across all six A/B/C-to-1/2/3 bijections under both frozen P1/P2 rubric phrasings (12 variants);
- executable analysis notebooks/scripts, manuscript/supplement text mirrors, source-binary hashes, and a file-level SHA-256 manifest.

## Post-hoc validity layer (added 2026-09-18)

The reference RQs and analyses were frozen first. The later experiments under `code/validity/` and `results/validity/` test specific threats to interpretation rather than replacing or tuning the reference results:

- recoverable anonymous generator-associated textual signatures;
- metadata-only corpus-structure diagnostics;
- strict prompt-fold + generator-stratum dual blocking for M1 and M3;
- source-bearing-only B->C restrictions;
- ModernBERT token/truncation audit (Condition-C max 446 < 1024);
- manual review of the highest cross-fold semantic-similarity pairs;
- Qwen3-8B rubric / answer-code sensitivity;
- exhaustive T4 mapping sensitivity (2 templates × all 6 bijections = 12 variants).

See `docs/VALIDITY_EXPERIMENTS_2026-09.md` and the updated experiment reproducibility matrix. These analyses support narrower interpretation: **within-corpus recoverability under specified evidence, split, and evaluator protocols**, not generator-invariant understanding, architecture superiority, or external generalisation.

## Reproducibility boundaries

### Human annotation

The original A1/A2/A3 and round-1 senior-adjudication binary workbooks were recovered from the research archive and hash-verified. To keep the GitHub release transparent and diff-friendly, the public release exposes their **complete analytic contents as sheet-level CSV mirrors** under:

`data/annotation/historical_full_csv/`

`SOURCE_BINARY_HASHES.csv` records the immutable hashes of the recovered source binaries. No blank template is substituted for a completed historical workbook.

### M0/M1/M2 CPU baselines

The reportable paper numbers are reproduced exactly from the frozen archived OOF predictions. The original historical training script was not retained. `code/baselines/07_retrain_cpu_baselines_reconstructed.py` therefore implements the documented model specifications and frozen folds for **fresh reconstructed retraining** and must not be described as the original historical executable.

### Generation

The 720 retained model outputs are the authoritative generation layer used by the study. For five checkpoints, immutable repository revisions and every historical chat-template/tokenization/stopping detail were not retained, so fresh generation is best-effort reconstruction rather than a bit-for-bit historical rerun. This limitation does not affect exact reproduction of the reported paper results, which starts from the frozen 720 outputs.

### M4

Only the final target-isolated forced-choice M4 protocol is reportable. The superseded free-generation M4 diagnostic must not be used for scientific comparison.

## Main release map

```text
.
├── code/
│   ├── generation/
│   ├── annotation/
│   ├── analysis/
│   ├── baselines/
│   ├── m3/
│   ├── m4/
│   └── followup/
├── data/
│   ├── prompts/
│   ├── provenance/
│   ├── raw/
│   ├── annotation/
│   │   └── historical_full_csv/
│   ├── frozen/
│   ├── computational/
│   └── followup/
├── docs/
│   ├── REPRODUCIBILITY.md
│   ├── PUBLICATION_REPRODUCIBILITY_AUDIT.md
│   ├── EXPERIMENT_REPRODUCIBILITY_MATRIX.csv
│   ├── RELEASE_VERIFICATION.json
│   └── ...
├── paper/
├── PUBLIC_METRICS_RECOMPUTED.csv
├── SOURCE_BINARY_HASHES.csv
└── SHA256SUMS.csv
```

## Experiment-to-artifact audit

`docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` maps each reportable experiment/claim to:

**RQ → input → executable code/notebook → primary output → paper table/figure → exactness boundary.**

`docs/PUBLICATION_REPRODUCIBILITY_AUDIT.md` gives the final publication-level audit, and `docs/RELEASE_VERIFICATION.json` records the automated integrity/result checks performed before release.

## Release transport integrity

The complete release is stored as 86 ordered Base64 text fragments under `release_bundle/` (parts 0001–0085 contain 10,000 characters each; part 0086 contains the remainder). This fragmentation is only a Git transport mechanism; reconstruction is validated by the archive SHA-256 below.

Expected archive SHA-256:

`69ce2a52c201424d8939d1a997dc3bd34854a2822131c6bc69a791b47635ce3e`

The same value is stored in `BUNDLE_SHA256.txt` and enforced by `UNPACK_RELEASE.py`.

## Safe paper wording

A defensible availability statement is:

> All frozen data, code, and intermediate/final outputs needed to reproduce every reported numerical result in the paper and supplement are available in the public repository. Historical runtime boundaries are documented explicitly where bit-for-bit reruns are not possible; complete historical annotation/adjudication contents are released as sheet-level CSV mirrors with source-binary hashes.

## Licences

- Code: MIT (`LICENSE`)
- Study-created data/documentation: CC BY 4.0 intent (`DATA_LICENSE.md`)

Users remain responsible for complying with upstream model/checkpoint terms when performing fresh regeneration.
