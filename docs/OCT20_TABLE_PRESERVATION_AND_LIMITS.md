# October 20 document-table preservation verification

A fresh local audit compared the **exact cell text**, including rows/cells, between the October 17 LLM-judge revision and the October 20 evidence-reconciled author copies. **20/20** main-manuscript tables and **80/80** supplement tables matched exactly at cell-text level; **0 mismatches**.

| Document | 17 October SHA-256 | 20 October SHA-256 |
|---|---|---|
| Main | `c4e5ce448dd8d2e4b29df125747ac1662d0131394054863290bf676d439b9f4e` | `663b8645b06711176315a222ac67bc5dff9890b475fddb66fa6e6872cf1000c7` |
| Supplement | `2257067df89d6c52c8adcee69774cfce3817a38a534ffcaff60fd48d5cbc2163` | `54a706a224f44440cc4d577ade55f81c702560da24b8415de39c17a74932d6be` |

**Crucial boundary:** This establishes only that the table-cell text was preserved in the editorial update. It does **not** demonstrate that any table's scientific number agrees with the frozen source case-level predictions. The 100 numerical table-to-source validations remain **UNVERIFIED**. It is not a check of visual formatting, cross-reference correctness, or labels in prose.

Reproducer: `code/analysis/verify_oct20_table_preservation.py`. To rerun, supply both versions of the main and supplement Word documents in the prescribed order. The Word source files referenced by these SHA-256 digests are author-facing local artifacts and are **not asserted to be deposited on main**.

The overarching decision remains **MAJOR REVISION / PARTIAL VERIFICATION**. See `docs/REVIEWER_EVIDENCE_RECONCILIATION_20261020.md` for the separate 56-OOF evidence scope, 23 reviewer families, and unresolved retry/protocol audits.
