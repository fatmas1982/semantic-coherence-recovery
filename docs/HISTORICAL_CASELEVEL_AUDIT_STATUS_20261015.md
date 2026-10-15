# Historical case-level score audit — 2026-10-15

A local audit recalculated macro-F1 and accuracy from archived CPU and GPU saved predictions: 360/360 CPU metric rows and 320/320 GPU metric rows agreed with the respective archived reports, within floating-point precision. It also checked 8/8 Table 18 source entries to three decimals. This verification does **not** rerun model training/inference, independently regenerate historical bootstrap intervals, or certify all manuscript tables. The data release for this latest audit is pending, and historical T1 serialization remains unresolved.

Source files: `P2_CPU_RESULTS_BUNDLE(5).zip`, `P2_GPU_FP16_OFFLOAD_RESULTS_BUNDLE(3).zip`. Preserve experiment identity: `results.rar` remains authoritative only for exact matching archived runs.

Expected publication folder: `results/validity_2026_10/historical_caselevel_audit_20261015/`.
