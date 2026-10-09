# Stage 1 — Search Log (Study: context-structure)
**Cutoff:** 2026-08-30 · **Window:** 2023-01-01 – 2026-08-30 · English, retrievable.
Sources: arXiv API (>=3 s throttle) + OpenAlex. Runners: `run_search.sh` (topic), `run_known_items.sh`
(known-item seeds + borderline/negative controls). Recall audit: `_gold_recall.md`.

## Topic queries (verbatim strings; hits = raw rows returned)

| Query | File | Hits |
|---|---|---|
| repository-level code completion context LLM (arXiv) | ax_repocomp.jsonl | 39 |
| repository level code generation context retrieval (arXiv) | ax_repogen.jsonl | 37 |
| abstract syntax tree LLM code context prompt (arXiv) | ax_ast.jsonl | 22 |
| call graph dependency context code large language model (arXiv) | ax_callgraph.jsonl | 37 |
| repo map skeleton code agent context (arXiv) | ax_repomap.jsonl | 27 |
| context compression coding agent LLM (arXiv) | ax_ctxcompress.jsonl | 34 |
| code context pruning selection completion LLM (arXiv) | ax_prune.jsonl | 31 |
| static analysis context code completion language model (arXiv) | ax_static.jsonl | 30 |
| structure-aware code retrieval augmented generation (arXiv) | ax_structrag.jsonl | 36 |
| code property graph retrieval LLM generation (arXiv) | ax_cpg.jsonl | 35 |
| cross-file context code completion benchmark (arXiv) | ax_crossfile.jsonl | 34 |
| context window budget tokens coding agent (arXiv) | ax_budget.jsonl | 29 |
| repository knowledge graph code generation LLM (arXiv) | ax_kg.jsonl | 29 |
| agent codebase exploration navigation context (arXiv) | ax_explore.jsonl | 19 |
| prompt construction repository code LLM cross-file (arXiv) | ax_promptcon.jsonl | 38 |
| issue resolution context localization repository agent (arXiv) | ax_issue.jsonl | 31 |
| repository-level context code large language model (OpenAlex) | oa_repo.jsonl | 40 |
| abstract syntax tree context large language model code (OpenAlex) | oa_ast.jsonl | 40 |
| context compression code generation LLM (OpenAlex) | oa_compress.jsonl | 40 |
| cross-file code completion context retrieval (OpenAlex) | oa_crossfile.jsonl | 40 |

## Known-item / control queries (max 5 each)

| Query | File | Hits |
|---|---|---|
| RepoCoder repository-level code completion iterative retrieval (arXiv) | ki_repocoder.jsonl | 5 |
| GraphCoder repository code completion code context graph (arXiv) | ki_graphcoder.jsonl | 4 |
| STALL boosting LLM repository code completion static analysis (arXiv) | ki_stall.jsonl | 5 |
| CodePlan repository-level coding planning LLM (arXiv) | ki_codeplan.jsonl | 5 |
| RepoFusion training code models to understand your repository (arXiv) | ki_repofusion.jsonl | 4 |
| monitor-guided decoding code language models static analysis (arXiv) | ki_mgd.jsonl | 4 |
| hierarchical context pruning repository code completion (arXiv) | ki_hcp.jsonl | 4 |
| aiXcoder long context repository code completion training (arXiv) | ki_aixcoder.jsonl | 5 |
| SWE-Pruner self-adaptive context pruning coding agents (arXiv) | ki_swepruner.jsonl | 3 |
| ACON optimizing context compression long-horizon agents (arXiv) | ki_acon.jsonl | 5 |
| RepoBench benchmarking repository-level code auto-completion (arXiv) | ki_repobench.jsonl | 5 |
| CrossCodeEval cross-file code completion benchmark (arXiv) | ki_crosscodeeval.jsonl | 5 |
| A3-CodGen repository-level code generation local global third-party (arXiv) | ki_a3codgen.jsonl | 3 |
| in-context autoencoder context compression large language model (arXiv) | ki_nc_icae.jsonl | 3 |
| LongCoder long-range pre-trained language model code completion (arXiv) | ki_nc_longcoder.jsonl | 3 |

**Total raw rows: 731.** Dedup (normalized title -> Jaccard >= 0.8) and pre-filter in `merge_dedup.py`;
per-record outcomes in `identified.jsonl`. Manual venue checks (strategy 3, DBLP sweeps) and their
outcomes are logged in `_gold_recall.md` and `../stage2_screening/decisions_adjudication.json`.
Deviation D1: the protocol's post-screening backward/forward snowballing pass was not executed (logged).
