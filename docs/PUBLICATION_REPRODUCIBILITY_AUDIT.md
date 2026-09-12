# Publication Reproducibility Audit

This audit separates three levels that must not be conflated:

1. **Exact result reproduction** — recompute every reportable statistic from frozen case-level or OOF artifacts.
2. **Exact historical rerun** — rerun the original training/generation implementation bit-for-bit.
3. **Fresh reconstructed rerun** — rerun a documented reconstruction where the historical executable was not retained.

## Audit result

- Human core IAA: exact from the frozen A1/A2/A3 primary/boundary/severity fields.
- FINAL GOLD and target populations: exact frozen publication layer.
- M0/M1/M2 paper numbers: exact from archived OOF predictions; the historical baseline training script was not retained, so fresh retraining is explicitly labelled reconstructed.
- M3: executable notebook + reportable OOF, stability, ablations, LOTO, leakage, class/boundary/source diagnostics retained.
- M4: executable target-isolated forced-choice notebook + full-population OOF retained. Legacy free-generation M4 is audit-only.
- Follow-up source-utility and entropy analyses: executable standalone Python + Colab notebook retained.
- Generation: all 720 outputs are frozen. Fresh generation code is a documented reconstruction for five checkpoints; RWKV/M05 settings are more completely retained. No bit-for-bit claim is made where revision/template details are missing.

## Missing historical artifacts

The original full A1/A2/A3 workbooks and the separate round-1 senior adjudication workbook were located in the user's Library, but programmatic materialization returned HTTP 403 in the repository-build environment. They are therefore **not silently reconstructed**. The public package instead releases all recoverable core pre-resolution ratings preserved in FINAL GOLD and the available targeted re-review workbook. Workbook-only secondary/evidence/ambiguity fields remain outside the public reproducibility layer unless the original files are later supplied through an accessible export.

See `EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` for the experiment-by-experiment mapping.
