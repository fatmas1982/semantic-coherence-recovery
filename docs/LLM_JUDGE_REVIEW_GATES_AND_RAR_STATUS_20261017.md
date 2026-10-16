# LLM-as-a-Judge / Evaluation-Protocol Audit — 17 October 2026

## Scope and release statement
The 14-issue independent-*style* desk review identified **3 critical, 9 major, and 2 moderate** protocol/evidence gates. This follow-up is a documentary and executable **partial remediation**, not new inference and not a certified re-analysis. The frozen reference, historical tables, and GOLD were not altered. **External independent human validation remains deferred**.

## RAR correction
At inspection, `main/results.rar` **exists** in the GitHub tree and has reported size **13,195,705 bytes**. Consequently the historical `docs/RESULTS_RAR_SHA256_AND_DEPOSITION_20261014.md` statement “NOT DEPOSITED” is **outdated** with respect to *presence on GitHub*. Its reported SHA-256 is `58493dc555ef95be1876416731723d71bb9c40ead2585e1b3bbafaad6ef7815d`, but a fresh independent download/hash check was **not possible** here; presence and bytewise integrity are different assertions. Run `sha256sum results.rar` after a clean authenticated checkout and compare. It is author-designated authoritative only for matching experiment identities. Its contents have **not** been freshly extracted or analyzed during this update, so no new statistics are claimed.

## Reproducibility tool added
`code/validity/verify_e1e2_judge_summary_20261017.py` uses standard-library CSV processing on two **already deposited summary input files**:
- `data/validity_2026_10/E1E2_DECISION_AND_MARGIN_DIAGNOSTICS.csv`
- `data/validity_2026_10/E1E2_DELTA_MACROF1_BOOTSTRAP_3000.csv`

It asserts **20** matching judge–target–experiment–variant keys; prescribed target denominators T1=720, T2=474, T3=460, T4=474; exact transition-count identities; rate arithmetic; delta-macroF1 algebra; and archived bootstrap metadata 3,000 resamples, seed 20261009. It prints a machine-readable JSON summary and exits nonzero on contradictions. It **does not** recompute bootstrap intervals, 60 GEE fits, E1/E2 prompt invariance, or parse the RAR. The test has been committed but was **not executed on GitHub Actions in this turn**. It should not be reported as a PASS until actually run.

## Reviewer gates (J1–J14)
| Issue | Required evidence / operation | Status |
|---|---|---|
| J1 | Exact target eligibility and conditional estimands | Manuscript clarification only |
| J2 | Byte-exact prompt serializer, tokenizer and code parsing | OPEN |
| J3 | Case-level E1/E2 bijection and input invariance | OPEN; summary audit added |
| J4 | No causal cross-profile architectural/precision claims | Wording update prepared |
| J5 | Generator-lineage exclusion compositional audit | OPEN |
| J6 | 60-test family and small-event GEE robustness | OPEN |
| J7 | Distinguish observed prediction switches from hypotheses | Wording update prepared |
| J8 | Source manifest and experiment precedence | RAR presence established; hash replay OPEN |
| J9 | Attempt/success/invalid counts and missingness | OPEN |
| J10 | T4 confusion, QWK, MAE and per-class tables | OPEN |
| J11 | Historical vs post-hoc labeling | Wording update prepared |
| J12 | CI seed/population/cluster replication ledger | OPEN; 3000/20261009 summary metadata observed |
| J13 | Internal-only generalization scope | Wording update prepared |
| J14 | Task-coupled source availability | Wording update prepared |

## Mandatory next steps before calling this closed
1. In a fresh checkout, run `sha256sum results.rar`; extract with a compatible RAR reader; store content inventory and SHA manifest.
2. Build deterministic case-level paired tables for each E1/E2 profile using the RAR, including status != ok; compare all 20 reported aggregate contrasts and 60 statistical comparisons.
3. Assert the mapping bijection and inversion for every row and prompt identity; publish executable tests rather than assertions in prose.
4. Recalculate uncertainty at Prompt_ID cluster level from raw paired cases and independently refit statistical models. Never overwrite the reference numerics silently.
5. Release a validated exactness matrix and privacy/rights review, and reconcile the latest DOCX versions before a final journal release.

This is an **intermediate, openly qualified repository update**. No final end-to-end reproducibility certification is asserted.
