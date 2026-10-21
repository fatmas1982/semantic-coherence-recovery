> **22 OCTOBER 2026 UPDATE:** The historical *multirater* severity CI gate left open below was **subsequently resolved at numeric replay scope** by recovering the P2_38 and P2_45 original bootstrap code. Independent replays match 15/15 and 19/19 archived interval records, including all six published severity intervals (tolerance <1e-10). See [source recovery](P2_20261022_HISTORICAL_MULTIRATER_CI_REPLAY_RECOVERY.md). The original P2_38 input binary, six-field adjudication reconstruction and external human validation remain open. This October 21 source-column audit is preserved as a dated snapshot, not silently rewritten.

---

# P2 — independently recomputed pre-resolution human reliability from frozen GOLD (21 October 2026)

**Status: 5/5 Krippendorff alpha POINT estimates PASS; 12/12 pairwise Cohen κ / QWK and 2,000-cluster-bootstrap CI rows PASS; historical three-rater CI lineage OPEN.** This is not a claim of complete annotation provenance or external validity.

## Locked source, data scope and identity

The author-owned `P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx` has SHA-256 `ccc910b7bafbfa9607e93ef2eba8605f56f7ed87460ef74892d4877c7db4de65`, matching the historical registered source binary. The `FINAL_GOLD` sheet contains 720 unique Case_IDs, 120 Prompt_ID clusters with six cases each, and 720×3 saved **pre-resolution** A1/A2/A3 `Primary`, `Boundary`, and `Severity` values. Calculations read *these saved rater fields only*, never adjudicated `Final_*` labels. These three preserved fields are **not** a substitute for all six fields in the original A1/A2/A3 source workbooks; complete six-field routing/adjudication provenance remains open. No raw per-case data are published by this commit.

## 3-rater Krippendorff α from saved rater values

| Dimension | Independently recomputed | Reported (6 dp) |
|---|---:|---:|
| Fine primary, nominal | 0.703147201 | 0.703147 |
| Collapsed family, nominal | 0.730530469 | 0.730530 |
| Grounding boundary, nominal | 0.723208183 | 0.723208 |
| Severity ordinal | 0.783964731 | 0.783965 |
| Severity nominal (diagnostic) | 0.596477532 | 0.596478 |

All five values agree to six decimals. Nominal alpha uses pooled coincidence disagreement; ordinal severity uses Krippendorff cumulative-frequency ordinal distance.

## Pairwise source replication including 95% bootstrap intervals

All **12** pair-by-dimension rows (A1–A2, A1–A3, A2–A3 × fine label / family / boundary / severity) reproduce exact agreement, Cohen κ or quadratic-weighted Cohen κ, and **all recorded associated percentile CI fields**, along with within-one agreement/CI when applicable, using **2,000 task-stratified Prompt_ID-cluster resamples, seed 20260804**. The largest absolute difference versus the archived `results/followup/P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv` (Git blob `749de50b40f076f56aebcc7ab5b73d00f69fbf69`) is less than **5×10⁻¹⁰**. This is a new independent source-field computation, not merely re-reading the archived output. **Do not confuse this 2,000-draw human bootstrap with the 3,000-draw E1/E2 sensitivity bootstrap (seed 20261009).**

## Source-derived agreement and 445-case severity subset

Independent nominal Fleiss κ and Gwet AC1 reproduce the supplement's fine-label, family and boundary point estimates at three decimals. The severity *majority-failure subset* can be reconstructed by requiring **at least two of the three saved rater severity scores >0**; exactly **445 cases** qualify.

| Severity statistic | All 720 | Majority-failure 445 |
|---|---:|---:|
| Exact agreement | 0.605556 | 0.501124 |
| Within-one agreement | 0.850000 | 0.817978 |
| Mean score spread | 0.597222 | 0.766292 |
| Ordinal Krippendorff α | 0.783965 | 0.528338 |
| Gwet AC2 | 0.752003 | 0.694973 |
| Mean pairwise QWK | 0.790462 | 0.454342 |

All point estimates agree with rounded manuscript figures.

## Important unresolved interval provenance

An independently coded **2,000 task-stratified Prompt_ID** bootstrap with seed **20260804** yields multi-rater severity percentile CIs that are *similar to but not identical at the manuscript's three-decimal precision*:

| Severity | Manuscript CI | Fresh independent diagnostic CI |
|---|---|---|
| All ordinal α | 0.752–0.814 | 0.753–0.813 |
| All Gwet AC2 | 0.716–0.787 | 0.717–0.786 |
| All mean QWK | 0.760–0.819 | 0.761–0.819 |
| Majority ordinal α | 0.470–0.586 | 0.469–0.582 |
| Majority Gwet AC2 | 0.647–0.744 | 0.646–0.743 |
| Majority mean QWK | 0.401–0.509 | 0.402–0.508 |

Those *diagnostic own-implementation intervals are NOT source-certified replacements* for manuscript CIs. Historical RNG stream, sampler order, statistic implementation or dataset revision must be traced before any automated change to Word. Point estimates and archived **pairwise** intervals have passed. Do not announce complete multi-rater CI certification.

## Remaining gates and publication boundary

- Complete original six-field A1/A2/A3 archival mirrors (and original binaries, where possible) and 297/423 adjudication routing were not replayed here. The de-identified CSV mirrors are described in `docs/HUMAN_REFERENCE_INTERNAL_AUDIT_DISCLOSURE_20261017.md` as stored inside an **unpacked historical transport bundle**, not as direct standalone paths in the main Git tree.
- Subset-specific and multi-rater CI historical code/source implementation is not reconciled.
- External independent human construct/criterion validation is **not conducted**.
- No source annotations, model outputs, GOLD workbook or raw ZIP files have been deposited in this note.
- No model was retrained and no manuscript figure/table was modified.

**Release decision: close source-field point-estimate reliability and paired human CI verification only; keep historical multi-rater CIs, six-field process provenance and external validation OPEN.**