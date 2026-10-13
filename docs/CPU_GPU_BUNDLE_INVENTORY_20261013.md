# User-provided October CPU/GPU bundles — 2026-10-13 inspection

Source: uploaded ZIP archives in the research conversation, **not** yet deposited as binary files in this public GitHub checkout.

| Phase | Archive | SHA-256 | Experiment archives | Predictions CSV present | Distinct Case_ID per experiment | Metrics and CI CSV present | Confusion and per-class CSV present |
|---|---|---|---:|---:|---|---:|---:|
| CPU | P2_CPU_RESULTS_BUNDLE(5).zip | fb97527da35b89291d3acd19f633677737437c8000cd2f42c0e4aad138b539fc | 36 | 36 | PASS | 36 | 36 |
| GPU | P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(3).zip | 55b879ce51470d6c79933f3f32cc46e1bb4e28bc69693ea8b43ed9514adb2e96 | 32 | 32 | PASS | 32 | 32 |

CPU case counts per experiment: 9 × 720, 18 × 474, 9 × 460.
GPU case counts per experiment: 8 × 720, 16 × 474, 8 × 460.

The original Colab Local Runtime / SSH judge sensitivity notebook was retrieved from the user's Drive ID `1nUvohS7C46Z8tsqTlNLhzjHmtFPEyeKm` and deposited at `code/validity/P2_COLAB_LOCAL_SSH_JUDGE_SENSITIVITY_20261009.ipynb`.

## Release boundary

The uploaded ZIP archives are locally inspectable but are not yet deposited in the repository. The presence of this inventory must not be treated as archival deposition or a claim that a fresh clone can regenerate the 68 reported runs. Metrics schema and paper/supplement table reconciliation still require a separate full independent audit. Preserve model revisions, Prompt_ID grouping, conditions and experiment identifiers when conducting it.
