# Stage 5 — Systematic Map (auto-derived from extraction.json; N=83)

## repr_primary

| value | n |
|---|---|
| hybrid | 21 |
| call_dep_graph | 16 |
| raw_window | 15 |
| embedding_retrieval | 12 |
| repo_map_skeleton | 8 |
| ast | 7 |
| cpg_dataflow | 2 |
| exec_traces | 2 |

## repr_any

| value | n |
|---|---|
| raw_window | 42 |
| embedding_retrieval | 39 |
| call_dep_graph | 31 |
| hybrid | 28 |
| ast | 22 |
| repo_map_skeleton | 12 |
| exec_traces | 4 |
| cpg_dataflow | 3 |

## mechanism

| value | n |
|---|---|
| similarity_retrieval | 25 |
| graph_guided_retrieval | 19 |
| agentic_exploration | 17 |
| learned_pruning | 7 |
| slicing_static_analysis | 6 |
| none_fixed_window | 3 |
| skeletonization | 3 |
| learned_compression | 2 |
| summarization | 1 |

## pipeline_position

| value | n |
|---|---|
| retrieval_time | 34 |
| in_loop | 30 |
| prompt_assembly | 16 |
| offline_index | 3 |

## task

| value | n |
|---|---|
| completion | 27 |
| editing_issue_resolution | 19 |
| generation | 19 |
| general_mixed | 9 |
| translation | 3 |
| qa_reasoning | 3 |
| review | 3 |

## evaluation

| value | n |
|---|---|
| unmatched_single | 38 |
| budget_matched | 29 |
| multi_change | 10 |
| demonstrated | 5 |
| not_evaluated | 1 |

## wieringa

| value | n |
|---|---|
| validation | 43 |
| evaluation | 38 |
| solution_proposal | 1 |
| philosophical | 1 |

## record_type

| value | n |
|---|---|
| system_tool | 59 |
| benchmark_eval | 14 |
| empirical_study | 8 |
| survey | 2 |

## scope

| value | n |
|---|---|
| repository | 63 |
| cross_file | 19 |
| function | 1 |

## budget_reported

| value | n |
|---|---|
| True | 58 |
| False | 25 |

## year

| value | n |
|---|---|
| 2026 | 35 |
| 2024 | 21 |
| 2025 | 19 |
| 2023 | 8 |

## peer_reviewed

| value | n |
|---|---|
| False | 60 |
| True | 23 |

## repr_primary × evaluation

| repr | budget_matched | unmatched_single | multi_change | demonstrated | not_eval |
|---|---|---|---|---|---|
| raw_window | 6 | 6 | 1 | 2 | 0 |
| embedding_retrieval | 3 | 6 | 1 | 2 | 0 |
| ast | 2 | 4 | 0 | 1 | 0 |
| call_dep_graph | 5 | 9 | 2 | 0 | 0 |
| hybrid | 8 | 9 | 3 | 0 | 1 |
| repo_map_skeleton | 2 | 3 | 3 | 0 | 0 |
| cpg_dataflow | 1 | 1 | 0 | 0 | 0 |
| exec_traces | 2 | 0 | 0 | 0 | 0 |

## RQ4: budget-matched ablations (29/83)

