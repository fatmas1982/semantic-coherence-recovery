# Semantic Coherence Recovery — Reproducibility Release

**Reliable Evaluation of Semantic-Coherence Failures in Small Language Model Outputs: Human Annotation, Computational Recovery, and LLM-Judge Sensitivity**

This repository is the public reproducibility package for the study. It is organized around a strict distinction between **exact numerical reproduction**, **historical bit-for-bit reruns**, and **fresh reconstructed reruns**.

## Release status

**PASS — the frozen reference release remains reproducible, and the later post-hoc validity/sensitivity layer is now exposed as browseable top-level code and result artifacts.** Historical runtime boundaries are documented explicitly where the original executable environment or immutable model revision was not retained. The original transport bundle remains immutable; post-hoc validity files added after that freeze live under `code/validity/` and `results/validity/`.

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
- exhaustive T4 mapping sensitivity (2 templates × all 6 bijections = 12 variants).\n- post-hoc annotator-to-adjudicated-reference T1–T4 concordance for IP&M submission contextualisation (not an independent human ceiling).

See `docs/VALIDITY_EXPERIMENTS_2026-09.md`, `docs/IPM_SUBMISSION_UPDATE_2026-09-18.md`, and the updated experiment reproducibility matrix. These analyses support narrower interpretation: **within-corpus recoverability under specified evidence, split, and evaluator protocols**, not generator-invariant understanding, architecture superiority, or external generalisation.

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

## IP&M R8 review-layer governance update (2026-09-19)

The later IP&M reviewer-driven follow-up layer (R1–R8) is exposed as browseable top-level `code/followup/`, `results/followup/`, and reviewer-revision documentation. After `UNPACK_RELEASE.py`, the current CPU verification path is:

```bash
python -m pip install -r requirements-cpu-repro.txt
python code/followup/P2_IPM_REPRODUCE_ALL_CURRENT_RESULTS.py
```

The default orchestrator recomputes the lightweight/point-support checks and verifies manuscript-used slow 2,000-replicate CI artifacts. Optional flags rerun the slow resampling jobs. It does not retrain M3/M4 or relabel FINAL GOLD.

A known historical metadata erratum is documented in `docs/IPM_KNOWN_PROVENANCE_ERRATA_R8.md`: the preserved FINAL GOLD v1.0 `SUMMARY` sheet contains a stale round-1 adjudication count of 394, whereas the reproducible six-field queue and provenance/workflow evidence establish 423. The historical binary is not silently overwritten.

**Double-anonymous review:** this public repository is identity-bearing and is not the anonymous reviewer-access route. A detached reviewer-safe snapshot is prepared separately for blinded review, with role-coded A1–A4 provenance and without personal names, affiliations, ORCID/profile identifiers, identifying source filenames, private correspondence, or author Git history.

Current governance records include `docs/IPM_CURRENT_EXPERIMENT_REPRODUCIBILITY_MATRIX_R8.csv`, `docs/IPM_FOLLOWUP_ARTIFACT_SHA256_R8.csv`, `docs/R8_REPRODUCIBILITY_EXECUTION_AUDIT.md`, and the R8 run-status JSON.

## R8A authorship and ethics resolution

The administrative item left open at the end of Reviewer #7 is resolved: the current manuscript has five co-authors; Authors 2–4 supplied the independent linguistic annotation layer and Author 5 supplied senior adjudication/targeted re-review. Ethics committee approval was not required for this methodological study, and the de-identified annotation/adjudication records are used and released for reproducibility with the co-authors' agreement. This update changes no scientific data, labels, folds, predictions, or reported results.

## R8A ethics and collaborator-governance closure

Under the author's institutional policy, formal ethics/IRB review is not required for this type of non-clinical methodological study; no separate formal exemption determination was required. The three annotators and senior adjudicator served as uncompensated volunteer research collaborators and agreed to research use of their judgments and de-identified public release of the corresponding records. The institution places no restriction on publication of the study-created data. Identifying professional provenance remains outside the blinded reviewer package. See `docs/IPM_ETHICS_DATA_RELEASE_GOVERNANCE_R8A.md`.
