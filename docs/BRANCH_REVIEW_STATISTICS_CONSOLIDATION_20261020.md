# Historical reviewer evidence consolidation — 20 October 2026

**Release status: DRAFT / PARTIALLY VERIFIED.** This document is a controlled evidence inventory and author-copy reconciliation. Its PASS labels apply only to exactly named computational checks; they do not make the research universally reviewer-certified or publication-ready.

## Migration performed, preserving original bytes

51 **unique** source-branch files were added atomically to `main` with unchanged source Git blob SHAs in commit `5f9543ea65806919fe0839bc347dcc980b0961bb`. There were **13 code files, 13 result files, 23 documentation/registry files, and two historical requirements files**. These originated in:
- `reviewer-code-only-2026-09-28` (46 files, of which 43 were also present in `ipm-submission-prep-2026-09-18`);
- `audit/consolidated-review-evidence-20261019` (five audit tables/notes).
- The `ipm-2026-e1e2-hji-review-fixes` branch had **no missing file paths** relative to `main` at migration time; its scoped CI runs had already created reproducible evidence.

**Verification**: each of the 51 paths was checked in the new `main` tree against the identical Git blob SHA in its source branch (51/51). See [byte-level migration manifest](BRANCH_ARTIFACT_BLOB_MANIFEST_20261020.csv). This validates copy identity, **not** scientific correctness of historical outputs. The migration did **not** overwrite frozen GOLD, model predictions, `README.md`, pre-existing CIs, or any existing `main` source file.

Older `R8`/`R14` files are frozen historical snapshots, not current release-authoritative instructions. In particular the R14 September 20 status `PASS_R14_FINAL_SUBMISSION_SYNC` concerned a **16-main-table manuscript**, whereas the October manuscript has **20 main and 80 supplement tables**. This old PASS must never be described as certification of the October manuscript. Likewise, old October 19 documents that called T1 serialization unresolved predate the 15 October historical reconstruction discovery and 20 October decision-algebra CI confirmation in [the current status](T1_MAINLINE_PROTOCOL_RECONCILIATION_20261020.md).

## Executed or inspected verification — distinct scopes

| Scope | Evidence | Supported statement | Not supported |
|---|---|---|---|
| Historical branch copy | `docs/BRANCH_ARTIFACT_BLOB_MANIFEST_20261020.csv` | 51/51 unchanged Git blob identities | Re-running all scripts |
| New imported-output clean-room gate | [GitHub Actions 39455660759](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39455660759), `code/analysis/check_imported_september_20261020.py` | **PASS_IMPORTED_ARCHIVE_CONTRACTS_ONLY** for archived CSV counts/arithmetic | Full bootstrap redraw, model training, human annotation redo |
| Task-stratified computational-bootstrap *archived output* | `results/followup/P2_IPM_TASK_STRATIFIED_COMPUTATIONAL_BOOTSTRAP_SENSITIVITY.csv` | 49 rows; max absolute endpoint shift **0.013079380282429554**; zero changed interval zero-inclusion statuses | Current October journal table numerical audit |
| Outer fold-by-class *archived output* | `results/followup/P2_IPM_FOLD_BY_CLASS_AUDIT.csv` | 20 target-by-fold rows; T1/2/3/4 case sums **720/474/460/474**; 24 prompts per outer fold; min nonempty class cell **11** | Absence of M3 inner-selection leakage |
| Human pair reliability & ambiguity summaries | `results/followup/P2_IPM_PAIR_SPECIFIC_HUMAN_RELIABILITY.csv`, `P2_IPM_AMBIGUITY_EXCLUSION_SENSITIVITY.csv` | 12 pair-specific dimensions, 11 ambiguity summary rows, archived reproducible code | Independent outside reference validity |
| Adjudication instabilities and provenance | `results/followup/P2_IPM_ADJUDICATION_INSTABILITY_EXCLUSION_SENSITIVITY.csv`, `P2_IPM_ADJUDICATION_QUEUE_RULE_AUDIT.csv` | Eight model/target exclusion summaries; archived 423/297 queue rule | Full adjudicator process reconstruction |
| GEE stability clean-room refits | [GitHub Actions 38293550933](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38293550933) | **60/60** fitted GEE rows within tolerance for coefficients/SE/Wald CI; 3 rare-event flags associated with a single Qwen contrast | Rare-event bias correction or causal effects |
| Corrected HJI bootstrap | [GitHub Actions 38293551006](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38293551006) | **60/60** archived corrected CI verification records | All historical human intervals identical across old sampling schemes |
| E1/E2 paired and GEE run | [GitHub Actions 38612837716](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38612837716) | **20** E1/E2 paired summaries and refreshed associated statistics; **3,000** Prompt_ID-cluster bootstrap draws in this executable | Automatic proof of historical **250-draw** Supplement Table S-E1E2 percentiles |
| M3 dual frozen OOF | [GitHub Actions 38293551006](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/38293551006), later [target-specific independent report](M3_DUAL_OOF_DIRECT_RECALC_20261020.md) | Four macro-F1 values exactly recover from **2,128** archived OOF case predictions | Independent replay of inner CV training |
| Main manuscript targeted summaries | [Tables 10/14/17](TARGETED_MAIN_TABLES_10_14_17_AUDIT_20261020.md), [CI](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39430171858) | 60/60 displayed values match selected source summaries at three decimals | Entire 100-table value and raw-data reconciliation |

