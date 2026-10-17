# RAR recovery audit: partial extraction (17 October 2026)

User-supplied metadata-only `P2_RAR_RECOVERY.zip` was independently inspected; ZIP CRC passes. `RECOVERY_SUMMARY.json` reports correct source RAR SHA-256 `58493dc555ef95be1876416731723d71bb9c40ead2585e1b3bbafaad6ef7815d`, size 13,195,705 bytes, but `unar 1.10.1` returned code 1.

The extracted SHA manifest contains 4,584 **path entries**, NOT 4,584 proven intact files. 327 distinct paths failed with `Attempted to read more data than was available`; all 327 of these have zero-byte entries. There are 330 zero-byte entries in total, including 3 without an explicit extraction error. Failures by top-level run area: WORKER_LOGS 134, M1_COMPLETE 94, M3_COMPLETE 66, EXPORTS/experiments 22, M4_NEW 8, EXPORTS/CPU_summary 1, EXPORTS/GPU_FP16_OFFLOAD_summary 1, EXPORTS/M3_T4_size_matched_r3_C.zip 1.

**Status: BLOCKED** for complete RAR case-level replay and raw statistical recomputation. SHA-256 of the RAR confirms **transport identity**, not that extraction succeeded. The recovered directory should not be treated as a complete, verified experiment archive; do not calculate publication values from zero-byte or partial files.

Next: recover the original uncompressed files from the source server or copy the original nested ZIP bundles separately; hash and compare *every* required member against an authoritative source manifest. A different modern RAR extractor is another option, but do not presume success. Treat nested archives extracted via this failed run as untrusted until separately verified. Existing GitHub case-level OOF is independent evidence only for its stated scope.

No new model training, bootstrap or GEE refitting was performed; external human validation remains deferred.
