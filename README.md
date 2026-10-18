# Semantic Coherence Recovery — Reproducibility Release

**Reliable Evaluation of Semantic-Coherence Failures in Generated Text: Human Annotation, Computational Recovery, and LLM-Judge Sensitivity**

This repository is the public reproducibility package for the study. It is organized around a strict distinction between **exact numerical reproduction**, **historical bit-for-bit reruns**, and **fresh reconstructed reruns**.

## Release status

**DRAFT / PARTIALLY VERIFIED — independent execution evidence is available only for named modules; the full corrected manuscript-plus-supplement release is not yet frozen or coauthor-approved.** Historical runtime boundaries are documented explicitly where the original executable environment or immutable model revision was not retained. The original transport bundle remains immutable; post-hoc validity files added after that freeze live under `code/validity/` and `results/validity/`.

## IP&M statistical precision follow-up (2026-10-12; draft PR #2)

The **post-hoc 60-fit GEE stability audit** does not introduce new judge inference or additional tests. It refits the previously reported working-independence logistic GEEs on the frozen 10,408 paired case-comparison rows, verifies their original coefficients/p-values, and reports changed-event counts, robust log-OR SEs and *nominal* Wald 95% OR intervals. One Qwen–T1–E2 comparison has just 15 changed outcomes (the same events across three human axes). These diagnostics do **not** correct small-event bias or change the one original 60-test Holm result. See [rationale, methods and limitations](docs/GEE_STABILITY_POSTHOC_AUDIT_2026_10_12.md), [analysis code](code/validity/reanalyse_gee_stability_2026.py), and [archived 60-row output](results/validity_2026_10/HJI_GEE_STABILITY_60.csv). The completed manuscript/supplement Word edits are separate, coauthor-review artifacts and are not represented as merged into this repository.

## Current M3 and governance reconciliation

The completed later M3 dual-blocked macro-F1 values are 0.591/0.671/0.682/0.573, superseding initial September values for this comparison. See [run-level hashes and case-level rationale](docs/M3_DUAL_VERSION_RECONCILIATION_20261012.md). Review [experiment-to-table traceability](docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv) and [100-table caption inventory](docs/MAIN_SUPPLEMENT_100_TABLE_INVENTORY_20261012.csv). The corrected HJI percentile file is authoritative; historical CIs remain superseded. Coauthor, institutional and data-release approvals have not been independently verified.

## Latest independent integrity gates (2026-10-12)

The **draft branch** now has independently passing GitHub Actions for: (i) safe restoration and SHA-256 verification of the 86-fragment/151-entry immutable historical bundle, preservation of the updated checkout files, 720-case/2160-rating human layer and M0–M4 archived OOF case alignment; (ii) recomputation of frozen headline metrics; (iii) 60 corrected HJI percentile bootstrap contrasts; (iv) 60 GEE inference-stability fits; and (v) four complete-task M3 dual OOF macro-F1 calculations. See [scoped evidence and unclosed gates](docs/RELEASE_CANDIDATE_EVIDENCE_AND_GAPS_20261012.md) and the [33-row experiment matrix](docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv).

**Reproducibility is conditional on archived outputs.** Original XLSX/PDF historical source-binary hashes may be listed in `SOURCE_BINARY_HASHES.csv` even when the original binary itself is *not* in the public archive. The released CSV/text mirrors and actual source binaries are different artifacts. The optional historical `code/analysis/verify_release.py` assumes some undistributed original XLSX files; use `code/analysis/verify_release_public_20261012.py` and the independent CI for public archival verification instead. Original M0–M2 trainer and five historical generator reruns are not reproducible bit-for-bit. Some follow-up studies have released summaries without every historical raw case artifact. A preliminary pattern screen detected no emails/URLs/phone-like strings in the three core annotators' comment/evidence-note columns but does **not** constitute full de-identification, rights approval, or inspection of all fields.

**No final journal-ready certification, coauthor permission, institutional ethics determination, unconditional third-party-data license guarantee, blinded review approval, DOI, release tag or PR merge is claimed.**

## October 2026 integration and strict reproduction boundary

The October E1/E2/HJI reanalysis code, de-identified paired predictions, M3 dual-block reconciliation, CI workflows, statistical outputs and provenance documents are present on `main` as of commit `3d5ed1b`.

**Please do not assume that cloning the repository alone reproduces every result in the latest supplied manuscript.** The separately supplied October FP16 CPU/GPU binary archives and updated DOCX manuscripts have not all been uploaded to GitHub. A clone can reproduce only the named frozen and October modules for which public case-level inputs, executable producers, and pinned dependencies are present. Publication rights authorization is distinct from independent verification of numerical claims.

For frozen reference checks:

```bash
python UNPACK_RELEASE.py --verify-only
python UNPACK_RELEASE.py --historical-dir /tmp/semantic_frozen_reference
python UNPACK_RELEASE.py
python code/analysis/reproduce_public_metrics.py
python code/analysis/verify_all_frozen_case_layers_20261012.py
python code/analysis/audit_experiment_artifact_paths_20261012.py
```

The source release remains tied to the 86-part frozen archive. The default unpacker now preserves newer files already present in the checkout; use a separate directory for historical provenance. Interpret failures as blockers. Additional paths and status are recorded in `docs/RELEASE_AUDIT_STATUS_20261012.md`, `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv`, and the experimental protocol documentation. Distinguish reportable reference runs, reconstructed reruns, post-hoc sensitivity and unresolved FP16 results. Never replace reference results silently with a newer numerical variant.

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


## Final-results source precedence (2026-10-14)

For exact experiments archived in the author-designated `results.rar`, those archived outputs supersede older duplicate reports **only when the complete experiment identity matches**. Other experiments—including E1/E2 sensitivity and human–judge analyses—remain unchanged. This rule does not imply that `results.rar` or the latest `.docx` manuscripts have been uploaded to GitHub. See [the final-results provenance policy](docs/FINAL_RESULT_SCOPE_POLICY_20261014.md) and [scope matrix](docs/FINAL_RESULT_SCOPE_MATRIX_20261014.csv).


## Dedicated October 2026 server-run archive (published branch, not merged)

The `SERVER_RUN_20261007_A` CPU/GPU/EXPORTS archive was uploaded to the dedicated branch `publication/server-run-20261007-a` at initial commit `d9f97ae`. It contains 4,578 data files plus a per-file SHA-256 manifest and a run-specific README; `LOCAL_WORK` was deliberately excluded pending review. [Browse the uploaded archive](https://github.com/fatmas1982/semantic-coherence-recovery/tree/publication/server-run-20261007-a/results/server_runs/SERVER_RUN_20261007_A).

Operator-run local verification reported zero mismatches across 4,578 raw staged Git blobs and SHA-256 manifest entries; 70 outer and 68 nested ZIP archives were readable; limited text-based credential-pattern scans returned zero flagged files. Details, exact counts, and limitations appear in [the archive README](results/server_runs/SERVER_RUN_20261007_A/README.md) and [the publication audit](docs/PUBLICATION_REPRODUCIBILITY_AUDIT.md).

**Important:** This is verified archival transport **only**. It does not establish successful completion of all M1–M4 jobs, exact scientific reproduction, completeness of output coverage, clearance of every private/sensitive data type, coauthor approval, or readiness to merge to `main`. The older statement above that October FP16 CPU/GPU archives have not all been uploaded refers to completeness of the broader release; do not interpret this branch archive as closing every outstanding artifact gap. No frozen/reference estimate is silently replaced by these newer files.
