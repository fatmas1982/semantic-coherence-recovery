# R8 Reproducibility Execution Audit

Date: 2026-09-19

The detached reviewer-safe one-command orchestrator was executed from the snapshot root and returned:

`PASS — current R8 reviewer-safe follow-up checks completed.`

Default-mode checks completed:
- explicit-ambiguity sensitivity recomputed from locked A1–A3 rows;
- pair-specific pre-resolution reliability recomputed with 2,000 task-stratified Prompt_ID-cluster resamples;
- exact six-field adjudication queue reproduced as 423 queued + 297 non-queued;
- computational-semantics structure diagnostics recomputed with 2,000 task-stratified Prompt_ID-cluster resamples;
- archived manuscript-used 2,000-replicate statistical-design sensitivity verified and fold/class support independently recomputed (minimum class cell = 11);
- archived adjudication-exclusion CI artifact verified and its point estimates independently recomputed;
- archived annotator-to-reference CI artifact verified and its target-level coverage/strict macro-F1 point metrics independently recomputed.

No M3/M4 retraining, relabelling, fold change, or FINAL GOLD scientific-field mutation occurred.

The default reviewer-safe path intentionally avoids repeating three slow 2,000-replicate jobs on every audit invocation. Complete scripts remain distributed and the orchestrator exposes `--recompute-statistical-bootstrap` and `--recompute-slow-ci-followups` for explicit full reruns. This is a runtime convenience, not a change to the reported estimators or frozen manuscript-used artifacts.