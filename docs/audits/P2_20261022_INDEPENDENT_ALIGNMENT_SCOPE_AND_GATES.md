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

## Remaining blocking gates

1. **86 citations: still not certified sentence-by-sentence.** Existing bibliography and DOI discovery, primary landing pages, or topical agreement with abstracts are not proof that all cited claims are entailed by the actual publications. Restricted-access primary full text and compound multi-citation prose require item-level manual adjudication.
2. All reported results across 100 tables, narrative interpretations and all human agreement CIs require an explicit `claim -> frozen artifact -> reproducible calculation -> manuscript cell` ledger. Selective metric and CI replays cannot be generalized.
3. The orchestrator `code/followup/P2_IPM_REPRODUCE_ALL_CURRENT_RESULTS.py` does **not** complete on the unpacked public checkout: after locally supplying the SHA-confirmed private GOLD file, it stops at missing `OOF_M4_SENS_T1_P1_identity.csv`. This M4 sensitivity-file source must be reconciled; do not silently replace it with another model run.
4. Historical source-binary identities that are only attested by SHA lines, fully fresh model training/generation and coauthor authorization are separate gates.
5. The `code/analysis/verify_release_public_20261012.py` in recent main already recognizes mixed worktree versions; retained original files and current checkout checks are different tests. Additional pinned-transport integrity script in this branch is explicit about that distinction.

## Publication instructions

Use this branch for verification code and public, deidentified audit notes only. Treat the author-side manuscript and supplement as a **private pair** until reviewer masking, source verification, final numerical crosswalk and all author sign-offs are completed. No `FINAL` tag, no unconditional `all tests pass` badge and no claim of complete 86/86 semantic certification.
