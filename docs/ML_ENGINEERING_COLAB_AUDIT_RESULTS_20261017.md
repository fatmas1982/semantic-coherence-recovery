# Colab machine-learning engineering audit — 2026-10-17

Input: user-supplied `P2_ML_ENGINEERING_AUDIT_ee0a76f660.zip`; run at commit `ee0a76f66019205ae71458416878bccb108b245e` (reported in bundle). This document records the **reported run evidence inspected from the ZIP**, not a fresh independent model training run.

| Gate | Results |
|---|---|
| 25 tests | 17 PASS, 1 BLOCKED, 7 NOT_TESTED, 0 FAIL |
| Original `results.rar` | SHA-256 PASS `58493dc555ef95be1876416731723d71bb9c40ead2585e1b3bbafaad6ef7815d`; size 13,195,705 bytes |
| Historical transport and case linkage | PASS (return code 0 for existing scripts) |
| M3 dual OOF | No duplicate Case_ID and no cross-fold Prompt_ID overlap in each T1–T4 target; **does not prove nested training leakage-free** |
| Recomputed M3 dual macro-F1 | T1 0.5913225257153932 (n=720), T2 0.671147712324077 (n=474), T3 0.68183570135006 (n=460), T4 0.5732726099821898 (n=474) |
| E1/E2 | Existing summary-algebra checker PASS; NOT a case-level permutation replay |
| RAR extraction | BLOCKED: 7-Zip 23.01 reports Unsupported Method, 4461 sub-item errors. Archive SHA passes, so the log alone does not establish corruption. |

**Seven NOT_TESTED gates:** static leakage review (only heuristic flags), dynamic nested train/dev/test trace, complete 24-archive nested metric recomputation, fresh training reproduction, E1/E2 case-level prompt bijection, clustered-bootstrap CI independent refit, and original GPU runtime replay.

**Governance:** No private annotation text was uploaded here. Local absolute Drive paths present in the user's private ZIP are intentionally omitted. No external human validation is claimed. This run does not justify a journal-ready or fully-reproducible certification. Resolve RAR5 extractor compatibility and rerun case-level gates. Raw model inferences and M3 retraining were not executed.
