# SERVER_RUN_20261007_A

## Provenance

Source: Local copy of the P2 server execution
identified as SERVER_RUN_20261007_A.

The archive is stored independently from historical
M3 releases and other published experiment outputs.

## Included directories

- CPU: archived CPU execution outputs
- GPU: archived GPU execution outputs
- EXPORTS: exported experiment artifacts and bundles

LOCAL_WORK is excluded pending separate source-code
and disclosure review.

## Integrity

SHA256_MANIFEST.csv contains per-file SHA-256
digests of the copied artifacts.

The copy operation verified each copied file against
its corresponding source file.

## Verification limitations

File integrity verification does not establish:

- experimental completeness
- statistical correctness
- methodological validity
- independence of archived experiments
- successful reproduction of all reported findings

These require separate audits.

## Publication status (2026-10-17)

**Published on the dedicated branch** `publication/server-run-20261007-a` at initial archive commit `d9f97ae`; **not merged into `main`** at the time of the documented push. This is a provenance/integrity milestone, not a claim of scientific or final publication approval.

### Reported local transport and content checks

The operator reported the following checks from a Windows PowerShell workstation before the initial push:

| Check | Reported outcome | Scope |
| --- | --- | --- |
| Source-to-copy SHA-256 manifest | 4,578 / 4,578 matched | CPU, GPU, EXPORTS files |
| Staged Git index presence / filtered-hash check | 4,578 / 4,578; 0 missing or mismatched | Git index vs checkout under Git filtering |
| Raw staged Git blob SHA-256 | 4,578 / 4,578; 0 mismatches | Exact bytes in Git index vs SHA-256 manifest |
| Outer ZIP read | 70 / 70 successful | 2,834 file entries reported readable |
| Nested ZIP read | 68 / 68 successful | One additional ZIP nesting level |
| Direct text-pattern scan | 4,509 text files; 0 findings | Selected token/credential patterns |
| Outer ZIP text-pattern scan | 2,766 text entries; 0 findings | Selected patterns |
| Nested ZIP text-pattern scan | 2,756 text entries; 0 findings | Selected patterns; 0 skipped entries in this scan |

These outcomes are **operator-reported command outputs**, not an independent rerun performed by a separate auditor. No comprehensive secret detection, personally identifying information audit, binary content review, or all-depth archive traversal is claimed. Successful checks cannot establish experiment completion, accuracy of metrics, statistical inference, independence of evidence, or rights/ethics approval.

### Release boundaries and next checks

- `LOCAL_WORK/` was excluded, pending review for code provenance, dependencies, and release eligibility.
- `SHA256_MANIFEST.csv` lists the 4,578 archived input files; this manifest and this README are additional tracked files, making 4,580 staged files for the initial archive commit.
- M1/M3/M4 run directory names and presence of outputs do **not** establish completeness. Reconcile every experiment against its required folds, repeats, targets, conditions, expected case IDs, prediction rows, success/error statuses and reportable reference protocol.
- Logs include error messages (including a reported Mistral `ImportError`); no inference of universal successful completion is warranted.
- No comparison to the frozen reference layer, the latest paper/supplement, or the experiment-to-claim matrix has been independently closed by this archive addition.
- The unmerged branch is publicly readable if repository visibility is public; that does not imply merge approval or manuscript readiness.

See `docs/REPRODUCIBILITY.md` and `docs/PUBLICATION_REPRODUCIBILITY_AUDIT.md` for wider study-level boundaries.
