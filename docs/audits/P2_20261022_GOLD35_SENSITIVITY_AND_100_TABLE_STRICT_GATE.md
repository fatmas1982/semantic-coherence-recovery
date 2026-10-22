# IP&M 2026-10-22 — Current GOLD ambiguity repair and strict 100-table release gate

**Decision: Source-version contamination CORRECTED in private Word review candidate, independently recalculated. Overall 100-table full-source and all-Git-history security certification REMAIN OPEN. This is not a journal-final tagged release.**

## Definitive immutable source / historical mix-up

Current P2 GOLD v1.0 original XLSX SHA-256 `ccc910b7bafbfa9607e93ef2eba8605f56f7ed87460ef74892d4877c7db4de65`: 720 cases, 474 failure, `Final_Ambiguity_Flag=yes` **35 cases**. P2_45's distinct Computational Linguistics final label reference had 452 failures and **36** `final_ambiguity_flag=yes` cases. A 720-Case_ID one-to-one comparison finds **three common yes cases, 33 legacy-only yes, and 32 current-only yes**. They represent substantially different post-adjudication definitions, not rounding.

The previous P2 manuscript claimed **36 (5.0%)** explicit ambiguous cases and the Supplement S16A/S18A reported subgroup n=36/684/414, while the current GOLD is n=35/685/426 (last = majority-failure excluding 35 current flagged). The former task-level S20 percentages exactly matched the legacy 36-case task distribution: `2,2,10,5,3,14` (in order Explanation, Instruction following, Multi-entity tracking, Question answering, Source-grounded generation, Summarisation). Current task-level counts: `21,3,5,0,5,1`, percentages `17.5%, 2.5%, 4.2%, 0.0%, 4.2%, 0.8%`.

The original historical `run_all.py` nominal, Fleiss κ, AC1 and ordinal alpha formulas were loaded; with the old 36-case membership they recapitulated all previously published subgroup point estimates at three decimal places. They were independently recomputed with the **current 35-case GOLD flag** without changing any A1/A2/A3 input labels. Current ordinal severity alpha: flagged n=35 **0.003509792** (exact agreement **2.857%**), nonflagged n=685 **0.798015486** (exact **63.504%**), majority-failure nonflagged n=426 **0.513154023** (exact **52.113%**). Old historical .560/.793/.532 values must NOT be labeled current-GOLD sensitivity.

**Author-side private Word corrections:** 2 MAIN scientific prose paragraphs, 3 SUPPLEMENT scientific tables (S16A, S18A, S20), plus one explicit version-lineage note. MAIN **20/20** table structures and text grids unchanged. SUPPLEMENT **80/80** tables retained; exactly these 3 table grids changed. Renders: MAIN **34 pages**, SUPPLEMENT **47 pages**. No GOLD labels, old six accepted human bootstrap intervals, M0-M4 OOF predictions, or other table values changed. Do not distribute these author Word files silently on the public repository.

## Fresh full cell inventory and source checks

- **20 MAIN + 80 SUPPLEMENT = 100 Word tables, 4,103 nonempty cells**.
- Fresh direct per-metric numeric-source crosscheck on corrected Word files: **453/453 PASS, 0 mismatches**, covering **397 unique physical Word table cells** across **19 source-matched Supplement table indices**; 3,706 other nonempty cells have **NO FRESH DIRECT SOURCE CHECK** in this new pass. Previous bounded 210/210 source/display checks and other historical audit scopes remain valid separately, and must not be aggregated as independent tests.
- **Caution:** not all cells contain a scientific value, and neither the syntax audit of all 100 tables nor 453 scoped direct checks constitutes **all-scientific-values source validation**. Remaining source-to-claim checks, reviewer evidence-family closures and protocol lineage remain open.

## Human rating provenance (private/person-code crosswalk)

The restricted P2_45 original A1/A2/A3 person-named workbook archive and locked intermediate were inspected. The nine saved A1/A2/A3 primary, boundary and severity columns **match all 720 case IDs against current GOLD** (0 differences across 6,480 comparable values). Author contributor identities and person-to-rater-code mapping are supported by the restricted archive **but are not included in this public report**, to avoid new person-code leakage; the user-approved six-author byline and CRediT are in a private author-facing file.

## Repository all-files + all-commit-history limit

The inspected `main` HEAD recursive Git tree was non-truncated and enumerated **4,965 tracked files** of about **57 MB** in Git blobs at the inspected snapshot, including **70 ZIP archives, a RAR file, large logs, notebook files, and binary model material**; 175 chronological main-branch commit records were enumerated by pagination. **Enumerating metadata does not scan every content byte**, nested archive, binary, or earlier-revision deleted/reverted secret. The connected GitHub tool does not provide bulk binary downloads for the entire repo; local `git clone` failed host DNS, so the required all-current-archive + all-commit-history content scan could **not** be completed in this environment. Prior limited 186-member historical transport pattern checks remain separately scoped, not public repo-wide clearance.

## Journal preparation and release decision

Byline order author-confirmed: study lead; coauthor Dr Ahmed; three independent primary annotators; one senior adjudicator. Separate local title page and CRediT files prepared and visually rendered. In-kind KUber access to E1/E2 servers, no direct P2 financial grant, no competing interests, ethics exemption, rights, and not-concurrently-submitted were confirmed by the corresponding author. Exact current IP&M Guide for Authors page returned 403; double-anonymized handling is **conditional** under Elsevier general policy until the journal-specific route is verified.

**DO NOT create a FINAL/100% VERIFIED tag or DOI.** A named `review-candidate` branch may snapshot this scope, but final publishable release requires completeness checks and security tests stated above. Explicitly preserve the current-GOLD 35-case correction and the historical P2_45 distinct 36-case record.
