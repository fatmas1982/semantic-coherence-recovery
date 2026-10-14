# Post-hoc CPU and GPU robustness update (15 October 2026)

**Scope**: This follow-up is separate from the frozen runs in `results.rar`. No original RAR-authoritative experiment is superseded. The CPU E1/E2 studies remain independently frozen.

## GPU standardized T1 (completed)

Original 720 text-bearing cases from FINAL GOLD were judged with separate model-specific chat templates using the binary A=no failure, B=failure rubric. All 720 Case_IDs matched GOLD exactly once, including 246 no-failure and 474 failure cases. These are **new post-hoc protocol-dependent** observations, not historical FP16 reference replications.

|Metric|Qwen3-8B|Mistral-7B|
|---|---:|---:|
|Accuracy|0.7514|0.5014|
|Macro-F1|0.7497|0.4843|
|Balanced accuracy|0.8063|0.6213|
|Failure recall|300/474 (63.29%)|115/474 (24.26%)|
|Confusion matrix (GOLD rows, prediction columns; none, failure)|[[241,5],[174,300]]|[[246,0],[359,115]]|

Model predictions differ in 196/720 (27.22%) cases under this new test; there is no controlled model-architecture inference. Historical T1 FP16-reference versus E1/rot0 input-serialization differences remain unresolved.

The repository includes four **newly deposited** CSVs in `results/validity_2026_10/standardized_t1_gpu_posthoc/`: summary, per-class, confusion matrix, and GOLD-aligned case predictions. The full original GPU ZIP containing serialized scores and logs is **not** deposited by this commit.

## CPU sparse-event GEE (completed)

Three sparse GEE models are all Qwen T1 E2/rot1, each with 15/720 changed decisions but different human-disagreement axes. Adjusted ORs primary 2.806, boundary 1.773, severity 1.623. Nominal 95% OR intervals [0.820,9.599], [0.478,6.580] and [0.359,7.332]. All 360 leave-one-Prompt_ID-out refits completed; OR ranges were primary 1.825–3.674, boundary 1.032–2.245 and severity 0.854–2.125.

The sole Holm-surviving finding in the separate 60-fit exploratory study is Mistral T2 E1/rot1 boundary, adjusted OR≈2.550; Holm p≈0.0333 and 65/474 decision changes. It is **not** a sparse-event model. These are exploratory associations, not causal confirmation. The 30-event flag is cautionary, not an absolute inferential threshold.

The runnable CPU+GPU notebook is now deposited at `code/validity/P2_CPU_GPU_SPARSE_GEE_T1_ROBUSTNESS_20261015.ipynb`. The original CPU diagnostics archive and full GPU ZIP remain external outputs until individually uploaded and verified.

## Manuscript

Research article and Supplement Word files were revised locally in the user's conversation to incorporate the post-hoc analyses into their proper scientific sections. Those binaries are not present in the current GitHub tree and should not be claimed as deposited.

