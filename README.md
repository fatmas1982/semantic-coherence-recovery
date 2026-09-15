# Semantic Coherence Recovery — Reproducibility Release

**From Reliable Human Annotation to Computational Recovery of Semantic Coherence Failures in Small Language Models**

This repository is the public reproducibility package for the study. It is organized around a strict distinction between **exact numerical reproduction**, **historical bit-for-bit reruns**, and **fresh reconstructed reruns**.

## Release status

**PASS — all frozen data, code, and intermediate/final artifacts required to reproduce every reported numerical result in the paper and supplement are included in the release bundle.** Historical runtime boundaries are documented explicitly where the original executable environment or immutable model revision was not retained.

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
- executable analysis notebooks/scripts, manuscript/supplement text mirrors, source-binary hashes, and a file-level SHA-256 manifest.

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
