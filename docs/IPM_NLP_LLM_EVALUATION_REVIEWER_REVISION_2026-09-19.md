# Reviewer 2 — NLP / LLM Evaluation revision

Date: 2026-09-19
Target: Information Processing & Management (IP&M)

This revision is interpretive/presentation-only. FINAL GOLD v1.0, frozen Prompt_ID folds, T1–T4 populations, M0–M4 predictions, and all reported metrics remain unchanged. No retraining, relabelling, remapping, new evaluator, or result selection was performed.

Implemented changes:
- reframed M3–M4 from conventional model comparison to contrasts among specified evaluator protocols;
- labelled the archived Qwen3-8B P1/identity configuration wherever headline M4 scores are reported;
- surfaced T2–T4 gold-conditioned eligibility in the abstract and primary-results table;
- replaced general “evidence ablation” terminology with “evidence-condition comparison”, while retaining the distinction between fixed-weight M4 inference comparisons and separately trained M3 B/C systems;
- added explicit rationale for selecting ModernBERT-base and Qwen3-8B;
- added the interpretation boundary that M4 results pertain to the executed 4-bit NF4-quantised Qwen3-8B scoring configuration and were not re-tested under full precision;
- retained T4 as a secondary ordinal diagnostic target without adding a new ordinal model.

No new experiment was required for Reviewer 2.