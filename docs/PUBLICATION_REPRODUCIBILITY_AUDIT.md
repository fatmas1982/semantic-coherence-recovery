# Publication Reproducibility Audit

This audit separates three levels that must not be conflated:

1. **Exact result reproduction** — recompute every reportable statistic from frozen case-level, workbook or OOF artifacts.
2. **Exact historical rerun** — rerun the original generation/training implementation bit-for-bit.
3. **Fresh reconstructed rerun** — rerun a documented reconstruction where the historical executable or every runtime detail was not retained.

## Final closure status

**RELEASE-CANDIDATE / PARTIAL INDEPENDENT VERIFICATION, not final submission PASS.** Prior archived metric-audit claims were documented, but the most recent manuscript/supplement versions still require version-linked table-by-table clean execution, coauthor approval and data-governance release checks. The previously successful GEE-only clean runner does not establish a full training/paper replay.

The current release now contains:

- the 120-prompt bank and 720-row prompt×model generation plan;
- all 720 authoritative retained generated outputs plus per-model raw output files;
- complete sheet-by-sheet CSV mirrors of the three recovered historical A1/A2/A3 workbooks;
- complete sheet-by-sheet CSV mirrors of the recovered round-1 senior adjudication workbook;
- the targeted second re-review workbook;
- FINAL GOLD v1.0 and the frozen CPU-baseline workbook;
- M0/M1/M2 archived OOF predictions and an explicitly reconstructed retraining script;
- M3 reportable A/B/C OOF, stability-seed OOF, LOTO case-level outputs, leakage/source/error analyses;
- M4 valid target-isolated forced-choice A/B/C OOF and summaries;
- legacy invalid free-generation M4 under an audit-only archive;
- follow-up source-utility and human-machine uncertainty outputs;
- a separately exposed post-hoc validity/sensitivity layer containing generator-signature and metadata-only diagnostics, strict M1/M3 dual blocking, source-bearing-only B→C restriction, ModernBERT token/truncation audit, manual high-similarity review, Qwen3-8B protocol perturbations, and exhaustive T4 answer-code permutations;
- reportable notebooks/scripts, paper/supplement Markdown mirrors, hashes and this experiment-to-artifact matrix.

## Exactness by stage

- **Human annotation:** the exact original A1/A2/A3 binaries were recovered and hash-verified; the public GitHub layer releases complete sheet-by-sheet CSV mirrors, so all analytic secondary-label, evidence-span/note, ambiguity, HREF and comment fields are public and diff-friendly. Published core IAA must still be computed from locked pre-resolution A1/A2/A3 decisions only, never adjudicated `Final_*` fields.
- **Senior resolution:** the exact 423-case round-1 senior adjudication binary was recovered and hash-verified; the public GitHub layer releases complete CSV mirrors of all four workbook sheets. The targeted second re-review and FINAL GOLD remain separate downstream provenance layers.
- **M0/M1/M2:** paper numbers are exactly reproducible from archived OOF predictions. The original historical training script was not retained; `code/baselines/07_retrain_cpu_baselines_reconstructed.py` is a documented reconstruction and must not be described as the original executable.
- **M3:** reportable OOF predictions, seed stability, LOTO, leakage audits, source analyses and diagnostic outputs are retained with the executable notebook.
- **M4:** only the target-isolated forced-choice run is reportable as the reference result. The later P1/P2 and answer-code perturbations are post-hoc protocol-sensitivity analyses; the P1/identity reference reproduces exactly before perturbations are interpreted. The earlier free-generation run remains under `archive/legacy_m4_invalid/` for audit only.
- **Post-hoc validity layer:** these files live under `code/validity/` and `results/validity/` outside the immutable 86-part transport bundle. They test threats to interpretation and do not replace the frozen reference analyses or constitute external validation.
- **Generation:** all 720 paper-used outputs are exact and authoritative. Fresh generation for five of the six checkpoints remains best-effort because exact immutable repository revisions and every model-specific chat-template/tokenization/stopping detail were not retained.

