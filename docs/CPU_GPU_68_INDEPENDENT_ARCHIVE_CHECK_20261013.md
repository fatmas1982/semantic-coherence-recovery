# Verified October 2026 CPU/GPU source archive inventory

Source: the user's actual attached source ZIP files. **Integrity checking does not demonstrate retraining or exact CI/table reproducibility.**

| Source archive | Bytes | SHA-256 | Experiments | Prediction coverage and overall Macro-F1 |
|---|---:|---|---:|---|
| P2_CPU_RESULTS_BUNDLE(5).zip | 877283 | fb97527da35b89291d3acd19f633677737437c8000cd2f42c0e4aad138b539fc | 36 | PASS 36/36 |
| P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(3).zip | 2500810 | 55b879ce51470d6c79933f3f32cc46e1bb4e28bc69693ea8b43ed9514adb2e96 | 32 | PASS 32/32 |
| IPM_REPRODUCIBILITY_GOVERNANCE_RELEASE_CANDIDATE_20261012(1).zip | 4158227 | ed97910c8e3627ddb95d41d3bc635ab2be90e9e6ae1bf4068662ebc46687f5a1 | Manuscript/supplement/governance candidate | File SHA verified |

## Independent archived-output check performed 2026-10-13

- Exactly 36 CPU plus 32 GPU nested experiment ZIPs.
- Each contains `reports/MANIFEST.json`, `reports/PREDICTIONS.csv`, `reports/METRICS_AND_CLUSTER_CI.csv`, `reports/CONFUSION_MATRIX.csv`, and `reports/PER_CLASS.csv`.
- Unique Case_ID count equals expected task population in every individual experiment: T1 720, T2 474, T3 460, T4 474.
- Overall macro-F1 recalculated using scikit-learn on `y_true` and the experiment's unique prediction column equals archived `group=all` value to absolute tolerance 1e-9 in **68/68** experiments.
- Reproduction of bootstrap CI endpoints and actual GPU training, availability of trainer dependencies and source checkpoint revisions, and full manuscript/supplement table comparisons were **not** performed by that test.

## Actual binary deposition check

This repository record is **not** the binary upload. The three ZIP archives must exist at:

`release/2026-10/source_archives/`

with the exact sizes and SHA-256 above to qualify as deposited. The user-facing handoff contains the original bytes plus a fail-closed Git publisher, `PUBLISH_VERIFIED_ARCHIVES.py`. Do not declare clone-only comprehensive reproducibility until the files are present and GitHub's fresh-clone CI passes end-to-end.

The original Colab Local Runtime/SSH notebook is already in `code/validity/P2_COLAB_LOCAL_SSH_JUDGE_SENSITIVITY_20261009.ipynb`.
