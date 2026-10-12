# Release audit status — 2026-10-12

**IMPORTANT: main is not certified as a complete up-to-date publication release.** The public base archive passed clean-room verification. The safe unpack fix and non-overwrite regression test were added to main; the corresponding main branch GitHub Actions run passed.

## Independent local inspection of the private candidate GPU bundle

Source: privately supplied `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(2).zip` (not copied to the public repository).
- 32 nested experiment archives: 24 M3 dual/size-matched and 8 M4 Qwen/Mistral FP16 condition-C.
- All 32 contain `reports/MANIFEST.json`, `reports/PREDICTIONS.csv`, `reports/METRICS_AND_CLUSTER_CI.csv`, `reports/CONFUSION_MATRIX.csv`, and `reports/PER_CLASS.csv`.
- All 32 have complete unique Case_ID coverage: T1 720, T2 474, T3 460, T4 474.
- Macro-F1 was recomputed directly from retained `y_true` and model prediction columns in all 32 nested reports.
- Corrected M3 strict dual-block Macro-F1: T1 0.591323, T2 0.671148, T3 0.681836, T4 0.573273. Earlier ~0.553/0.675/0.701/0.601 values in historical documentation must not be silently presented as the same execution.
- This confirms retained result integrity and coverage; it does **not** independently re-execute model training, validate every training input hash, or validate every statistical CI.

## Outstanding gates

1. Integrate approved non-identifying October CPU and GPU artifacts under versioned paths with code/input/output contract manifests; do not expose the private source archive until attribution, coauthor rights, and human free-text privacy are cleared.
2. Audit every manuscript and supplement table, statistical claim, confidence interval and test against their frozen case-level source and executable producer; track old and corrected versions.
3. Resolve the documented FP16 T1 reference discrepancy before promoting numerical claims.
4. Check code executability and full experimental reproduction, not just manifest presence and cached metrics.
5. Complete coauthor, data privacy, source rights and research-governance publication clearance.

**Do not label this commit or branch as a final, independently certified complete research release.**
