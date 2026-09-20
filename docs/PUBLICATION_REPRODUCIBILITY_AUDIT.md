# Publication Reproducibility Audit

This audit separates three levels that must not be conflated:

1. **Exact result reproduction** — recompute every reportable statistic from frozen case-level, workbook or OOF artifacts.
2. **Exact historical rerun** — rerun the original generation/training implementation bit-for-bit.
3. **Fresh reconstructed rerun** — rerun a documented reconstruction where the historical executable or every runtime detail was not retained.

## Final closure status

**PASS for numerical reproducibility of the paper and supplement, subject to the explicit historical-rerun boundaries below.**

The current release now contains:

- the 120-prompt bank and 720-row prompt×model generation plan;
- all 720 authoritative retained generated outputs plus per-model raw output files;
- complete sheet-by-sheet CSV mirrors of the three recovered historical A1/A2/A3 workbooks;
- complete sheet-by-sheet CSV mirrors of the recovered round-1 senior adjudication workbook;
- the targeted second re-review workbook;
- FINAL GOLD v1.0 and the frozen CPU-baseline workbook;
- M0/M1/M2 archived OOF predictions and an explicitly reconstructed retraining script;
- M3 reportable A/B/C OOF, stability-seed OOF, LOTO case-level outputs, leakage/source/error analyses;
- M4 valid target-isolated forced-choice A/B/C OOF and summaries;
- legacy invalid free-generation M4 under an audit-only archive;
- follow-up source-utility and human-machine uncertainty outputs;
- a separately exposed post-hoc validity/sensitivity layer containing generator-signature and metadata-only diagnostics, strict M1/M3 dual blocking, source-bearing-only B→C restriction, ModernBERT token/truncation audit, manual high-similarity review, Qwen3-8B protocol perturbations, and exhaustive T4 answer-code permutations;
- reportable notebooks/scripts, paper/supplement Markdown mirrors, hashes and this experiment-to-artifact matrix.

## Exactness by stage

- **Human annotation:** the exact original A1/A2/A3 binaries were recovered and hash-verified; the public GitHub layer releases complete sheet-by-sheet CSV mirrors, so all analytic secondary-label, evidence-span/note, ambiguity, HREF and comment fields are public and diff-friendly. Published core IAA must still be computed from locked pre-resolution A1/A2/A3 decisions only, never adjudicated `Final_*` fields.
- **Senior resolution:** the exact 423-case round-1 senior adjudication binary was recovered and hash-verified; the public GitHub layer releases complete CSV mirrors of all four workbook sheets. The targeted second re-review and FINAL GOLD remain separate downstream provenance layers.
- **M0/M1/M2:** paper numbers are exactly reproducible from archived OOF predictions. The original historical training script was not retained; `code/baselines/07_retrain_cpu_baselines_reconstructed.py` is a documented reconstruction and must not be described as the original executable.
- **M3:** reportable OOF predictions, seed stability, LOTO, leakage audits, source analyses and diagnostic outputs are retained with the executable notebook.
- **M4:** only the target-isolated forced-choice run is reportable as the reference result. The later P1/P2 and answer-code perturbations are post-hoc protocol-sensitivity analyses; the P1/identity reference reproduces exactly before perturbations are interpreted. The earlier free-generation run remains under `archive/legacy_m4_invalid/` for audit only.
- **Post-hoc validity layer:** these files live under `code/validity/` and `results/validity/` outside the immutable 86-part transport bundle. They test threats to interpretation and do not replace the frozen reference analyses or constitute external validation.
- **Generation:** all 720 paper-used outputs are exact and authoritative. Fresh generation for five of the six checkpoints remains best-effort because exact immutable repository revisions and every model-specific chat-template/tokenization/stopping detail were not retained.

## Remaining non-closures

Two historical-execution claims remain intentionally unavailable and must not be made:

1. **Bit-for-bit regeneration of five original SLM generation checkpoints.**
2. **Bit-for-bit retraining of the historical M0/M1/M2 CPU implementations from the original lost training script.**

Neither limitation blocks exact reproduction of the numerical results reported in the paper, because the authoritative frozen generated outputs and OOF predictions are released.

See `EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` for the experiment-by-experiment map.

## Post-hoc validity closure

The 2026-09 validity layer is now publicly browsable and includes case-level or OOF outputs wherever applicable. Key verified summaries are:

- anonymous generator recovery with character TF-IDF: macro-F1 0.536;
- M3 strict dual-blocked macro-F1: 0.553 / 0.675 / 0.701 / 0.601 for T1–T4;
- Condition-C token audit: median 122, p95 378, maximum 446, no case above 1024;
- exact M4 P1/identity reference reproduction before protocol perturbation;
- exhaustive T4 mapping sensitivity: 12 variants, macro-F1 range 0.206–0.413 and QWK range 0.006–0.401.

These results narrow interpretation to within-corpus recoverability under specified evidence, split, and evaluator protocols.

## IP&M R8 reproducibility/governance addendum

The R1–R8 reviewer-driven follow-up layer is maintained separately from the immutable base transport bundle. A one-command CPU orchestrator now verifies/recomputes the current follow-up layer without retraining M3/M4 or relabelling FINAL GOLD. Its default reviewer-safe execution returned `PASS_CURRENT_R8_REVIEWER_SAFE_CHECKS`.

The R8 governance audit also identified one stale historical workflow-summary cell: the preserved FINAL GOLD v1.0 `SUMMARY` sheet says 394 round-1 adjudication cases, but the reproducible six-field queue, provenance layer, and senior-adjudication workflow establish 423. The historical source binary remains unchanged; the discrepancy is recorded as a metadata erratum and does not change any scientific case-level field or reported result.

For double-anonymous review, the identity-bearing public GitHub repository is not used as the reviewer-facing anonymous route. A detached sanitized snapshot retains the same scientific rows/predictions while replacing identifying provenance with A1–A4 role labels and excluding author/rater identifiers and Git history.

Current R8 follow-up governance artifacts are listed in `docs/IPM_CURRENT_EXPERIMENT_REPRODUCIBILITY_MATRIX_R8.csv` and hashed in `docs/IPM_FOLLOWUP_ARTIFACT_SHA256_R8.csv`.
