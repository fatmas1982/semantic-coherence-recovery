# P2 — complete reachable Git history and archive integrity audit (22 October 2026)

**Decision: Git bundle integrity, full reachable-blob read and supported nested-archive checksum/credential-pattern gates PASS. Not a scientific 100-table or absolute privacy certification; no journal-final tag.**

## Snapshot and source
- Author-supplied `P2_complete_history.bundle`, **27,840,770 bytes**, SHA-256 `1422fc788414a916d4b4ad30d99f566c93ce737746f3844f24fc3bb60f8e9e7d`.
- `git bundle verify`: PASS, complete for the included references; `git fsck --full --no-reflogs`: PASS.
- Source main and review-candidate HEAD: `14833ea7c47befab5846aefa46068508552c5af5`. **21 refs** (11 branches, 9 pull-request refs and HEAD), **0 tags** in bundle, **350 reachable commits**, **6,368 Git objects**, comprising **5,094 unique blobs, 924 trees and 350 commits**. **5,094/5,094 blob bodies read**; zero truncated/unavailable objects.
- This snapshot predates the public-verifier code fix and this audit publication, so it is not a scan of subsequent commits.

## Commit-object metadata privacy scan
All **350/350 reachable Git commit objects** were additionally inspected for credential/private-key token signatures in their metadata and commit messages: **zero tested token/key matches**. The commit objects intrinsically contain **three distinct author/committer email strings**, repeated **692** times across the historical records. Email-bearing Git history and a named public repository are **not anonymized reviewer deposits** merely because Word manuscripts omit names. Do not expose this Git mirror to reviewers under any assumption of double-anonymity; confirm IP&M's actual review route and use a separate author-neutral code snapshot if needed.

## Archives — content actually read
- **278 ZIP-compatible archive versions** including nested archives and DOCX package variants, **11,238/11,238 contained file members read** with full-read ZIP CRC validation.
- One historical `results.rar`: RAR5 independent second-pass verification of **4,584/4,584 regular members**, matching file sizes and per-file CRC-32 (0 mismatches) and normal EOF. An initial scanner warning after processing all files was traced to misclassification of a directory entry as a regular member; **resolved**, not evidence of archive damage.
- Reassembled **86** tracked Base64 parts into a public `tar.xz`; computed SHA-256 `69ce2a52c201424d8939d1a997dc3bd34854a2822131c6bc69a791b47635ce3e`, matching `BUNDLE_SHA256.txt`; inspected **152 regular files** inside it.
- No Git LFS-pointer signature was found among the reachable 5,094 blobs. This says nothing about never-committed external storage, dangling or pruned objects.

## Sensitive-data signatures — appropriately bounded
- Entire reachable blob bodies and supported archives were tested for recognizable PEM/SSH private-key blocks, GitHub tokens, OpenAI keys, AWS access keys, Google API keys, Slack tokens, assignment-like static secrets, and visible emails, IPv4 addresses and personal home paths. **Zero signatures** matched the named credential/private-key patterns. A zero signature match is not proof of zero unknown-format or encrypted secrets or lack of indirect identifiers.
- **Two email occurrences** were found in a historical SSH/Colab notebook; **two more** in the historical supplemental manuscript inside the decoded public archive. Author permissions and manuscript anonymization are separate; no email values are disclosed here.
- Numerous historical per-user home-directory paths were found in logs (2,014 pattern occurrences in the automated aggregate across direct/nested content), possibly identifying operator names and server layout. These are **not necessarily credentials**. Technical review is advised for a double-anonymized submission.
- The scan did **not** OCR embedded document images or unsafely unpickle serialized Python objects, and it does not purport to identify every possible contextual personal identifier.

## Fresh checkout and reproducibility
1. `git clone --branch main` from the supplied mirror, `python UNPACK_RELEASE.py --verify-only` PASS: 185 safe readable tar entries; standard unpack PASS, 143 missing files extracted and 9 existing paths preserved.
2. The **original** public verifier failed from the ordinary checkout because it assumed `.frozen_reference_2026/SHA256SUMS.csv` even though normal unpack places `SHA256SUMS.csv` at root. This was a reproducibility workflow path defect, not a data corruption.
3. Verified and fixed `code/analysis/verify_release_public_20261012.py` so ordinary checkout and isolated historical extraction both work and explicitly report per-file hashes: **145/151** frozen manifest matches in ordinary preserved-newer worktree, **6 intentional newer-path collisions**, versus **151/151** matches for isolated `UNPACK_RELEASE.py --historical-dir .frozen_reference_2026`. Reproduced archived public M3/M4 metrics and all four target-population/case-layer consistency checks. Source-only public verification expressly reports historical original XLSX binaries as *NOT_VERIFIED_SOURCE_BINARY*; original binaries are not silently added to public release.
4. GitHub code correction commit `a2ed7504bebcaa5a6a4dfd7b359b1974fbdf30dc`. The author-side detailed scanner scripts and redacted reports are delivered privately; no contact addresses or source binary contents are committed by this audit.

## Release gate and nonclaims
This closes **reachable repository-history reading and known credential-pattern screening / archive per-member integrity** at the documented scope. It **does not** close semantic/visual privacy review of all embedded media, missing or dangling history not referenced by the supplied bundle, full historical nested GPU trainer execution, exact journal anonymity/upload instructions, or the all-scientific-value source verification for **100 manuscript/supplement tables**.

In particular, current P2 GOLD has **35** explicit final-ambiguity flags whereas distinct historical P2_45 uses **36**, a difference already corrected in author-controlled Word drafts. Do not merge these populations. **No final/100%-verified release tag or DOI was authorized by this audit.**
