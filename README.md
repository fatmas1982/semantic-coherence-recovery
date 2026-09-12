# Semantic Coherence Recovery

**From Reliable Human Annotation to Computational Recovery of Semantic Coherence Failures in Small Language Models**

This repository is the public reproducibility package for a study that links a reliability-tested human annotation layer to computational recovery of semantic-coherence failures in small-language-model (SLM) outputs.

## What is released

- the 120-prompt diagnostic bank and six-model generation plan;
- all 720 retained SLM outputs used in the study;
- generation provenance/configuration and a best-effort reconstruction runner;
- the locked annotator manual (GitHub-readable text export) and blank annotation sheets;
- FINAL GOLD v1.0 and the frozen computational-baseline workbook;
- M3 ModernBERT out-of-fold predictions, stability runs, ablations, robustness and leakage-audit outputs;
- the valid target-isolated M4 Qwen3-8B forced-choice predictions and summaries;
- post-hoc task-conditioned source-utility and human-machine uncertainty analyses;
- notebooks/scripts used to verify or reproduce the computational analyses;
- GitHub-readable Markdown exports of the P2_57 submission-candidate manuscript and supplement; the submission DOCX files contain the same public repository URL in their Data/Code Availability statements.

## Central scientific question

The study asks whether fine-grained semantic-coherence distinctions can first be applied reliably by humans and then recovered computationally. The four downstream targets are:

| Target | Decision | N |
|---|---|---:|
| T1 | failure vs no_failure | 720 |
| T2 | semantic_only vs grounding_involved among failures | 474 |
| T3 | Core_SCF vs OVR mechanism family | 460 |
| T4 | severity 1 vs 2 vs 3 among failures | 474 |

The final results support a staged distinction:

> **failure detection is not the same task as fine-grained diagnosis, and neither is the same as severity assessment.**

## Repository map

```text
.
├── README.md
├── CITATION.cff
├── LICENSE
├── DATA_LICENSE.md
├── code/
│   ├── generation/      # generation-plan builder + reconstructed SLM generation runners
│   ├── annotation/      # sheet preparation, validation, merge, IAA utilities
│   ├── analysis/        # frozen CPU-baseline verification notebook
│   ├── m3/              # reportable ModernBERT notebook
│   ├── m4/              # reportable Qwen3-8B forced-choice notebook
│   └── followup/        # source-utility and uncertainty analyses
├── data/
│   ├── prompts/         # prompt bank + 720-row crossed generation plan
│   ├── provenance/      # model registry + generation configuration
│   ├── raw/             # 720 generated outputs + per-model output files
│   ├── annotation/      # blank annotation/codebook templates
│   ├── frozen/          # FINAL GOLD, baseline workbook, targeted re-review pack
│   ├── computational/   # M3/M4 OOF predictions and result artifacts
│   └── followup/
├── docs/
│   ├── REPRODUCIBILITY.md
│   ├── GENERATION_PROVENANCE.md
│   ├── ANNOTATION_PROTOCOL.md
│   ├── DATA_CARD.md
│   ├── FILE_MAP.md
│   └── ANNOTATOR_MANUAL_v1.2_final_locked.txt
├── archive/
│   └── legacy_m4_invalid/  # audit-only superseded M4 materials
├── paper/                  # P2_57 manuscript + supplement as Markdown exports
└── SHA256SUMS.csv
```

## One-command complete release extraction

The complete organized reproducibility tree is also shipped as seven text-safe bundle parts in `release_bundle/`. After cloning, run:

```bash
python UNPACK_RELEASE.py
python code/release/reconstruct_binary_assets.py
```

`UNPACK_RELEASE.py` verifies the tar.gz SHA-256 before extraction. The second command reconstructs and verifies the exact frozen XLSX/PDF binary inputs from their text chunks. This yields the full code/data/paper tree documented below. Key documentation and scripts are also exposed directly at repository root for quick inspection.

## Fastest exact reproduction path

If your goal is to reproduce the **reported numerical analyses**, do **not** regenerate the SLM responses. Use the frozen artifacts:

