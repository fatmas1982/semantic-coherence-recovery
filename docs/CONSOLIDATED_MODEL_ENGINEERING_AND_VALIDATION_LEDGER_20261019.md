# Consolidated validation and model-engineering review evidence ledger (2026-10-19)

> **Status: DRAFT AUDIT INVENTORY — NOT A FINAL PUBLICATION CERTIFICATION.**
>
> This ledger consolidates previously dispersed experiment families and post-review validation checks. It distinguishes **available archival evidence** from **directly reproduced analyses**, **operator-reported checks**, **candidate manuscript claims**, and **unresolved verification**. It is not a newly executed end-to-end rerun or a replacement for frozen reference results.

## Authoritative manuscript snapshot being reconciled

Locally supplied author files (2026-10-17):
- `P2_MAIN_LLM_JUDGE_PROTOCOL_REVISED_20261017(1).docx`
- `P2_SUPPLEMENT_LLM_JUDGE_PROTOCOL_REVISED_20261017(1).docx`

These binaries were **reviewed as attachments**, but are **not deposited by this ledger**. Their numerical tables require exhaustive value-by-value reconciliation against final source artifacts before edits or publication claims.

## Source-precedence policy

1. Treat `docs/FINAL_RESULT_SCOPE_POLICY_20261014.md` as the scope rule: a newer result supersedes an older one **only when the exact experiment identity matches** (model/checkpoint, precision, target, input condition, seed/repeat, split/blocking and scoring protocol).
2. Frozen historical M0–M4 OOF results remain the reference for matching reference experiments; dual/size-matched M1/M3 results are **post-hoc sensitivity**, not replacements for ordinary Prompt_ID-folded M1/M3 estimates.
3. Distinguish the archived Qwen3-8B target-isolated forced-choice M4 from the later Qwen and Mistral FP16-offload Condition-C runs. The latter are NOT the same as E1/E2 answer-code/option-order experiments. Avoid architecture/model-family ranking claims.
4. `P1/identity` and `E1/rot0` are separate labels and are not assumed to share byte-identical inputs; a previously documented FP16 T1 reference/prompt-serialization discrepancy remains open.
5. All validity extensions that followed initial frozen analysis must be labeled **post-hoc / exploratory**, never preregistered or confirmatory by retrospective wording.

## Coverage ledger — experiment family, artifact/protocol and status