- RepoCoder (2303.12570): In-File vs RepoCoder varies both the presence of retrieval and its content (no cross-file budget at all vs a fixed K=10 retrieval budget); the more controlled c
- RepoBench (2306.03091): RepoBench-R's central comparison varies only the retrieval method (lexical Jaccard/Edit-Sim vs. semantic CodeBERT/UniXcoder embeddings) over the same candidate 
- MGD (2306.10763): Primary comparison (§4.1) varies only presence/absence of monitor-guided logit masking; prompting strategy, decoding parameters, and token budgets are held cons
- CrossCodeEval (2310.11248): Retriever/representation varied (BM25 lexical vs UniXCoder/ada dense embeddings) at matched top-5 snippets / 512-token budget in the retrieval-method comparison
- REPOFUSE (2402.14323): Table 1's core comparison (analogy-only vs. rationale-only vs. dual context) holds the 4096-token truncation budget fixed and varies only which context type(s) 
- R2C2-Coder (2406.01359): Table 5 ablation (with/without abstract context, with/without snippet context) varies representation composition only, holding the N=4,096-token prompt budget a
- GraphCoder (2406.07003): Both representation (CCG control/data-dependence graph vs RepoCoder's iterative regeneration-retrieval) and mechanism vary simultaneously; token counts differ b
- LongCodeArena (2406.11612): Six independent benchmark tasks each vary both the underlying model and the context-assembly strategy (raw window vs BM25/embedding retrieval vs full-repo file 
- HCP (2406.18294): Headline comparison (Random-All baseline vs HCP) varies both representation (flat concatenation vs hierarchical dependency-graph+embedding pruning) and token bu
- RTLRepoCoder (2504.08862): Table 4's RAG ablation (retrieval on vs. off) is run at the same fixed 10,240-token context window on the same >10k-token subset — the retrieval mechanism is th
- RepoScope (2507.14791): Headline comparison (Table 2, RepoScope vs. SimpleRAG/RepoCoder/DRACO/CodeAgent/RLCoder) varies both the context representation/retrieval mechanism and, only ap
- Prometheus (2507.19942): Ablations remove one agent/memory component at a time (working memory, multiple patch selection, bug reproduction, regression testing) from the full system whil
- Lindenbauer25 (2508.21433): Central comparison varies the context-management mechanism (fixed-window observation masking vs LLM-generated running summary) at run time; token budget/cost is
- SWE-QA (2509.14635): Comparison across direct prompting, sliding-window RAG, function-chunking RAG, AST-based retrieval, and agentic exploration varies representation/mechanism and 
- LongCodeZip (2510.00446): Compression method is the sole varied factor: LongCodeZip, LLMLingua variants, RAG, DietCode, SlimCode, and random pruning are compared at matched compression r
- MHRC-Bench (2601.03708): The central comparison (raw truncated whole-file concatenation vs. RepoCoder/GraphCoder/RLCoder retrieval-augmented context) holds the 2,048-token budget fixed 
- VulnResolver (2601.13933): CPCAgent and SPAAgent are added incrementally on top of a base workflow; both context representation and total token/cost budget vary together across the ablati
- SWE-Pruner (2601.16746): Table 1 compares pruning methods at fixed compression-ratio targets (4x/8x) — the pruning method is the sole varied factor at matched output budget across compa
- Stingy Context (2601.19929): comparison is 'flat methods' vs. hierarchical TREEFRAG compression — representation and budget change simultaneously (compression is itself the budget reduction
- SWE-Adept (2603.01327): Table 2's headline comparison (SWE-Adept vs. SWE-agent/RepoGraph/LocAgent/OrcaLoca) varies both representation (dependency tree with lazy skeleton loading) and 
- ReCUBE (2603.25770): central comparison (full-context vs. agent vs. agent+CCE) varies representation, retrieval mechanism, and effective context length/cost together — not a fixed-b
- SWEzze (2603.28119): Central comparison varies the compression mechanism (learned segment-relevance filtering vs generic token-level LLMLingua-2 vs perplexity-ranked LongCodeZip vs 
- LaMR (2605.15315): Compression ratio (budget) is held constant between LaMR and the reproduced SWE-Pruner baseline (Sec 4.1: 'all methods are evaluated under matched compression c
- TICoder (2606.08135): Main comparison varies the retrieval mechanism (dual-view similarity + RCG-derived usage patterns) and the test-driven iterative planning mechanism simultaneous
- SeeRepo (2606.14061): The central comparison (text-only vs. vision-only vs. multimodal SeeRepo) varies both representation and modality, and token/cost are the measured outcomes rath
- SWE-Pruner Pro (2607.18213): Table 1 compares multiple pruning methods (LLMLingua2, Selective Context, RAG, Self-Prune, LongCodeZip, SWE-Pruner, SWE-Pruner Pro) under identical agent/backbo
- Agent Retrieval Bench (2607.24882): This is the study's central comparison: representation/mechanism (lexical BM25, structural RepoMap, five embedding models, logged agentic Codex-CLI context) is 
- CodeNib (2607.25431): Eager vs Compact holds retrieved candidates identical (same top-10 dense ranking) and isolates the context-retention/delivery policy (frozen injection vs one-ti
- Paritok-4B (2608.24188): Compares Paritok-4B against GPT-5 and GPT-4.1-mini used as ad hoc compressors on the same trajectories/downstream agent (Claude Sonnet); compression ratios are 