### Critical disclosure: two E1/E2 interval lineages

The October **Supplement Table S-E1E2** describes 250 historical Prompt_ID-cluster draws with seed 20261009. The later successful GitHub Actions reanalysis ran 3,000 draws with the same recorded seed. Seed equality does **not** imply identical percentile endpoints across different replicate counts. This is a **version/protocol-boundary discrepancy**, not evidence of a model failure, and must remain visible until individual table endpoints are compared to their exact original 250-draw source. Do not overwrite the historical table with 3,000-draw results without an explicit manuscript revision and source proof.

### Additional interpretive cautions

The three sparse GEE rows each draw from the *same* Qwen T1 E2 contrast with 15 changed decisions; they are **not** three independent batches of rare events. The majority-failure subset of human ordinal severity has a lower α than the full sample. Task-stratified bootstrap is conditional on frozen OOF and grouped prompt sampling; it does not integrate uncertainty from retraining or alternate outer folds. M1/M3 size-matched studies and generator-stratum probes are post-hoc within the observed corpus. Avoid causal source, tokenizer, model architecture or generator self-preference claims.

## Author-facing manuscript reconciliation

The final local author copies were derived from the 20 October T1-integrated Word documents. Retrospective scoped annotations were inserted into the main human-reference/methodology/E1-E2/statistics discussion, and into supplementary human, task-stratified, E1-E2 and reviewer-gate text. **No original scientific table cell text changed:** 20/20 main tables and 80/80 supplement tables were compared in full.

| Artifact | Before SHA-256 | Revised SHA-256 | Rendered pages |
|---|---|---|---:|
| Main paper | `96fa7a3272abdeb13573f013fc071e616c8b4543bffda81bbf146ed416f11ee2` | `eaa9dcca8d7063a3e5de12b4c538925f0c98c58234d5057a29a46ca6b91ad4b2` | 37 |
| Supplement | `8c2fe5d55b2d720853009140efa2843c7ede414fbb399e73c6e96b203c129dd5` | `9d7751c63702714f5214a671fb56480b8c4fd9d85443920780cec75ba23cdc57` | 52 |

The new Word binaries **remain author-facing local deliverables** and have not been silently deposited in the public GitHub repository. The archival outputs and old R14 paperwork are not relabeled as a verified current manuscript release.

## Reviewer assessment

[Up-to-date 23-family matrix](REVIEWER_FAMILY_STATUS_20261020.csv). Source historical matrix `REVIEWER_FAMILY_STATUS_20261019.csv` is preserved unchanged for reproducibility. It is important not to downgrade already reproduced GEE/HJI/M3/E1-E2 tests to “not executed,” or upgrade all other tests to “PASS” without evidence.

**Remaining requirements for submission freeze:** exact linkage of all reportable numbers to correctly versioned source predictions; any unsettled Table S-E1E2 250/3,000 CI endpoint alignment; dynamic verification of M3 nested model selection and leakage where historically executable; full failed-run-to-success provenance or appropriate residual disclosure; and human coauthor/ethics/public-data clearance. Independent external human validation remains deferred future work.

**Current decision: MAJOR REVISION / IMPROVED EVIDENCE INVENTORY AND SCOPED CI PASS; NOT 100% COMPLETE.**