1. Run `python code/release/reconstruct_binary_assets.py` to reconstruct and verify the exact frozen binaries.
2. `data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx`
3. `data/frozen/P2_CPU_Baselines_v1.0.xlsx`
4. Run `code/analysis/P2_54_Colab_01_Verify_Completed_Experiments.ipynb`.
5. Run `code/m3/P2_54_Colab_02_v3_M3_ONLY.ipynb` for the contextual encoder.
6. Run `code/m4/P2_55_Colab_M4_ONLY_Forced_Choice_Qwen3_8B.ipynb` for the reportable zero-shot LLM judge.
7. Run `code/followup/P2_55_Colab_FOLLOWUP_ANALYSES_ALL_CODE.ipynb`.

See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) for the exact order, hashes, seeds and expected outputs.

## Generation-stage reproducibility boundary

The archived 720 outputs are the authoritative generation layer used by the paper. The original run retained the prompt/model pairings, model checkpoint names, visible inputs, outputs, seed profile and the detailed M05/RWKV sampling settings. However, the exact immutable repository revision and every model-specific chat-template/tokenization/stopping detail were **not retained for M01, M02, M03, M04 and M06**.

For that reason:

- `code/generation/02_generate_model_outputs_reconstructed.py` is a transparent **best-effort reconstruction runner**;
- it should not be described as bit-for-bit reproduction of the historical generation stage;
- paper-result reproduction begins from `data/raw/generated_outputs_720.csv`, whose 720 retained outputs are frozen.

This distinction is intentional and protects the provenance record from invented settings.

## Annotation materials

The released manual is `v1.2_final_locked`. Annotators were instructed to judge each row independently, use only visible anchors, separate failure mechanism, grounding boundary, and severity, and record evidence/ambiguity fields. The repository includes blank input/template sheets.

**Important:** the `completed_annotation_sheet_A1/A2/A3.csv` files in the original generation archive are blank completion templates, not the three historical full workbooks. However, FINAL GOLD v1.0 preserves the locked pre-resolution **A1/A2/A3 primary labels, boundary zones and severity scores** for all 720 cases. For convenience, those core ratings are exported in wide and 2,160-row long formats under `data/annotation/locked_core_ratings/`, and `code/annotation/06b_human_reliability_from_gold.py` recomputes the core published IAA without using any adjudicated `Final_*` field. Secondary labels, evidence notes/spans, ambiguity fields and other workbook-only fields are not reconstructed from blank templates.

## Public-data completeness note

The public package contains the complete 120-prompt bank, all 720 frozen generated outputs, FINAL GOLD v1.0, frozen computational targets/baselines, M3/M4 OOF predictions and derived result artifacts, the locked annotation manual, the 2,160 locked pre-resolution **core** A1/A2/A3 decisions (primary label, boundary zone and severity), and the available targeted re-review workbook.

The original full A1/A2/A3 workbooks and the separate round-1 senior-adjudication workbook are not reconstructed here because their workbook-only secondary/evidence/ambiguity fields are not recoverable from the frozen publication layer currently available to this package. Blank templates are never substituted for historical ratings. This boundary is stated explicitly in the manuscript/supplement.

## Valid M4 protocol

Only the target-isolated forced-choice M4 run is reportable. The legacy free-generation M4 exposed labels outside the active target contract and is retained under `archive/legacy_m4_invalid/` for audit only. **Do not use legacy M4 metrics in scientific comparisons.**

## Data and code licences

- Code: MIT License (`LICENSE`)
- Study-created data/documentation: CC BY 4.0 intent (`DATA_LICENSE.md`)

Users remain responsible for complying with any upstream model/checkpoint terms that apply to regenerated model outputs.

## Citation

See [`CITATION.cff`](CITATION.cff). Until the article receives its final bibliographic record, cite this repository and the manuscript title.

## Repository

https://github.com/fatmas1982/semantic-coherence-recovery

## Binary/text representation note

To keep every repository object diff-friendly while preserving exact frozen bytes, the original FINAL GOLD workbook, CPU-baseline workbook, targeted re-review workbook, and locked annotator-manual PDF are stored as base64 text chunks under `data/frozen/binary_payloads/`. Run `python code/release/reconstruct_binary_assets.py` once after cloning; the script reconstructs the exact binaries and verifies their SHA-256 hashes. GitHub-readable CSV/text mirrors are provided alongside them. `SOURCE_BINARY_HASHES.csv` records the source hashes for the manuscript/supplement text mirrors as well.
