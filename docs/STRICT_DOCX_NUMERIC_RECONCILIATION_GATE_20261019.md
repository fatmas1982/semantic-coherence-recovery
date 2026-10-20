# Strict DOCX numeric reconciliation checkpoint (2026-10-19)

**NOT A TABLE-LEVEL PASS.** This report was derived from the author-supplied `P2_MAIN_LLM_JUDGE_PROTOCOL_REVISED_20261017(1).docx`, `P2_SUPPLEMENT_LLM_JUDGE_PROTOCOL_REVISED_20261017(1).docx`, and an earlier operator-run diagnostic ZIP `P2_RUN_PROVENANCE_MANUSCRIPT_RECONCILIATION.zip`.

- Indexed **20 main + 80 supplement tables**, with **4,103 nonempty Word table cells**.
- Read **8 frozen-reference metric rows** and **56 October server-run OOF metric rows** from the existing audit ZIP; these were **not re-executed** here.
- Localized **185 rounded numeric coincidences** distributed across **22 distinct tables** (**56 main candidate locations, 129 supplement candidate locations**).
- **0/100 tables certified by this stage.** Coincident numbers, especially at three decimal places, do NOT establish identical target, condition, seed, split, metric denominator, evaluation code, or confidence interval.
- No source result files, annotations, predictions, Word manuscripts, or supplement figures were changed.
- The full downloadable evidence package includes `NUMERIC_CANDIDATE_CROSSWALK.csv`, `STRICT_100_TABLE_CLOSURE_GATE.csv`, `OOF_RECALCULATION_EVIDENCE.csv`, Word file SHA-256 values and a scope-limited report. These CSVs **are not yet deposited in this repository**.
- Original ML / Model-Engineering Reviewer implementation ZIP and corrections remain to be checked issue-by-issue; the index/ledger is not a substitute for such a check.

## Mandatory closure
Require exact reviewer recommendation → versioned code → protocol key → frozen case-level input → newly recomputed output → specific paper table/claim and tests/CI, then assign VERIFIED / MISMATCH / NOT REPRODUCIBLE / NOT APPLICABLE. Keep FP16 reference, E1/E2, dual-blocking, size matching, and historical M3/M4 reference results as separate protocol identities. Incomplete historical retry chain and FP16 T1 serialization discrepancy remain explicitly OPEN.

**Disposition:** paper-wide numerical and model-engineering reviewer closure **NOT VERIFIED**.
