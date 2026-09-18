# Post-hoc Validity and Sensitivity Experiments — 2026-09

These analyses were added **after the frozen reference analyses** to test threats to interpretation. They do not replace the primary RQs, do not create new confirmatory endpoints, and are not external validation.

## Generator-associated textual signatures
An output-only anonymous six-way generator probe reaches character-TF-IDF macro-F1 **0.536** (95% Prompt_ID-cluster bootstrap CI approximately **[0.496, 0.572]**) versus nominal chance **1/6**. This shows recoverable generator-associated textual signatures; it is not a generator-quality ranking.

## Metadata-only corpus diagnostics
Task type and anonymous generator stratum were used only as prior/shortcut diagnostics. Task+generator macro-F1 is approximately 0.756/0.801/0.843/0.733 for T1–T4. These are not evaluator models.

## Strict dual blocking
Training excludes both the test Prompt_ID fold and test anonymous generator stratum. M1 falls from 0.614/0.669/0.722/0.567 to 0.559/0.593/0.519/0.380. M3 falls from 0.655/0.777/0.791/0.637 to **0.553/0.675/0.701/0.601**. Generator-associated structure therefore contributes measurably, while appreciable T2–T4 recovery remains. This is still within the observed six-stratum corpus.

## Source-bearing-only B->C restriction
For fixed-weight M4, source-bearing C-B is positive on all four targets (approximately +0.104/+0.179/+0.088/+0.085 macro-F1). M3 contrasts are heterogeneous and are not causal source-effect estimates because B/C systems are separately trained.

## ModernBERT token/truncation audit
Condition-C token lengths: median **122**, p95 **378**, max **446**, and **0** cases above 1024. Truncation is therefore not a plausible explanation for the observed M3 B/C pattern in this frozen corpus.

## Manual high-similarity review
The highest audited cross-fold prompt and prompt+source pairs showed repeated task templates or related-but-distinct instances rather than obvious duplicated substantive task instances. This does not prove absence of every latent semantic equivalence.

## M4 protocol sensitivity
The archived P1/identity predictions reproduce exactly before perturbation. Observed macro-F1 ranges are T1 **0.590–0.741**, T2 **0.535–0.609**, T3 **0.216–0.530**, and initial T4 **0.216–0.413**. The T3/T4 results are especially answer-code sensitive; interpretation is model–rubric–answer-code dependent.

## Exhaustive T4 mappings within P1/P2
All six A/B/C-to-1/2/3 bijections were evaluated under each frozen rubric phrasing: **2 × 6 = 12 variants**. Across them, macro-F1 mean = **0.317** (SD **0.078**), range **0.206–0.413**; QWK mean = **0.178**, range **0.006–0.401**. P1/identity remains macro-F1 **0.391**, QWK **0.401**. No favorable mapping is selected.

## Scientific boundary
The supported claim is **within-corpus computational recoverability under specified sampling, evidence, split, and evaluator protocols**. These post-hoc analyses do not establish external generalisation, generator-invariant semantic understanding, architecture superiority, or a universal evaluator ranking.
