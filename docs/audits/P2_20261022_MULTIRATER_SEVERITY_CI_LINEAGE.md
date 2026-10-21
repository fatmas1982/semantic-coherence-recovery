# Independent historical bootstrap CI lineage check — multirater severity (22 October 2026)

**Decision: Historical multi-rater CI PROVENANCE STILL OPEN; point estimates and pair-specific CI reproduction PASS. This is a scoped negative/reconciliation audit, not a blanket manuscript certification.**

## Verified input and previously established evidence
The immutable author-side GOLD file has SHA-256 `ccc910b7bafbfa9607e93ef2eba8605f56f7ed87460ef74892d4877c7db4de65` and contains 720 unique cases, 120 prompt clusters, and saved original A1/A2/A3 `Severity` columns (not adjudicated severity). It **was not uploaded by this commit**. Prior source-column calculations reproduced five three-rater Krippendorff alpha point estimates and 12/12 pair-specific 2,000-draw human agreement/kappa bootstrap interval outputs at archived precision. Full-sample ordinal alpha: 0.783964731; 445-case majority-failure alpha: 0.528337535.

## Six archived CI comparisons

| Subset and metric | Historical 95% CI | Independent nominal-protocol replay |
|---|---|---|
| all / ordinal alpha | 0.752–0.814 | 0.753–0.813 |
| all / Gwet AC2 | 0.716–0.787 | 0.717–0.786 |
| all / mean pairwise QWK | 0.760–0.819 | 0.761–0.819 |
| majority (445) / ordinal alpha | 0.470–0.586 | 0.469–0.582 |
| majority / Gwet AC2 | 0.647–0.744 | 0.646–0.743 |
| majority / mean pairwise QWK | 0.401–0.509 | 0.402–0.508 |

The independent candidate uses 2,000 task-stratified Prompt_ID-cluster resamples, `numpy.default_rng` (PCG64), seed `20260804`, with a fresh eligibility filter for the majority subset in each resample. **None of six complete intervals reproduced both printed endpoints at three decimals.** This is not evidence that a historical interval is necessarily wrong; it shows that the exact historic interval algorithm/RNG state remains unknown.

## Explicitly limited diagnostic alternative-protocol tests

All alternatives resampled whole prompts, not individual outputs; each used 2,000 repetitions. Complete historical intervals matched (out of six):
- Nominal task-stratified PCG64 seed 20260804: **0/6**.
- Pooled all-prompt PCG64 seed 20260804: **1/6**.
- Task-stratified legacy MT19937 seed 20260804: **0/6**.
- Pooled legacy MT19937 seed 20260804: **0/6**.
- Task-stratified PCG64 seed 20260908: **0/6**.

No alternative was selected as authoritative based on accidental proximity. The latter seed belongs to a *different* computational-bootstrap estimand and is a diagnostic negative control, not a proposed substitute.

## Manuscript implications
The latest author DOCX copies append a precise disclosure to the human reliability methods/provenance text. All scientific table-cell strings are byte-equivalent at the text level between prior and revised DOCX versions: **20/20 main, 80/80 supplement**. No historical confidence limits, alpha point values, or 3,000-draw E1/E2 results were changed.

- `P2_MAIN_MULTIRATER_CI_PROVENANCE_DISCLOSED_20261022.docx` SHA-256: `811c032350c361ce07d9482ce93fb802fc60ed8e4c0e9fef7cf28a56deafc3fc`, rendered 37 pages.
- `P2_SUPPLEMENT_MULTIRATER_CI_PROVENANCE_DISCLOSED_20261022.docx` SHA-256: `c91da7e6b9d5c2c7b21c5cdf2e62ac368b6b65d096640501c390d81a95fe5142`, rendered 51 pages.

Author DOCX binaries and private GOLD are deliberately **not deposited** to this public GitHub branch. The locally delivered reproducibility archive contains source-independent aggregated output, the sensitivity script, exact diff manifests and both author Word files, but **not the raw GOLD workbook or case-level ratings**.

## Unclosed gate
Find original historical multirater CI bootstrap script, input version/hash, resample draw ordering/quantile method, and execution record. Keep historical displayed CIs explicitly labelled as archived descriptive estimates without an exact independent CI replay. Do not claim all human intervals are reproducible; the **12 pair-specific** CIs are a different, successfully replayed artifact. No coauthor/ethics/journal approval is presumed.

**Overall release remains DRAFT / PARTIALLY VERIFIED.**
