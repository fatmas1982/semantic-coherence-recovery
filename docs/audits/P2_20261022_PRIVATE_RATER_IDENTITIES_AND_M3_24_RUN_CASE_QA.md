# IP&M human-rating identity provenance and fresh 24-run M3 case-level audit

**2026-10-22 — BOUNDED PASS.** This public document deliberately **does not reproduce individual contributor names, contact addresses, ORCID identifiers or the unredacted email PDFs**. A separate private author record contains those details. Do not infer a mapping from contributor names to A1/A2/A3 pseudonyms.

## Human rating and senior adjudication roles

The corresponding author provided dated email replies establishing names, affiliations and contact details for **three primary independent human annotators and one separate senior adjudicator**. Their names/contact details are retained only in the controlled author-side documentation, **not deposited here**. The user explicitly confirmed that the three initial annotators supplied the independent assessments and the fourth contributor was the one senior adjudicator. The provided four email screenshots do not establish which primary annotator is A1, A2, or A3; therefore, the mapping remains **unverified and pseudonymised**. The email replies do not by themselves establish final author byline order or exact-version signoff.

Scientific analytic interpretation (unchanged): **720 cases × three independent primary raters = 2,160 pre-resolution rating records**; **A4 is not a fourth independent rater** for multirater alpha, AC2 or QWK. Senior adjudication of 423 flagged cases and 29 targeted re-reviews is separate. A4 adjudication does not imply an independent external validation cohort.

## Independently executed new M3 archive checks (same date)

Input: author-supplied `IPM_M3_GITHUB_PUBLICATION_20261015(1).zip`, source `release_files/results/m3_historical_20261015/oof/`, accompanying `RELEASE_SHA256_MANIFEST.csv`.

- **24/24** `OOF_M3_*` source files parsed: 4 target populations × (one dual + five size-matched) = **12,768** case-level prediction records (6 runs × [720 + 474 + 460 + 474]).
- **24/24** source-file SHA-256 hashes and byte lengths matched their **preserved in-archive release manifest**. This is a fresh crosscheck against that supplied source package, not a live byte-by-byte scan of the public GitHub checkout or a newly run GPU trainer.
- Across the 24 files: **0** duplicate Case_ID within run, **0** Prompt_ID groups assigned across different folds within run, **0** missing required case/prompt/fold/gold/prediction cells, **0** invalid selected-epoch values outside 1–8, and exact cross-run alignment of case-level gold, prompt, fold, task and generator strata within each target.
- **0** stored probability-vector sum errors exceeding tolerance `1e-4`, **0** mismatches between the stored predicted class and `argmax(probabilities)` after decoding the target-specific integer class origin. T1–T3 label origin is **0**, and T4 label origin is **1**. An unadjusted T4 argmax would spuriously flag exactly **2,844** (474 × 6) apparent disagreements: these are a **label-indexing artifact**, not model prediction errors.
- Independently recomputed dual macro-F1: T1 **0.5913225257153932**, T2 **0.671147712324077**, T3 **0.68183570135006**, T4 **0.5732726099821898**; the numbers reproduce the frozen M3 dual point estimates.

**Additional clean held-out training-support check:** For each of the 24 OOF runs, all **30** held-out (outer_fold, generator_stratum) cells were populated (**720/720** total). A fresh computation from each run's held-out fold and held-out generator compared the recorded `train_n` for **all 12,768 test-case records** with the number of rows eligible under dual blocking; **zero mismatches**, including the size-matched controls. Recorded `inner_dev_fold` matched the source-worker's deterministic next-fold convention for all test-case records; **zero mismatches**. This strengthens *archived support accounting*, not proof that the inner trained model saw only those rows in every historical process.

This check establishes integrity of archived **held-out outputs and fold accounting**. It does **not** re-execute the historical inner CV, feature-fit, tokenizer, model-training and early-stop pipelines, nor recover failed-to-successful server retry lineage. Historical nested-selection causal independence remains a separate gate.

## Edit/release scope

No annotations, labels, model predictions or scientific table cells were modified. The author-side package supplies a private name/email/affiliation/ORCID ledger for these four contributors, an unsigned authorship/CRediT title-page **worksheet**, a documented attribution boundary, an executable independent M3 archived-output check and its two detailed 24-run reports. Since the journal's anonymization route is not independently confirmed, names are deliberately excluded from the reviewer manuscript and this public audit.

**Result:** Rater-role distinction and **M3 OOF manifest/probability/fold gate PASS**, with explicit unresolved A1–A3 person-code mapping, byline order, nested historical trainer trace and whole-manuscript numeric certification.
