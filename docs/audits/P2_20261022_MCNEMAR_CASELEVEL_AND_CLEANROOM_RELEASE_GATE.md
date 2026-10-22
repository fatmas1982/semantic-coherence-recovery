# IP&M case-level McNemar closure and archived release clean-room replay
**2026-10-22 | SCOPED REPRODUCTION PASS; PUBLIC-RELEASE SELF-CONTAINMENT LIMITED.**

## Newly closed case-level M3-vs-M4 inference gap
A clean, independent case-by-case join was performed with:
- baseline M3-C OOF (`data/computational/m3/OOF_M3_T{1..4}_C_seed20260908.csv`), recovered from the frozen release archive inside the author-supplied `GITHUB_REPRODUCIBILITY_FINALIZATION_KIT(1).zip`;
- forced-choice M4-C OOF (`OOF_M4_FORCED_T{1..4}_C.csv`) recovered from the author-supplied `P2_55_M4_FORCED_CHOICE_RESULTS(1).zip`.

The same four M4 case files are also available within the archived frozen release. A fresh `Case_ID` 1:1 join verified full population, matching `Prompt_ID` and matching `y_true` in all 2,128 target-case records. Binary correctness was compared from **individual paired predictions**, not from manually transcribed discordant counts. Exact two-sided McNemar `p` was recalculated as `min(1, 2*Pr[Binomial(b+c,0.5)<=min(b,c)])`, with no continuity correction.

| Target | Matched N | M3 correct/M4 wrong | M3 wrong/M4 correct | Total discordant | Exact two-sided p | Source vs Supplement S61 |
|---|---:|---:|---:|---:|---:|---|
| T1 | 720 | 114 | 161 | 275 | 0.005442800476960387 | PASS |
| T2 | 474 | 144 | 70 | 214 | 4.68702099703565e-7 | PASS |
| T3 | 460 | 179 | 47 | 226 | 2.46694435974038e-19 | PASS |
| T4 | 474 | 186 | 80 | 266 | 6.82146139218376e-11 | PASS |

**4/4 source-paired counts and 4/4 exact test reports PASS**, including published `<.001` threshold rows. Supplement S61 **does not need numeric correction**. Correctness calculations reproduce M3-C/M4-C Macro-F1 point estimates respectively T1 .655264/.741073, T2 .777201/.609381, T3 .790805/.529736 and T4 .636871/.390764. There are **2,128 paired case-target records**, not 2,128 independent prompts.

Reproducible public script at `code/analysis/reproduce_m3_m4_mcnemar_caselevel_20261022.py` can be run after `python UNPACK_RELEASE.py`. The author-side audit includes a separate independently executed version plus full source pointers; the public documentation/script deliberately publishes no private annotator identities, emails, or additional raw case payload.

## New clean-room archived-bundle check, with exact boundary
The author-supplied **historical** `GITHUB_REPRODUCIBILITY_FINALIZATION_KIT(1).zip` contains a 186-member tar.xz. SHA-256 `a68f1be48e32b28a683431b093649999c9fb7f19af2130d87fca5f03f9f9260d` matched the archive's expected hash. Archive members were screened for absolute paths, traversal components and links before extraction in a newly created local directory. The supplied original `code/analysis/reproduce_public_metrics.py` then **PASS**-recomputed frozen M3-C/M4-C F1 and paired correctness.

However, the archival `code/analysis/verify_release.py` initially **FAILED** with FileNotFoundError because its `data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx` and `P2_CPU_Baselines_v1.0.xlsx` are **not included in the archival transport**. The independently supplied original binaries both matched their recorded source SHA-256 (`ccc910...4de65` and `4502e71...31163`), and the identical verifier then **PASSED** once those binaries were placed into a *private temporary test directory*. This does **not** mean the public archive is self-contained for that historical verifier, nor does it mean those binaries were publicly committed. Public `README.md` already explicitly discloses this; current `code/analysis/verify_release_public_20261012.py` provides a separate public-data verification route.

This old archival pass does not demonstrate that **all 4,960 current main-branch files**, whole Git history, latest 100 paper tables, latest GitHub HEAD actions, or entire GPU training/LLM inference can be reproduced from one clean checkout. No such claim is made.


## Bounded technical privacy/security preflight of historical 186-member transport

A new text-pattern scan was executed on the author-supplied historical 186-member transport. **13 Python files parsed successfully (0 syntax errors)**. Patterns screened: GitHub personal access token prefixes, AWS access-key identifiers, PEM private-key headers, assignment-like static secrets/passwords, email addresses and IPv4 strings. No matches to the tested credential/private-key/IPv4 patterns were observed. **Two email-address occurrences were detected in one historical supplementary Markdown file, `paper/P2_57_Submission_Candidate_SUPPLEMENT.md`.** This means that archived document cannot be called fully anonymous. The author independently asserts permission for public release, but that is a different matter from the existence of personally identifying details; it also cannot be reused unchanged for double-anonymized peer review. No emails or names are reprinted in this public report.

**Strong boundary:** This was a **heuristic text/content scan of the historical frozen transport**, not a check of all current main-branch GitHub files, nested server archives, commit history, generated notebooks, third-party binaries or semantic indirect identifiers. A zero-match result in the narrow rules above is not a guarantee that there are no secrets or sensitive information elsewhere.

## Existing scope unchanged
- 100/100 current Word scientific tables structurally retained and syntax-screened. **Full every-numeric-cell recomputation remains open**.
- Previous 210/210 bounded result-display/derived checks are still separate; the S61 correctness checks are newly upgraded from display-level arithmetic to **case-level** proof. Do not count every repeated display as a distinct experiment.
- S01 multirater human CI source replay PASS, S11 archived 24-run M3 support/hash/fold/probability validation PASS; original historical nested train-dev/feature-fit GPU runtime not fully replayed.
- Public-source privacy sweep is *partial* only; no whole-history credential/privacy certification.
- Original P2_38 locked input bytes and P2_40 intermediate provenance retained as previously disclosed limits.
- Latest author manuscripts stay controlled Word review candidates; no alteration to numerical table cells or release DOI/tag in this audit.

**Decision: S61 case-level McNemar GATE CLOSED; 2026-10-22 archived source metric replay GATE PASS subject to distinct historical binary dependency; overall IP&M submission-freeze GATE OPEN.**
