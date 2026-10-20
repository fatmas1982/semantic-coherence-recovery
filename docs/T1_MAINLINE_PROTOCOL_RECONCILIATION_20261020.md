# T1 FP16 reference vs E1/rot0 — integrated evidence on main (20 October 2026)

## Mainline status: no cherry-pick necessary

The historic source note [T1_HISTORICAL_SERIALIZATION_RESOLVED_20261015.md](T1_HISTORICAL_SERIALIZATION_RESOLVED_20261015.md) is **already present on `main`**, with identical Git blob SHA `43afd1af29dd2047f5ef65880b2d1ca373310c5b` in `audit/consolidated-review-evidence-20261019`. This is verified source identity, so duplicating the historical experiment would produce contradictory copies rather than improve reproducibility.

The archived 15 October audit **reports** 2,880/2,880 successful *within-protocol* reconstructions of T1 prompt SHA-256 across FP16 and E1/rot0, both judges, and 720 case inputs per configuration. The only documented rubric-text difference between the two historical protocols is the newline:
- FP16: `Do not classify the subtype. Choose only A or B.`
- E1/rot0: `Do not classify the subtype.\nChoose only A or B.`

This explains the **serialized input-hash difference** under the archived pinned tokenizer/protocol reconstruction, not the causal reason for model decision changes. Crucially, Qwen: **0/720 different token counts** (equal counts, not zero tokens); Mistral: **720/720 different token counts**. Input hashes differ **720/720** for both judges.

## Additional direct, clean-main verification conducted on 20 October

A *separate executable check* has independently recomputed the historical FP16-versus-E1/rot0 **decisions and binary macro-F1**, using only original deposited `main` files:

- `code/analysis/verify_t1_fp16_e1_baseline_20261020.py` — Python stdlib case joins and point-estimate algebra;
- `results/validity_2026_10/T1_FP16_VS_E1_ROT0_DIRECT_PREDICTION_RECONCILIATION_20261020.csv` — independently generated source-to-source decision-difference summary;
- `.github/workflows/verify-t1-fp16-e1.yml` — executable CI verification;
- [GitHub Actions run 39451713598](https://github.com/fatmas1982/semantic-coherence-recovery/actions/runs/39451713598) — **SUCCESS**, with job log `PASS_ARCHIVED_DECISION_AND_MACROF1_RECALCULATION`.

| Judge | Case+GOLD+Prompt_ID join | Changed decisions | FP16 macro-F1 (recomputed) | E1/rot0 macro-F1 (recomputed) |
|---|---:|---:|---:|---:|
| Qwen3-8B FP16 | 720/720, no mismatches | 4 | 0.7679227037948411 | 0.7707529147241724 |
| Mistral-7B FP16 | 720/720, no mismatches | 9 | 0.4440087005037559 | 0.4276082638141963 |

E1 baseline labels come from the frozen `pred_base` in the eleven `data/validity_2026_10/paired_cases_part_*.csv` parts for `experiment=E1,variant=rot1`. The archived FP16 reference is taken from the two `results/server_runs/SERVER_RUN_20261007_A/GPU/M4_NEW/<judge>/OOF_<judge>_T1_C.csv` files. The public case IDs identifying changed decisions are recorded in the result CSV.

**Not redone in this new CI check:** historical tokenizer loading, the 2,880 SHA comparison, new GPU inference, a controlled newline-only intervention, fresh bootstrap CIs, claims about model/tokenizer causality or protocol-harmonized architecture comparisons. The 15 October report is the source of claims about precise input reconstruction; this new CI verifies independently *only* the archived prediction/score component.

## Main paper and supplementary paper — integrated edits

Edited the latest author-facing corrected Word copies from 20 October (not detached appendices):
- **Main paper**: inserted concise evidence-constrained details in the E1/E2 methodological specification (§6.9), FP16 T1 results adjacent to Table 17, and robustness discussion (§7.7).
- **Supplement**: inserted aligned methods in §S9.12a, FP16 comparison and token-count interpretation in §S9.13, and evaluator-reviewer gate qualification in the J2/J3 discussion.

All **20 main and 80 supplement original table cell strings** were compared before/after; **100/100** preserved. Neither GOLD nor original model outputs nor published table values changed. The Word documents are separate **author review artifacts** and must not be claimed as deposited to `main` by these Markdown commits.

| Author-facing deliverable | SHA-256 |
|---|---|
| `P2_MAIN_MANUSCRIPT_T1_PROTOCOL_INTEGRATED_20261020.docx` | `96fa7a3272abdeb13573f013fc071e616c8b4543bffda81bbf146ed416f11ee2` |
| `P2_SUPPLEMENT_T1_PROTOCOL_INTEGRATED_20261020.docx` | `8c2fe5d55b2d720853009140efa2843c7ede414fbb399e73c6e96b203c129dd5` |

## Correct conclusion and open gate

- **PASS (previous archived audit evidence):** the reason original T1 FP16 and E1/rot0 **input hashes differ** is the one-line-versus-newline rubric presentation, according to the 15 October pinned-source reconstruction.
- **PASS (fresh executable CI):** source-aligned 720/720 Case_ID, GOLD and Prompt_ID matching in each judge, 4 and 9 different decisions, and all four recomputed reference/control macro-F1 values.
- **NOT CLAIMED:** a causally isolated explanation of why the 4 or 9 model decisions change, exact rerun of historic model inference, or completion of broader E1/E2 protocol and 100-table manuscript audits.
- **Study reference:** use `E1/code_rot0` as the baseline for *within-E1/E2 paired perturbation analyses*, not as a byte-identical replacement for original FP16 Table 17 reference. These are distinct recorded implementations with different input serializations.

**Do not label the T1 byte-level reconstruction as a newly reexecuted experiment merely because this note and the independent archived-output CI are added to `main`.**
