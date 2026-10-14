# Final results precedence and manuscript scope — 2026-10-14

## Authoritative rule (approved by study author)

The uploaded **results.rar** archive is the **final numerical authority only for the exact experiment instances it contains**. Identity must match the task, judge/generator or trained model, input condition, split/blocking scheme, repetitions/seed, and evaluation protocol. Do not infer that the archive supersedes unrelated results solely because they share a name such as M3 or M4.

1. For a matching archived experiment, use its final predictions and reports, recomputing metrics from the frozen case-level predictions wherever possible.
2. Older duplicates of **that same experiment** are superseded and must not appear in manuscript tables, abstract, discussion or conclusion as current results. Retain old source artifacts only as clearly labeled historical audit data.
3. **E1/E2 are outside this RAR's observed scope** and remain on their independently documented source and results. The reference M4 FP16 results in the RAR are not E1/rot0 and must never be substituted for the sensitivity-study baseline.
4. All other analyses **absent from the RAR remain unchanged**. In particular, do not globally overwrite M0–M4, HJI/GEE, human agreement, or other nonmatching protocol numbers.
5. Each assertion that one result supersedes another requires **experiment-key provenance**, not just equality of task/model labels.
6. Never claim complete independent replication from a subset check. An earlier **28-point manuscript-to-RAR numeric reconciliation** covered only selected M3 dual and M4 FP16 values; it did not audit every table, estimate, confidence interval or paper claim.

## Manuscript editorial pass

Local revised manuscripts dated 2026-10-14:
- `IPM_MAIN_RAR_SCOPE_CLEAN_20261014.docx` — removed 2 duplicate source-note paragraphs; numerical data and 18 tables retained.
- `IPM_SUPPLEMENT_RAR_SCOPE_CLEAN_20261014.docx` — removed 2 duplicate source-note paragraphs; numerical data and 82 tables retained.

The editorial changes do **not** assert that the reference archive settles the still-open T1 Reference FP16 versus E1/rot0 serialized-prompt discrepancy. That discrepancy concerns different experiments.

**Binary deposition boundary:** The two local DOCX files and the uploaded `results.rar` are NOT present at a verified path in this GitHub repository as of this note. This Markdown policy is an applied repository update, not a substitute for uploading the binary files. Until deposited with independently checked SHA-256 and a fresh clone readback, they must be reported as external source artifacts.

See `docs/CPU_GPU_68_INDEPENDENT_ARCHIVE_CHECK_20261013.md` for a separately scoped archive review.
