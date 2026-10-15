# Historical M0–M4 case-level audit — 2026-10-15

## Verified checks

- Archived CPU bundle: 360/360 metric rows reproduced directly from `reports/PREDICTIONS.csv` across 36 experiments. Includes reconstructed M1 and archived M4 A/B/C outputs; this is **not a fresh rerun of training or inference**.
- Archived GPU FP16/offload bundle: 320/320 metric rows reproduced from `reports/PREDICTIONS.csv` across 32 experiments (M3 and M4 Qwen/Mistral).
- Grand total: **680/680** case-level macro-F1 and accuracy calculations numerically identical to the respective `reports/METRICS_AND_CLUSTER_CI.csv` and bundle `summary/ALL_METRICS.csv` values. Maximum observed absolute difference in macro-F1: 8.33e-17; in accuracy: 1.11e-16.
- Unique Case_ID and 120 unique Prompt_ID per experiment. The expected N in each subgroup agrees with report and summary.
- Bootstrap CI endpoints are well ordered and consistent **between the archived report and summary**. These checks do not independently regenerate the archived bootstrap samples.
- Main manuscript Table 18: 8/8 historical FP16 macro-F1 and endpoint triplets agree with archived raw-run source to **three-decimal presentation precision**.

## Critical scope limitations

1. This is an independent recalculation of scores from **saved predictions**; it is not a rebuild of M0/M2 models, re-training M1/M3, nor generation with M4.
2. The archived `results.rar` is authoritative **only for matching historical runs**. This audit drew directly from separately named CPU and GPU ZIP bundles, not an independent parse of every object in `results.rar` (its RAR decompressor is unavailable in the current container). Source precedence remains conditional on exact identity and protocol.
3. No manuscript-wide certification across 18 main and 84 supplementary tables is implied. The historical row audit concerns 680 saved metric rows plus 8 main-Table-18 summaries.
4. Recalculated macro-F1 for three-class T4 subgroups must include the **full original label set** (1,2,3), even when a small subset omits a class; otherwise sklearn defaults to fewer classes and produces spurious discrepancies. The audit explicitly fixes class labels.
5. Historical T1 serialized-input disagreement (FP16 reference vs E1/rot0) remains unresolved. Standardized T1 post-hoc GPU scores are separate experiments.
6. Point-estimate agreement does not establish calibration, significance, causal architectural differences, annotation validity, unseen-task generalization or bitwise reproducibility of model generation.

## Audit interpretation

The studied archived M1/M3/M4 prediction-to-report score computations are internally reproducible. No scoring or subgroup denominator inconsistency was detected. **Submission clearance remains conditional**, especially for historic interval re-generation, source links for other manuscript values, protocol limits and the archived `results.rar` scope.
