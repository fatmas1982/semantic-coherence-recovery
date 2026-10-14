# Colab E1/E2 + GEE reanalysis — 2026-10-14 (actual user ZIP, scoped)

**Superseded run:** `P2_E1E2_GEE_CPU_REANALYSIS_20261014_173134_UTC(1).zip` (auxiliary stability failed). **Latest successful run:** `P2_E1E2_GEE_CPU_REANALYSIS_20261014_175345_UTC_2.zip`.

- `E1E2_20_RECOMPUTED.log`: exit 0, **20 paired contrasts from 10,408 case-level comparison rows**, Prompt_ID bootstrap 3,000 repetitions (seed 20261009).
- `HJI_GEE_60_RECOMPUTED.log`: exit 0, **60 exploratory GEE analyses**, class-adjusted bootstrap 2,500 repetitions (seed 20261010). Exactly **one Holm-adjusted result** significant at alpha .05: `mistral_fp16_offload/T2/E1/rot1/boundary` OR **2.549867**, unadjusted p **0.000555**, Holm p **0.033287**. Observational association, not causality.
- Recomputed delta Macro-F1 across the 20 paired contrasts ranges from **-0.255448** to **0.196089**; distinct contrasts share cases, so summing change events is **not an independent-case sample size**.
- **Latest run** `HJI_GEE_STABILITY_60.log`: exit **0**: `PASS: 60 fitted GEE contrasts; minimum events=15; low-event rows=3`. Its newly generated `HJI_GEE_STABILITY_60_RECOMPUTED.csv` matched the archived stability result within reported numerical tolerance (prior audit indicated worst difference ~1.2e-14).
- The file `GEE_STABILITY_LIMITATION.txt` in the latest ZIP is **stale** and must not be used as current status. The latest distribution should omit it and supply `GEE_STABILITY_SUCCESS.txt` instead.
- The 20 and 60 primary analyses and the 60-fit independent auxiliary check all **succeeded** in the latest run. The previous stability failure remains a historical run record only.
- The author designates `results.rar` authoritative ONLY for exact experiment runs it contains. E1/E2 and HJI/GEE are independent and are not superseded by RAR M4 reference runs.

## Upload/deposition boundary

This Markdown records the verified output contents and key values. The **latest binary results ZIP and Colab notebook are not deposited in GitHub by this Markdown update**; verify the repository file tree before making any binary-deposition claim. Their copies are available in the conversation deliverable package.

The complete frozen case-level data and processing scripts remain in `data/validity_2026_10/` and `code/validity/`. The formerly missing reference CSV was available to the latest successful rerun. Do not retain the old unresolved-warning wording as the current execution status.
