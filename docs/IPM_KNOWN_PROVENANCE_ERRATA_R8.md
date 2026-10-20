# R8 Known Provenance Erratum and Review-Sanitization Record

## Historical metadata discrepancy

The preserved historical `P2_FINAL_SENIOR_ADJUDICATED_GOLD_v1.0.xlsx` binary contains a stale workflow-summary value:

- `Senior adjudication round-1 cases = 394`

That summary cell is not used in any case-level analysis. The authoritative workflow count is **423**, established by three convergent sources:

1. the mechanically reproducible six-field A1–A3 disagreement rule;
2. the historical workbook's own provenance layer;
3. the archived senior-adjudication workflow and current manuscript/supplement.

The six trigger fields are primary label, secondary label, boundary zone, severity score, HREF subtype, and explicit ambiguity flag. The audit reproduces **423 queued + 297 complete-agreement = 720**.

## Governance handling

The historical source binary is not silently overwritten or re-versioned. For blinded review, a detached reviewer-safe derivative corrects only the stale summary metadata and replaces identifying provenance filenames with A1/A2/A3/A4 role labels. No case-level label, family, grounding boundary, severity, target, or adjudicated scientific decision changes.

## Blinded-review privacy

The identity-bearing public GitHub repository is the canonical archival/development repository and is **not** the double-anonymous reviewer-access route. The detached reviewer-safe snapshot excludes personal names, affiliations, ORCID/profile identifiers, identifying source filenames, private correspondence, and author Git history.