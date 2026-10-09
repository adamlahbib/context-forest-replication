# Gold-set recall audit (Study 5)

| Item | Retrieved | Passed pre-filter |
|---|---|---|
| repocoder | yes | yes |
| graphcoder | yes | yes |
| stall | yes | yes |
| codeplan | yes | yes |
| repofusion | yes | yes |
| monitor-guided decoding (official title: "Guiding Language Models of Code with Global Context using Monitors", 2306.10763) | yes | yes |
| hierarchical context pruning | yes | yes |
| aixcoder | yes | yes |
| swepruner|swe pruner | yes | yes |
| acon | yes | yes |
| repobench | yes | yes |
| crosscodeeval | yes | yes |
| a3codgen|a3 codgen | yes | yes |
| NEG:incontext autoencoder|in context autoencoder | yes | yes |
| NEG:longcoder | yes | yes |

**Gold recall: 13/13.** An initial run reported 12/13: the monitor-guided-decoding item was matched by
its community nickname, but the paper's official title never contains that phrase — it had in fact been
retrieved (2306.10763) and passed the pre-filter. The audit pattern was corrected (`merge_dedup.py`);
logged as an audit-instrument fix, not a retrieval fix. Both negative controls entered the screening
set, where they function as screening tests (expected exclusions: E2 general-text compression; E1
model-internal long context).

**Venue-check additions (search strategy 3 — DBLP over ICSE/FSE/ASE/ACL/AAAI listings, 2026-08-30):**
two records found by venue search and absent from the arXiv/OpenAlex identification set, added as
venue-check candidates for screening: "RepoGenix: Dual Context-Aided Repository-Level Code Completion"
(ASE 2024) and "Aligning LLMs to Fully Utilize the Cross-file Context in Repository-level Code
Completion" (ASE 2025). All other venue-search hits were already in the identification set
(ContextModule, RepoShapley, RepoFuse/REPOFUSE, RepoHyper, Relative-Positioning Chunking,
When-Retrieval-Hurts, Hierarchical Context Pruning, GraphCoder, aiXcoder-7B-v2).
