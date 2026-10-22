# Independent source-to-manuscript alignment audit (22 October 2026)

Status: **REVIEW BRANCH; NOT FINAL, NOT AUTHOR APPROVAL, NOT A JOURNAL DEPOSIT.**

## Authority and manuscript release boundaries

- Scientific label authority: FINAL GOLD v1.0: 720 cases, 474 failures, 246 non-failures, 35 current ambiguity flags, and 120 six-output prompt clusters. Historical 36-flag subgroup is not the current denominator.
- Author-side latest reviewed Word candidate: **20 scientific main tables**, **80 supplement tables**. The publicly archived `docs/manuscript/MAIN_MANUSCRIPT_EXISTING_EVIDENCE_ONLY.docx` and `SUPPLEMENT_EXISTING_EVIDENCE_ONLY.docx` are **not binary or structural mirrors** of those candidate files: public checked-out copies have 18 and 86 tables, respectively. Do not claim these files correspond to the current author revision.
- Current author main copy includes an E1/E2 correction of **16 prose confidence intervals**, while the independent source verification inspected **20 paired E1/E2 rows** (10,408 case-level records). This update to authors' manuscript is **not published here**.
- The journal uses double-anonymized review. Do **not** deposit identifying title page, full author-side Word documents, private raw GOLD XLSX, or reviewer-only sensitive materials into this public branch merely to force binary parity. A private version-to-artifact map is required.

## Directly executed scoped numerical checks

- 68 archived model experiment central estimates match case-level OOF-derived metrics; historical 2,000-draw CIs for all 68 runs were previously reproduced with the archived sampling protocol; 136 endpoints matched.
- 20/20 E1/E2 3,000-draw paired-bootstrap source checks match printed precision; note only corrected displays are authoritative.
- 60/60 GEE result rows independently refitted and matched coefficients, standard errors and Wald intervals; 10,408 paired case rows, 20 comparisons, 11 source parts. **Three low-event flags** mean some inferential contrasts remain exploratory.
- 4/4 paired exact McNemar case-level checks match.
- 720/720 generated case alignment, 2,160 locked pre-resolution human ratings and archived OOF row integrity checks passed.
- `python code/analysis/verify_pinned_transport_hashes_20261022.py` directly checks **151/151 pinned transport members** without confusing historical immutable files with a checkout containing newer files. This does NOT certify private historical source XLSX content.

## Remaining blocking gates (after verified archived-input recovery)

1. **86 citations: still not certified sentence-by-sentence.** Existing bibliography and DOI discovery, primary landing pages, or topical agreement with abstracts are not proof that all cited claims are entailed by the actual publications. Restricted-access primary full text and compound multi-citation prose require item-level manual adjudication.
2. All reported results across 100 tables, narrative interpretations and all human agreement CIs require an explicit `claim -> frozen artifact -> reproducible calculation -> manuscript cell` ledger. Selective metric and CI replays cannot be generalized.
3. **RESOLVED, WITH PROVENANCE LIMITS:** An archived combined case-level M4 export has **18 named source_file groups, 9,460 rows and no duplicate (source_file, Case_ID)**. A new preparation script reconstructs these 18 logical OOF shards and creates **4 byte-identical aliases** from existing `10_OOF_T1.csv` through `13_OOF_T4.csv`. With the SHA-confirmed original private GOLD provided **locally only**, `code/followup/P2_IPM_REPRODUCE_ALL_CURRENT_RESULTS.py` completed the default reviewer-safe checks with **PASS**, and its `--recompute-slow-ci-followups` mode independently recomputed the adjudication-exclusion intervals and target human-reference checks with **PASS**. This is **archived-output reconstruction, not original M4 per-shard byte identity, inference, or retraining**. Follow-up pre-resolution annotator ambiguity counts of **36** are historical and must not be confused with FINAL GOLD's **35** flags.
4. Historical source-binary identities that are only attested by SHA lines, fully fresh model training/generation and coauthor authorization are separate gates.
5. The `code/analysis/verify_release_public_20261012.py` in recent main already recognizes mixed worktree versions; retained original files and current checkout checks are different tests. Additional pinned-transport integrity script in this branch is explicit about that distinction.

## Archived R8 reproducibility command (private run only)

```bash
python UNPACK_RELEASE.py
python code/analysis/prepare_followup_archived_inputs_20261022.py
# PRIVATELY copy user-owned checksum-confirmed GOLD v1.0 into data/frozen;
# never add it to Git or a public pull request.
python code/followup/P2_IPM_REPRODUCE_ALL_CURRENT_RESULTS.py --recompute-slow-ci-followups
```

Source report records 22 prepared files (18 M4 shards + four named baseline aliases). No historical per-shard byte-level equivalence is claimed. The slow-CI run was independently exercised in a private local copy and completed PASS.

## Publication instructions

Use this branch for verification code and public, deidentified audit notes only. Treat the author-side manuscript and supplement as a **private pair** until reviewer masking, source verification, final numerical crosswalk and all author sign-offs are completed. No `FINAL` tag, no unconditional `all tests pass` badge and no claim of complete 86/86 semantic certification.
