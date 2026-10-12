# October 12, 2026 supplied candidate artifacts — exact source inventory

This file records the exact supplied candidate bytes and **does not claim** that the corresponding binary archives or DOCX files have been uploaded to this GitHub repository.

The user has explicitly authorized public release of their supplied candidate, but numerical/technical verification remains a separate acceptance gate.

## Source artifacts

- Candidate ZIP: `IPM_REPRODUCIBILITY_GOVERNANCE_RELEASE_CANDIDATE_20261012(1).zip` (local supplied; 16 files)
- Manuscript: `IPM_MAIN_GOVERNANCE_RECONCILED.docx`, SHA-256 `c921de31a3dc56d946f137b795d4ecee04ad7977f3cb711cf1725fbdfe1802ce`
- Supplement: `IPM_SUPPLEMENT_GOVERNANCE_RECONCILED.docx`, SHA-256 `a0fedb866af27c7edce78fe9cb1f4f1ddca4cf99f18317a233b663d5139cb4c2`
- October GPU source: `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(2).zip`, SHA-256 `55b879ce51470d6c79933f3f32cc46e1bb4e28bc69693ea8b43ed9514adb2e96`.
- M3 24-row report and case-level predictions included in local candidate package.

## Verification actually performed

October GPU bundle 32 experiment ZIPs: case counts T1=720, T2=474, T3=460, T4=474; nonduplicated Case_ID in all experiment reports; required MANIFEST, PREDICTIONS, METRICS_AND_CLUSTER_CI, CONFUSION_MATRIX and PER_CLASS present; Macro-F1 computed from archived y_true/pred equals the stored metric within 1e-9. All 32 passed this archived-output-only check.

### Not established

- Source GPU binary presence on main or automated GPU rerun using clone alone
- All CPU experiment artifacts, source-trainer reconstruction and exact GPU retraining
- Numerical reproduction of every main/supplement table (100 table inventory is structural only)
- Complete independent evaluation of bootstrap confidence intervals and every new statistical test
- Full agreement of reportable results with each document's figures and interpretations

A rigorous reviewer must not interpret this status as end-to-end publication reproducibility. This is an evidence-index file and not a final-release certification.
