# Reviewer 6 — Computational Semantics / Discourse revision

Date: 2026-09-19
Target: Information Processing & Management (IP&M)

This revision clarifies the linguistic interpretation of the locked taxonomy and adds two descriptive frozen-data structure diagnostics. No annotation label, FINAL GOLD decision, target definition, model prediction, fold, or computational point estimate was changed.

## Source provenance clarified

The current validation manuscript uses Annotation Manual v1.2_final_locked as the authoritative annotation instrument. The locked manual already assigns SCF-01–SCF-07 to the core_semantic family; OVR-01 and OVR-05 to overlap_or_semantic; OVR-02/03/04/06 to overlap; HREF to background_or_overlap; and NONE to none. The current manuscript therefore does not retroactively derive these families from the new analyses.

A separate conceptual manuscript, “Semantic Coherence Failures in Small Language Models: A Taxonomy and Boundary Framework beyond Hallucination” (IJHCS-D-26-01005), is currently under review. It develops the conceptual taxonomy/boundary framework and reports a separate 400-output AI-assisted pilot. The present IP&M paper does not claim taxonomy novelty. The related manuscript is disclosed to the editor in the cover letter, while the blinded manuscript describes it generically as a separate conceptual taxonomy manuscript under review. Neither the related manuscript nor the locked Guide is uploaded to the public GitHub repository as part of this reviewer revision.

## Implemented Reviewer #6 actions

1. **Operational umbrella definition — Must fix**
   - “Semantic coherence” is now explicitly defined as an operational umbrella spanning discourse coherence proper, semantic consistency, discourse-reference continuity, and task-relative pragmatic alignment.
   - The paper explicitly rejects interpreting all codes as one narrow discourse-coherence construct.

2. **Core SCF versus OVR rationale — Must fix**
   - The SCF/OVR collapse is described as an operational super-family inherited from the locked manual, not a discovered latent linguistic dichotomy.
   - Core SCF captures primarily internal continuity/alignment relations.
   - OVR captures inconsistency, misattribution, context/state conflict, reasoning-answer mismatch, and mixed-context synthesis.
   - OVR is not equated with the overlap grounding boundary because OVR-01 and OVR-05 can be semantic_only or overlap.

3. **T3 interpretive boundary — Must fix**
   - T3 is now described as operational code-family discrimination rather than a grounding-invariant latent mechanism contrast.
   - The paper notes that OVR-02/03/04/06 are partly defined through conflict with visible context/grounding.

4. **QUD definition — Must fix**
   - The first occurrence now expands Question Under Discussion (QUD).

5. **Construct-to-theory traceability — Strongly recommended**
   - Added Supplementary Table S4A mapping each operational code to its linguistic object/theoretical lineage and closest precedent.
   - This is traceability, not a claim that a linguistic theory uniquely entails the study label.

6. **T3 family × grounding diagnostic — Strongly recommended and executed**
   - Population: 460 T3-eligible Core-SCF/OVR cases.
   - Core SCF: 286/333 semantic_only (85.9%), 47/333 overlap (14.1%).
   - OVR: 10/127 semantic_only (7.9%), 117/127 overlap (92.1%).
   - Cramér’s V = .728; 95% task-stratified Prompt_ID-cluster bootstrap CI [.675, .776].
   - The result confirms strong association while also showing that family and grounding are not identical.

7. **Task × mechanism-family diagnostic — Strongly recommended and executed**
   - Population: 720 FINAL GOLD cases; 120 Prompt_ID clusters.
   - Cramér’s V = .251; 95% task-stratified Prompt_ID-cluster bootstrap CI [.227, .295].
   - Explanation and instruction-following are Core-SCF-heavy; multi-entity/context tracking and question answering show larger OVR shares; HREF is most visible in source-grounded generation.
   - The result supports interpreting cross-task transfer as partly exposed to task-conditioned family composition.

## Association equation and inference policy

The Supplement reports:

    V = sqrt(chi^2 / [N * min(r - 1, c - 1)])

and row-conditional proportions:

    p_ij = n_ij / sum_j n_ij

Ninety-five per cent intervals for V use 2,000 task-stratified Prompt_ID-cluster bootstrap resamples (seed 20260919), preserving all six checkpoint outputs attached to each sampled prompt. No p-value is interpreted because the prompt bank and corpus are purposively constructed.

## Reproducibility assets

- code/followup/P2_IPM_COMPUTATIONAL_SEMANTICS_STRUCTURE_DIAGNOSTICS.py
- results/followup/P2_IPM_T3_FAMILY_BY_GROUNDING_CROSSTAB.csv
- results/followup/P2_IPM_TASK_BY_MECHANISM_FAMILY_CROSSTAB.csv
- results/followup/P2_IPM_COMPUTATIONAL_SEMANTICS_ASSOCIATION_SUMMARY.csv

The script reads the released FINAL GOLD workbook at data/frozen/P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx after running UNPACK_RELEASE.py.

## Not performed because Reviewer #6 marked them not required

- taxonomy redesign;
- re-annotation;
- a discourse parser or additional model;
- changing FINAL GOLD;
- retraining M3 or M4.