| Family or audit | Evidence locator | What can be claimed now | What must NOT be claimed without further proof |
|---|---|---|---|
| Corpus/generation and 120 prompt clusters × 6 outputs | `data/publication/` (extracted public bundle), `docs/REPRODUCIBILITY.md` | Frozen 720-case layer and generation-provenance records | Bit-identical re-generation of five historical checkpoints |
| A1/A2/A3 locked pre-resolution agreement | `data/annotation/historical_full_csv/`, `code/annotation/` | Archived 2,160 pre-resolution ratings; separately documented IAA analyses | Independent external human-reference validity or fresh blind rereview |
| Senior 423-case resolution, targeted 29-case rereview, deterministic consistency pass | `docs/PUBLICATION_REPRODUCIBILITY_AUDIT.md`, recovered GOLD provenance | Separate resolution layers; controlled post-resolution reference | Treating adjudicated labels as pre-resolution inter-rater agreement |
| GOLD T1–T4 reconstruction | Canonical 720-case CSV in immutable extracted bundle; frozen baseline OOF | Operator-reported case/label reconciliation; T3 Core_SCF normalization corrected in Colab (460 cases) | New psychometric validation; exact rerun proof unless code and output added and independently executed in CI |
| M0–M2 baseline reference | `data/frozen/baseline_csv_mirror/`, `code/baselines/` | Numerical archived OOF checks; reconstructed trainer separately labeled | Historical bit-identical M0–M2 retraining |
| M3 reference A/B/C OOF, stability seeds and within-corpus task LOTO | `data/computational/m3/`, `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` | Frozen OOF primary reference; identified robustness families | Replacing reference A/B/C with October dual-block results |
| M4 archived Qwen3-8B forced-choice A/B/C | `data/computational/m4/`, `code/m4/` | Valid target-isolated reference protocol | Treating superseded free-generation archive as valid comparison |
| Source utility and human easy/hard / entropy | `code/followup/`, `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` | Within-corpus exploratory analyses | Causal source effect or calibrated predictive confidence |
| Lexical/semantic cross-fold leakage and manual top-pair review | `results/validity/cpu/`, `docs/VALIDITY_EXPERIMENTS_2026-09.md` | Scope-specific duplicate/near-duplicate concerns evaluated | Proof of no semantic leakage of any kind |
| Anonymous-generator identity signature probe | `results/validity/cpu/P2_81_GENERATOR_IDENTITY_PROBE_OOF.csv` | Potential generator-associated shortcut audit | Population transfer to unseen generators |
| Metadata-only target diagnostic | `results/validity/cpu/P2_81_METADATA_ONLY_TARGET_OOF.csv` | Corpus-structure and non-text shortcut sensitivity | Text evaluator efficacy |
| M1 strict prompt+generator dual blocking, size matching | `results/server_runs/SERVER_RUN_20261007_A/CPU/M1_COMPLETE/` | 24 OOF CSVs present; audit indicated case-ID/label coverage; archived transport byte verified | Every original trainer/input/run-log end-to-end replay |
| M3 strict dual-blocking and five size-matched repeats | `results/server_runs/SERVER_RUN_20261007_A/GPU/M3_COMPLETE/`, `docs/M3_DUAL_VERSION_RECONCILIATION_20261012.md` | 24 archived OOF files and post-hoc robustness with explicit revision lineage; reference dual macro-F1 approximately 0.591/0.671/0.682/0.573 | Equating initial superseded blocked scores to this exact protocol; external validation; no training-set-size effect |
| ModernBERT token/truncation | `results/validity/cpu/P2_81_M3_TOKEN_AUDIT_*.csv` | Reconstructed-input token-length diagnostic | Exact historical encoding for every checkpoint |
| Source-bearing-only B/C | `results/validity/cpu/P2_81_SOURCE_BEARING_BC_REANALYSIS.csv` | Restricted-case sensitivity | Causal inference from separately trained M3 B/C |
| M4 P1/P2 rubric, answer-code mapping, all T4 mappings | `results/validity/m4_protocol/`, `results/validity/m4_t4_complete/` | Frozen reference plus deliberately varied evaluation contract; exhaustive 12 T4 variants within fixed 2×6 design | Selecting best mapping post hoc as benchmark reference |
| October FP16 offload — Qwen and Mistral | `results/server_runs/SERVER_RUN_20261007_A/GPU/M4_NEW/` | Eight Condition-C OOF files present; per-target results can be recomputed | Assuming these are E1/E2 rot0 controls; cross-family causal/architecture superiority |
| E1 answer-code / E2 option-order perturbations | `docs/GEE_STABILITY_POSTHOC_AUDIT_2026_10_12.md`, `data/validity_2026_10/` | Post-hoc paired perturbation comparisons with 10,408 overlapping comparison rows | Independent 10,408 cases, token-prior causality, or a fifth confirmatory RQ |
| Human-judge change contrasts, 60 GEE models and corrected HJI CI | `results/validity_2026_10/HJI_GEE_STABILITY_60.csv`, corrected 60-row HJI file and corresponding code | Scoped 60-fit precision audit and corrected confidence-interval lineage; 15 changed outcomes for sparse Qwen T1 E2 case (not 45 independent changes) | Bias-corrected rare-events inference, multiplicity-adjusted CIs, or independent observations |
| Model-engineering / ML-review follow-up: code/input/output contracts, missingness, CV leakage, duplicate/near duplicate, reproducibility, hashes | `docs/RELEASE_CANDIDATE_EVIDENCE_AND_GAPS_20261012.md`; separate reviewer audit bundles were supplied in earlier sessions | Issues and scope represented in this registry as mandatory gates | Marking every reviewer-requested correction as complete without reviewing exact package outputs and commit |
| Post-archive integrity audits | `results/server_runs/SERVER_RUN_20261007_A/SHA256_MANIFEST.csv` and run README | Operator reported 4,578 raw Git blob/manifest byte matches; archive publicly stored | Security clearance, rerun correctness, end-to-end completeness |
| Six-phase and later Colab validation outputs | Previously exchanged ZIPs: first through sixth pass, targeted GOLD reconstruction and run-provenance manuscript reconciliation | User-operated consistency/integrity reports (56 OOF validated, T1–T4 reconciled according to supplied run outputs) | Calling Colab runs an external independent blind review or verified complete run-level recovery |
| Log error/retry recovery | `results/server_runs/SERVER_RUN_20261007_A/GPU/` logs and per-job JSON | Presence of 7 error-containing log files and surviving OOF data has been reported | That failed processes themselves subsequently succeeded, without exact linked run identifiers and terminal success markers |
| Manuscript/supplement table-to-artifact review | `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` plus 2026-10-17 author DOCX snapshot | Table/claim inventory available, reference metrics partially recomputed | Claiming every table/CI/p-value in latest DOCX was numerically audited |

