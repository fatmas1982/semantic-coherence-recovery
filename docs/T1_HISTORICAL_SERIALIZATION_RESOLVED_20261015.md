# T1 historical serialization audit — 2026-10-15

## Scope
Two archived semantic-failure judge protocols (FP16 Reference and E1/rot0), two pinned tokenizer revisions, 720 T1 cases per judge and protocol. This is an input-provenance audit, **not** a controlled causal experiment on model decisions.

## Exact historical input reconstruction
| Judge | FP16 Reference SHA-256 matches | E1/rot0 SHA-256 matches | E1 token count matches | FP16 vs E1 equal input hashes |
|---|---:|---:|---:|---:|
| Qwen3-8B | 720/720 | 720/720 | 720/720 | 0/720 |
| Mistral-7B | 720/720 | 720/720 | 720/720 | 0/720 |

Total successful reconstruction comparisons: **2,880/2,880**. The two protocols have distinct prompts; the 2,880 hash comparisons are repeated provenance checks, not independent experimental observations.

## Exact formatting difference
FP16 Reference ends the T1 rubric with:
```text
Do not classify the subtype. Choose only A or B.
```
E1/rot0 instead ends with:
```text
Do not classify the subtype.
Choose only A or B.
```
With frozen case data, archived prompt builders, and pinned tokenizer revisions, this single newline suffices to reproduce all archived cross-protocol T1 input-hash differences, after applying each model's chat template.

## Model decision comparison (historical runs)
Qwen: 716/720 same decisions, 4/720 different; FP16 Reference macro-F1 0.7679227; E1/rot0 macro-F1 0.7707529.

Mistral: 711/720 same decisions, 9/720 different; FP16 Reference macro-F1 0.4440087; E1/rot0 macro-F1 0.4276083.

These paired historical execution differences must **not** be attributed causally to the newline: exact byte-level provenance does not control all potential execution factors. Use E1/rot0 as the internal control for E1/E2 sensitivity analysis; do not substitute the FP16 historical reference as an equivalent input protocol.

## Future work
A prospective paired intervention should vary only meaning-preserving whitespace while freezing model weights, environment, tokenization, decoding/scoring and case content; assess changed decisions, margins, macro-F1 with Prompt_ID-clustered uncertainty (120 clusters), and annotation ambiguity. Register contrasts and multiple-testing corrections a priori.

## Reproducibility boundaries
The archived 720-case judgments and their SHA-256 comparisons verify input construction, not bit-identical regeneration of predictions. The 2,880 comparisons are across two protocols × two judges × 720 cases. Original evidence files and related manuscript DOCX binaries should be uploaded independently with SHA-256 manifests. This note does not claim those binaries are in this repository.

Evidence: original FP16 OOF exports and E1/rot0 case-level CSVs recovered from the server archive, independently reconstructed in Google Colab using pinned tokenizers and the frozen GOLD source hash. Audit outcome reported by the executed verification script: `VERIFIED_SINGLE_NEWLINE_SUFFICIENT_FOR_INPUT_HASH_DISCREPANCY`; exit code 0.
