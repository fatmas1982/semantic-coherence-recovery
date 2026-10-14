# Colab E1/E2 + GEE reanalysis — 2026-10-14 (actual user ZIP, scoped)

Uploaded result ZIP: `P2_E1E2_GEE_CPU_REANALYSIS_20261014_173134_UTC(1).zip`.

- `E1E2_20_RECOMPUTED.log`: exit 0, **20 paired contrasts from 10,408 case-level comparison rows**, Prompt_ID bootstrap 3,000 repetitions (seed 20261009).
- `HJI_GEE_60_RECOMPUTED.log`: exit 0, **60 exploratory GEE analyses**, class-adjusted bootstrap 2,500 repetitions (seed 20261010). Exactly **one Holm-adjusted result** significant at alpha .05: `mistral_fp16_offload/T2/E1/rot1/boundary` OR **2.549867**, unadjusted p **0.000555**, Holm p **0.033287**. Observational association, not causality.
- Recomputed delta Macro-F1 across the 20 paired contrasts ranges from **-0.255448** to **0.196089**; distinct contrasts share cases, so summing change events is **not an independent-case sample size**.
- `HJI_GEE_STABILITY_60.log`: exit **1** because `data/validity_2026_10/HJI_60_CORRECTED_CI_SEED_20261010.csv` was missing from the Colab checkout. **The independent 60-fit stability rerun did not pass**. Its already-bundled `HJI_GEE_STABILITY_60.csv` should not be represented as a fresh successful output; it may be a previously downloaded file.
- The 20 and 60 primary analyses **succeeded**; the auxiliary reference-matching stability check **failed due to missing input file**.
- The author designates `results.rar` authoritative ONLY for exact experiment runs it contains. E1/E2 and HJI/GEE are independent and are not superseded by RAR M4 reference runs.

## Upload/deposition boundary

This Markdown records the verified output contents and key values. The **23-KB binary results ZIP and the notebook have not been deposited as binary repository files in this update**, because the connected GitHub write API in the current runtime cannot consume local binary file paths. Do not claim the results archive or notebook source was uploaded by this provenance document.

The complete frozen case-level data and processing scripts remain in `data/validity_2026_10/` and `code/validity/`. The missing reference CSV is part of the repository data tracked separately; a repaired notebook should retrieve this exact source prior to attempting the stability audit.
