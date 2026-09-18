# Validity / Sensitivity Results

This directory contains the post-hoc validity analyses added after the frozen reference analysis layer.

- `cpu/`: generator-signature probe, metadata-only diagnostics, M1 dual blocking, source-bearing-only B->C restriction, token audit, manual high-similarity review, and point-estimate reproduction checks.
- `m3_dual_block/`: strict ModernBERT prompt-fold + anonymous-generator-stratum blocking.
- `m4_protocol/`: Qwen3-8B template / answer-code perturbation results plus exact reference-reproduction check.
- `m4_t4_complete/`: all 12 T4 variants (2 frozen templates × all 6 bijective A/B/C-to-1/2/3 mappings).

These are **post-hoc validity/sensitivity analyses**, not replacements for the frozen reference results and not external validation. See `docs/VALIDITY_EXPERIMENTS_2026-09.md`.
