# Human-reference internal audit and disclosure (17 October 2026)

## Scope and status

**INTERNAL ARCHIVAL CONSISTENCY: PARTIALLY VERIFIED. EXTERNAL INDEPENDENT HUMAN VALIDATION: NOT CONDUCTED. NO CLAIM OF FULL VALIDATION.**

This addendum records an evidence-scoped audit of the frozen `P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx` workbook and a three-file derivative audit package (`ANNOTATION_GATES.csv`, `TARGETED_29_FIELD_CHANGE_AUDIT.csv`, `HUMAN_REFERENCE_VALIDATION_REPORT.md`). It does **not** supersede the freeze, the original annotation files, or existing paper results. In the authors' local audit the original GOLD binary matched SHA-256 `ccc910b7bafbfa9607e93ef2eba8605f56f7ed87460ef74892d4877c7db4de65`. The supplied derivative ZIP matched `cd2dd3c4514643f70a5118949f448a67425ee1db5ed729383e6d96dbe5e88d3c`. These assertions are **reported from the local run**; this GitHub commit does not represent a fresh CI execution of these binaries.

## Recorded audit results

- GOLD: 720 case identifiers, unique; 120 prompt clusters; 474 final failures and 246 non-failures.
- Frozen provenance: 297 three-annotator consensus-path cases and 423 adjudication-path cases. The latter include 394 round-one decisions and 29 targeted review cases (27 revised and two confirmed).
- The 29 reviewed case identifiers were located in GOLD and their five available final fields (primary, secondary, boundary, severity, and HREF subtype) matched the review-closure fields.
- A separate consistency worksheet documents four deterministic primary/secondary ordering normalisations. The 29-case derivative field-change sheet reports 23 *primary-label* changes; **27 revised cases does not mean 27 primary-label changes**.
- In the final GOLD, 383 cases show unanimous A1–A3 values across three preserved columns (primary, boundary, severity). The 297 historical consensus-path count **cannot** be independently derived from only those three columns, because the original route rule used six fields.

A first trial of the consistency test counted a field within the targeted review worksheet (2) instead of the separate `CONSISTENCY_AUDIT` worksheet (4). The correction of this *test scope error* is disclosed; the underlying GOLD was not edited. The final local audit reported 21 passing assertions within its limited input scope. The checks are not proof of semantic label validity.

## Historical annotator and adjudicator sources already published

After executing the verified `UNPACK_RELEASE.py` workflow, the repository contains these historical **de-identified CSV analytic mirrors**:

- `data/annotation/historical_full_csv/A1/Annotation.csv`
- `data/annotation/historical_full_csv/A2/Annotation.csv`
- `data/annotation/historical_full_csv/A3/Annotation.csv`
- `data/annotation/historical_full_csv/ROUND1_ADJ/Adjudication.csv`

Those mirrors live in the **reconstructed transport bundle**; their absence from an unexpanded Git checkout is not proof that they were never released. Original source-binary hashes are recorded in `SOURCE_BINARY_HASHES.csv`. Source binaries and CSV mirrors are **different artefacts**. Some original XLSX/PDF binaries are **not** publicly included. Do not claim that all original binaries are available. Publication authorization, privacy de-identification, professional provenance, and dataset reuse licensing must be verified separately.

## Remaining INTERNAL gates (not certified by this addendum)

1. Replay each original six-field A1–A3 sheet and the A4 historical adjudication sheet from the restored bundle, with file hashes, case-level keys, missing values, and duplicate checks.
2. Independently reconstruct the historical six-field 297/423 routing rule and reconcile all A4 decision transitions, without overwriting the immutable reference.
3. Recompute pre-resolution inter-annotator reliability and uncertainty intervals from historical source sheets under the stated missing-value / ordinal-distance specifications; compare to reportable estimates.
4. Reconcile every headline statement, table, supplement result, and manuscript version with frozen numeric source artefacts; use the latest author-approved files.
5. Perform complete confidential-data review, rights/ethics clearance, and page-by-page final manuscript QA before publication.

External independent human construct/criterion validation is deliberately deferred to future work, using independent experts, an a priori protocol and blinded materials; no observations or approval from such a future study exist.

## Approved cautious characterization

> The study uses a senior-adjudicated operational human reference, supported by pre-resolution internal reliability analyses and documented archival-integrity checks. External independent human validation was not conducted and is proposed for future work. Internal agreement, adjudication, hash matches, and computational out-of-fold analyses do not by themselves prove construct or criterion validity.

**Release decision: documentation and historical materials only; this is NOT a certification of a fully independently validated human reference, nor of journal readiness.**