## Model-engineering review checklist — required closure evidence

For each reviewer-raised issue create a row that captures **review finding → fix/experiment protocol → immutable code revision → exact input manifest → execution/output path → expected units/coverage → recomputed statistic → manuscript/supplement location → result state → reviewer limitation**.

Mandatory topics: target/label provenance; task- and prompt-cluster-grouped folds; generator-stratum shortcut/dual block; sample-size-matched repeated controls; train/test overlap and near duplicates; versioned tokenizer/input serialization and missingness; seed and stochastic stability; model-engineering exceptions/OOM retry recovery; confidence interval / multiplicity / sparse GEE diagnostics; FP16 judge reference-vs-perturbation protocol separation; output-contract compliance; original-vs-reconstructed execution; 2026-10 paper/source precedence and potential reviewer-facing leakage of sensitive notes.

**No retrospective claim that the review led to new preregistered hypotheses, external construct validity, architectural ranking, or fully independent validation.**

## Publication-gate states (as of this registry)

- **TRANSPORT/INDEX:** PASS with operator-reported command-output scope.
- **OOF CASE COVERAGE:** previous Colab reports indicate PASS for the audited 56 OOF files, but versioned executables/results are not yet deposited in a unified reproducible GitHub audit.
- **GOLD T1–T4:** user confirmed T3 reference normalization PASS (460/460); provenance is not yet CI-pinned in this consolidated ledger.
- **RUN FAILURE → SUCCESS PROVENANCE:** UNVERIFIED. OOF existence alone does not close failed run history.
- **MANUSCRIPT + SUPPLEMENT NUMERIC CLAIMS:** NOT FULLY AUDITED against author 2026-10-17 Word snapshots.
- **PUBLICATION CLEARANCE/COAUTHOR RIGHTS/ETHICS:** require explicit authorized human determination.

## Immediate next work

1. Recover the exact **Machine-Learning / Model-Engineering Reviewer** audit package, the corrected code and its result manifests. Compare each promised fix with released runnable evidence; avoid relying on older assistant narrative.
2. Capture the user's six-phase Colab ZIPs and subsequent target reconstruction and run-provenance ZIPs as immutable, SHA256-listed, privacy-screened **new** artifacts (without editing historical raw files). Assign a stable run identifier, Python/library versions and source commit to each.
3. Produce a final table-by-table numeric reconciliation for the 2026-10-17 main and supplement DOCX, preserving distinction between reference results and post-hoc sensitivity. Recompute each metric/CI/test from exact case-level source when available.
4. Resolve the documented FP16 T1 serialization discrepancy and run-error chain if resolvable; otherwise keep the limitation visible.
5. Request approval for journal-oriented archival release only after coauthor and data-governance signoff. Do not mark as `FINAL PASS` in the interim.

## Existing key documentation

- `docs/PUBLICATION_REPRODUCIBILITY_AUDIT.md`
- `docs/RELEASE_CANDIDATE_EVIDENCE_AND_GAPS_20261012.md`
- `docs/RELEASE_AUDIT_STATUS_20261012.md`
- `docs/FINAL_RESULT_SCOPE_POLICY_20261014.md`
- `docs/GEE_STABILITY_POSTHOC_AUDIT_2026_10_12.md`
- `docs/EXPERIMENT_REPRODUCIBILITY_MATRIX.csv`
- `docs/M3_DUAL_VERSION_RECONCILIATION_20261012.md`

**Methodological distinction:** a file-existence check, a manifest checksum, a frozen-OOF recomputation, a separate new experimental rerun and a complete paper claim audit establish different types of evidence and must not be conflated.
