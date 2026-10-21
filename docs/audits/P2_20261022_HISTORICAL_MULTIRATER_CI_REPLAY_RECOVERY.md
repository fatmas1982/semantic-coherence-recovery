# Human inter-rater bootstrap CI — recovered historical source and independent replay

**22 October 2026 — SCOPED CI REPLAY PASS.** This report supersedes the earlier "multirater historical CI lineage open" conclusion for the six reported human severity intervals. It does **not** certify every manuscript table, complete original input-binary identity, six-field adjudication history, external human validity, or journal readiness.

## Source recovered and replayed
The user-supplied `P2_38_CL_Analysis_and_Verification_Package.zip` contains `scripts/run_all.py` and `outputs/tables/bootstrap_confidence_intervals.csv`; `P2_45_Computational_Linguistics_Authoritative_Recalculation_Complete_Package.zip` contains its corresponding source code, preserved data mirror and archived interval outputs.

Historical **human-reliability** algorithm:
- 2,000 `Prompt_ID` cluster-bootstrap draws **stratified by task**, `numpy.default_rng(20260804)`, prompt groups iterated in the source task/prompt ordering; sampled clusters retain all six checkpoint responses and three A1/A2/A3 pre-adjudication ratings.
- Within **each bootstrap replicate**, recompute the majority-failure subset as cases with at least two original *primary* ratings other than `NONE` (observed original n=445); this subset is **not** fixed at 445 inside every draw.
- Evaluate Krippendorff ordinal alpha, Gwet AC2, and mean pairwise quadratic-weighted Cohen kappa; take 2.5th/97.5th percentile endpoints. In particular this is **not** the later computational-OOF bootstrap convention with seed 20260908.
- Recovered archival P2_38 code SHA-256: `f7b6eade79d2b80afb8758f8763f9fc5eddd90a7534fead795a15630b7346b2b`; P2_45 code SHA-256: `4fdd8ceebabc7495d9b4da36dcd61c9c2b1015f8b2526150f080c0eeb2d0dac0`.

A fresh read-only replay in the analysis environment reproduced **15/15** archived interval records for P2_38 and **19/19** for P2_45 under numeric tolerance `1e-10`. All **six** reportable severity 95% CIs also agree at the manuscript's three-decimal precision. Tiny binary/decimal floating-point serialization differences (~1.1e-16) in a comparison crosswalk are numerically immaterial: do **not** claim byte-identical floating-point serialization.

## Six matched 95% confidence intervals

| Measure | 720-case all-sample CI | Majority-failure subset 445-case CI |
|---|---|---|
| Krippendorff ordinal alpha | [0.752, 0.814] | [0.470, 0.586] |
| Gwet AC2 | [0.716, 0.787] | [0.647, 0.744] |
| Mean pairwise QWK | [0.760, 0.819] | [0.401, 0.509] |

Full-precision endpoint crosswalk and replayed code are included in the author-facing verification ZIP. It does not include case-level records, original annotator workbooks, or the confidential GOLD workbook.

## Intermediate P2_40 status — excluded from selected numerical lineage

A divergent **intermediate** P2_40 CI output was observed. Its six complete CI intervals do not reproduce the selected P2_38/P2_45 endpoints at display precision. The cause has **not** been proven. P2_40 is therefore designated `HISTORICAL_INTERMEDIATE_NOT_REPORTING_SOURCE`, not an independently verified current source. It is retained for traceability and is **not deleted**, retroactively modified, called fraudulent, or silently interchanged with the selected result. The scope of this release is P2_38/P2_45 replay and current Word disclosure only; resolving P2_40's exact genesis is not required for adopting the source-reproduced selected CIs, provided this exclusion remains documented.

## Remaining version / methodological limitations
1. The exact original P2_38 `final_resolved_dataset_v1.2_locked.csv` binary, SHA-256 `9876be616c2d1d57a3a0683d2cb64fd07849ffed183b66c255ef52501e7a002e`, has **not** been recovered. P2_38 code was replayed with a checked reconstructed pre-resolution rating source (SHA-256 `5d0fa0385a1eaa7ab3916081864721d42b4dd6b39655c3568f14ff6b38ba85a6`), so the exact **numerical results** reproduce but historical input-binary identity is still open.
2. P2_45 replay input SHA-256 `d4b4dfad672b778b5b93d10812ce4f1a0108696e7ad8f6ce00b138f0a733b2c4`. Historical P2_45's adjudicated Computational Linguistics reference lists **452** failures; the current **P2 GOLD** is **474** failures. They are separate final-adjudication/reference versions and cannot be silently substituted. The reported human reliability bootstrap specifically uses original locked **A1–A3** pre-resolution ratings.
3. The human 2,000-draw seed `20260804`, frozen computational 2,000-draw seed `20260908`, later sensitivity 2,000-draw seed `20260928`, and E1/E2 selected **3,000**-draw seed `20261009` are distinct estimands and protocols. Reproducing the six human CIs does not close their separate gates.
4. Six-field original A1/A2/A3 → A4 route reconstruction, failed-run retry provenance, full all-100-table statistical audit, external human construct/criterion validation, and publication approvals remain separate gates.

## Author Word crosswalk / unchanged data
Author-only Word revisions dated 2026-10-22 correct the two preceding *non-reproducibility* disclosures, their obsolete headings, and narrowly worded open-gate clauses. **20/20 main** and **80/80 supplement** scientific table cell texts are preserved exactly; no GOLD case/rating, reported CI endpoint, model score, or E1/E2 value was changed. Rendered pages: **37 main, 51 supplement**. The author Word binaries are delivered privately in the chat, not silently committed to the public repository.

## Interpretation
**Human multirater historical CI replay gate: PASS at numeric interval scope.** P2_40 = archived intermediate, not a reporting source. **Overall P2 paper = PARTIALLY VERIFIED, not submission-approved.**
