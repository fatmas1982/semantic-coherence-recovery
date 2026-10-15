# Reproducibility and research-integrity status (15 October 2026)

## Scope and claims
This document distinguishes data already published in this repository from local, uncommitted release artifacts. **The presence of this note does not certify complete reproducibility of M0–M4.**

The following are separately auditable:
1. Archived predictions and post-hoc computational replay of selected reported metrics;
2. Historical prompt serialization and tokenization reconstruction for the T1 FP16/E1 comparison (2,880/2,880 recorded hash matches in the accompanying historical report);
3. Raw-data GEE refits, bootstrap and Wald comparisons in the published validation folders;
4. M3 dual-blocked and size-matched fold/epoch metadata extracted from archived OOF outputs, as available in the local release package.

The current repository contains some M3 dual-blocked results, the T1 serialization account, and GEE/E1E2 verification materials. **It has not been established that all 24 newly assembled historical M3 OOF files, the 120-fold ledger, the 720 generator/fold ledger, their source manifest, or updated Word manuscripts were committed to main.** Verify their presence independently before claiming public release.

## Limits that must remain explicit in the manuscript
- The GOLD reference is an internally adjudicated operational target, not independently validated ground truth.
- T2–T4 are GOLD-conditioned diagnostics rather than end-to-end detection estimates.
- Prompt-level clustered resampling conditions on the collected corpus and saved predictions; it does not capture the full variation from re-training, newly sampled generator checkpoints, or new tasks.
- Comparisons between M3 supervised recovery and M4 zero-shot LLM judging are **protocol comparisons**, not controlled model-family or architectural effects.
- A dual-blocked comparison changes both available training information and sample composition; it is not by itself a causal estimate of generator-signature shortcut dependence.
- Under sparse changes, asymptotic GEE Wald inference should be interpreted as exploratory.
- T1 input-byte reconstruction resolves the historical serialization difference, but not the causal contribution of rubric formatting to changed decisions.

## Release acceptance checklist
- [ ] Inspect released data for rights, potential confidential text and personal information before publication.
- [ ] Record a content-hash manifest for every released input, output and code artifact.
- [ ] Confirm published paths for all expected M3 original OOF files and the 120/720 ledgers.
- [ ] Verify authoring environment, checkpoint revisions, seeds, generator/fold assignment and selected epochs against archived outputs.
- [ ] Map main manuscript quantitative tables to immutable source files and aggregation scripts.
- [ ] Align *Code and Data Availability* with what is actually public at a verified commit SHA.
- [ ] Disclose inability to exactly regenerate historical trainer checkpoints when a frozen historic training implementation is unavailable.

This is a research integrity disclosure, not a report of new experiments or of new independently verified accuracy figures.
