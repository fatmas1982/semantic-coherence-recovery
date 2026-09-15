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
- reportable notebooks/scripts, paper/supplement Markdown mirrors, hashes and this experiment-to-artifact matrix.

## Exactness by stage

- **Human annotation:** the exact original A1/A2/A3 binaries were recovered and hash-verified; the public GitHub layer releases complete sheet-by-sheet CSV mirrors, so all analytic secondary-label, evidence-span/note, ambiguity, HREF and comment fields are public and diff-friendly. Published core IAA must still be computed from locked pre-resolution A1/A2/A3 decisions only, never adjudicated `Final_*` fields.
- **Senior resolution:** the exact 423-case round-1 senior adjudication binary was recovered and hash-verified; the public GitHub layer releases complete CSV mirrors of all four workbook sheets. The targeted second re-review and FINAL GOLD remain separate downstream provenance layers.
- **M0/M1/M2:** paper numbers are exactly reproducible from archived OOF predictions. The original historical training script was not retained; `code/baselines/07_retrain_cpu_baselines_reconstructed.py` is a documented reconstruction and must not be described as the original executable.
- **M3:** reportable OOF predictions, seed stability, LOTO, leakage audits, source analyses and diagnostic outputs are retained with the executable notebook.
- **M4:** only the target-isolated forced-choice run is reportable. The earlier free-generation run remains under `archive/legacy_m4_invalid/` for audit only.
- **Generation:** all 720 paper-used outputs are exact and authoritative. Fresh generation for five of the six checkpoints remains best-effort because exact immutable repository revisions and every model-specific chat-template/tokenization/stopping detail were not retained.

## Remaining non-closures

Two historical-execution claims remain intentionally unavailable and must not be made:

1. **Bit-for-bit regeneration of five original SLM generation checkpoints.**
2. **Bit-for-bit retraining of the historical M0/M1/M2 CPU implementations from the original lost training script.**

Neither limitation blocks exact reproduction of the numerical results reported in the paper, because the authoritative frozen generated outputs and OOF predictions are released.

See `EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` for the experiment-by-experiment map.