## Remaining non-closures

Two historical-execution claims remain intentionally unavailable and must not be made:

1. **Bit-for-bit regeneration of five original SLM generation checkpoints.**
2. **Bit-for-bit retraining of the historical M0/M1/M2 CPU implementations from the original lost training script.**

Neither limitation blocks exact reproduction of the numerical results reported in the paper, because the authoritative frozen generated outputs and OOF predictions are released.

See `EXPERIMENT_REPRODUCIBILITY_MATRIX.csv` for the experiment-by-experiment map.

## Post-hoc validity closure

The 2026-09 validity layer is now publicly browsable and includes case-level or OOF outputs wherever applicable. Key verified summaries are:

- anonymous generator recovery with character TF-IDF: macro-F1 0.536;
- M3 strict dual-blocked macro-F1: 0.591 / 0.671 / 0.682 / 0.573 for T1–T4;
- Condition-C token audit: median 122, p95 378, maximum 446, no case above 1024;
- exact M4 P1/identity reference reproduction before protocol perturbation;
- exhaustive T4 mapping sensitivity: 12 variants, macro-F1 range 0.206–0.413 and QWK range 0.006–0.401.

These results narrow interpretation to within-corpus recoverability under specified evidence, split, and evaluator protocols. The 2026-10-12 complete nested-GPU M3 audit supersedes the initial blocked summary; see `M3_DUAL_VERSION_RECONCILIATION_20261012.md` for both old/new numbers, case-level outputs, protocol, and SHA hashes. The corrected HJI 60-interval output is authoritative only from `data/validity_2026_10/HJI_60_CORRECTED_CI_SEED_20261010.csv`. Historical HJI CI endpoints remain superseded and cannot be substituted.


## Server-run archive: October 17, 2026 transport gate (branch only)

**Archive:** `results/server_runs/SERVER_RUN_20261007_A/` on `publication/server-run-20261007-a`. Initial uploaded archive commit: `d9f97ae`. This is a branch-level upload and **not a merge into `main`**, a change to the frozen study reference, or a final publication sign-off.

| Evidence layer | Observed/operator-reported result | Claim permitted |
| --- | --- | --- |
| Source-copy manifest | 4,578 entries; 0 missing; 0 SHA-256 mismatches | Local copy agrees with its generated manifest |
| Git index | 4,580 newly staged paths; 4,578 archive data files compared | Count reconciles with README and manifest |
| Raw Git objects | 4,578 raw blobs compared to manifest SHA-256; 0 mismatches | Byte-level fidelity for staged data at initial commit |
| ZIP read | 70 outer ZIPs and 68 nested ZIPs read; 0 read failures reported | Tested archive structures were readable |
| Limited secret screening | 4,509 direct text files, 2,766 outer-ZIP text entries, 2,756 nested-ZIP text entries; 0 pattern hits | No hits for tested patterns in scanned material; not a security clearance |
| Source code | `LOCAL_WORK` excluded | Original local work files not released in this branch archive |

The above results were supplied by the operator as PowerShell output, not independently rerun through this repository's CI. The staged-blob verification is strong transport evidence but does **not** validate M1–M4 scientific completeness, case-level experiment coverage, reproducibility of metrics, statistical assumptions, or lack of duplicate and superseded analyses. ZIP content screening used a small set of credential-token patterns; it is not equivalent to comprehensive PII, personal paths, embedded credentials, governance, or ethics review. A reported Mistral worker `ImportError` requires run-level disposition.

**Outstanding scientific closure actions:** produce a machine-readable archive inventory mapped to experiment IDs and executable source, classify every run completed/partial/failed, check missing expected target×condition×fold×seed combinations and prediction row counts, establish exact source and version precedence against the frozen references, rerun the corresponding table-level calculations independently, reconcile to the latest manuscript/supplement, and obtain relevant coauthor/data-governance approvals. Do not promote this transport PASS to publication-level PASS.
