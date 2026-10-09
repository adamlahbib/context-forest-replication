# Seeing the Forest: A Systematic Mapping of Structure-Aware Context Engineering for Repository-Level Code LLMs and Agents

<!-- SOURCE OF report.md. Edit this file, never report.md: every corpus count is a double-brace placeholder
filled by render_report.py from stage5_map/_map_stats.json. -->

## Abstract

Code LLMs and coding agents see a repository only through the context they are given, and a large design space now builds that context from syntax trees, call and dependency graphs, repository maps, retrieved snippets, and compression. A common claim is that structured context beats flat retrieval, but structured context often also changes how much the model sees. We map {{N}} studies (2023–2026) by what the context is made of, how it is selected, and how gains are tested, and we re-read the full text of every study with a comparison ({{evaudit.n}}) to check whether the context budget was held fixed. {{evaudit.final.budget_matched}} studies hold the budget fixed, or show that the structured variant uses no more of it. Only {{evaudit.svf.n}} of these compare structured against flat context; {{evaudit.svf.structure_better}} favour structure, {{evaudit.svf.flat_better}} favour flat context, and {{evaudit.svf.no_difference}} show no clear difference. The other comparisons change the amount of context or several things at once. Structure may help, but the controlled evidence is thin and mixed, not absent. We close with evaluation practices that would settle the question.

**Keywords:** code LLMs, coding agents, repository-level context, context engineering, retrieval-augmented generation, code graphs, systematic mapping study

## I. Introduction

A code LLM or coding agent sees a repository only through the context it is given, and repositories do not fit in a context window. A design space has grown around building that context: syntax trees, call and dependency graphs, repository maps and skeletons, static-analysis slices, embedding retrieval, and methods that compress all of these into a token budget. A common claim in this literature is that *structured* context beats *flat* retrieval. That claim is hard to test, because a structured context usually also differs in *how much* it gives the model: a comparison that changes both cannot tell which one helped.

We map this design space with a systematic mapping study and four research questions:

- **RQ1 (Representation).** What is the context made of: raw windows, ASTs, call or dependency graphs, repository maps, retrieved snippets, or combinations?
- **RQ2 (Mechanism).** How is it selected or compressed, and at which point in the pipeline?
- **RQ3 (Budget).** What trade-offs between token budget and task quality are measured?
- **RQ4 (Evidence).** Which comparisons hold the context budget fixed while varying the representation, and what do they show?

Table: Main findings, by strength of evidence.

| Finding | Evidence | Main limitation | Implication |
|---|---|---|---|
| Hybrids and graph-based context lead the design space; agents increasingly select context themselves (RQ1–2) | Descriptive | Representation κ is moderate | Taxonomies of this field should state their hybrid rule |
| Budgets are reported far more often than controlled (RQ3) | Descriptive | Trade-off papers optimise the trade-off | Report realised tokens per arm |
| {{evaudit.svf.n}} matched structured-vs-flat comparisons: {{evaudit.svf.structure_better}} favour structure, {{evaudit.svf.flat_better}} flat, {{evaudit.svf.no_difference}} neither (RQ4) | Controlled, but few and heterogeneous | Ten of the {{evaudit.final.budget_matched}} matched studies only share a cap | "Structure beats flat retrieval" is plausible, not established |
| Structure as a relevance prior that spends a budget better | Hypothesis | Not tested directly by any study | Test with matched budgets across representations |

Section II describes the method, Section III the map (RQ1–RQ3), Section IV the evidence audit (RQ4), Section V the implications and recommended evaluation practices, and Section VI the threats to validity.

## II. Method

We follow Petersen et al.'s mapping process [@petersen2008systematic; @petersen2015guidelines] with Kitchenham and Charters' screening practice [@kitchenham2007guidelines]. Research questions, search strings, eligibility criteria, the facet scheme, sampling seeds, and the screening cap were fixed in a protocol before retrieval; deviations are numbered, logged amendments.

### Search

We ran scripted arXiv and OpenAlex queries (2023-01-01 to 2026-08-30), known-item seed queries, and venue checks of ICSE/FSE/ASE, ICLR/NeurIPS/ICML, and ACL/EMNLP. A quasi-gold standard of 13 known items, including negative controls, was retrieved and handled as designed (13/13). The planned citation snowballing was not run (deviation D1); Section VI reports a bounded substitute.

### Screening, and what the cap removed

Table: Selection funnel. The pre-filter, not the cap, removed most records.

| Stage | Records |
|---|---|
| Unique records retrieved | {{funnel.identified}} |
| Removed by the keyword pre-filter (code, context mechanism, LLM) | {{funnel.prefilter_removed}} |
| Passed the pre-filter | {{funnel.prefilter_pass}} |
| Removed by the 200-record cap (seeded random draw) | {{funnel.cap_removed}} |
| Screened on title and abstract | {{funnel.screened}} |
| Reached full-text extraction | {{funnel.extracted}} |
| Excluded at full text (reasons logged per record) | {{funnel.demoted}} |
| **Included corpus** | **{{N}}** |

The protocol capped screening at 200 records, drawn by a seeded random sample if more passed the pre-filter, to bound screening effort before the size of the literature was known. In the event only {{funnel.prefilter_pass}} records passed, so the cap removed {{funnel.cap_removed}}; both were screened afterwards and both are exclusions ({{prefilter_check.cap_included}} eligible). The cap therefore did not shape the corpus. The keyword pre-filter did, and Section VI measures how much it missed.

A study was included if it concerns an LLM code task at repository or cross-file scope, or context construction or compression for code LLMs at any scope (I1); contributes or studies a context mechanism (I2); is detailed enough to code (I3); and is from 2023–2026, in English, and retrievable (I4). Exclusions covered model-internal long-context work only, general-text RAG with no code instantiation, structure for non-LLM models, function-level prompting with no cross-file or budget concern, duplicates, and unretrievable records.

A seeded 20% sample (n = {{screening_dual.n}}) was screened again blind: include-versus-not agreement was {{screening_dual.agree_binary}}/{{screening_dual.n}} (κ = {{screening_dual.kappa_binary}}); over include, exclude, and uncertain it was {{screening_dual.agree_3way}}/{{screening_dual.n}} (κ = {{screening_dual.kappa_3way}}), with no include–exclude conflict.

### Classification scheme

Each study is coded on representation, mechanism, pipeline position, task, scope, evaluation, Wieringa research type [@wieringa2006requirements], and record type. Table III defines the representation classes and the boundary that caused most disagreement.

Table: Representation classes: operational definition and an example. One primary class per study; all classes present are also recorded.

| Class | The context given to the model is... | Example |
|---|---|---|
| Raw window | contiguous text from the current file, not retrieved | RepoCoder's in-file prompt [@zhang2023repocoder] |
| Embedding retrieval | snippets selected by lexical or dense similarity (rule R1) | CrossCodeEval's retrieved context [@ding2023crosscodeeva] |
| Call/dependency graph | code selected or ordered by call, import, or type edges | HCP's dependency-pruned prompt [@zhang2024hcp] |
| AST | code or facts derived from the syntax tree | Monitor-guided decoding [@agrawal2023mgd] |
| CPG/dataflow | code selected by data- or control-flow relations | DraCo's dataflow-guided retrieval [@cheng2024draco] |
| Repository map/skeleton | a compressed whole-repository view (signatures, structure) | Stingy Context's skeleton |
| Execution traces | runtime or agent-trajectory content | Observation masking of agent histories [@lindenbauer2025lindenbauer2] |
| Hybrid | two or more of the above as *co-equal* parts of the contribution | REPOFUSE's analogy plus dependency context [@liang2024repofuse] |

*The hybrid boundary.* A study is hybrid only when its contribution is the combination; if one family carries the contribution and another is incidental, the study takes that family's class. Most coding disagreements were exactly this judgement: of the {{kappa_coding.repr_disagreements}} representation disagreements in the blind re-coding, {{kappa_coding.repr_disagreements_hybrid}} involve the hybrid class. Two examples: VulnResolver's context is a natural-language analysis report with embedded snippets; the extractor coded call graph, the second coder raw window, and adjudication hybrid. Kovrigin24's agent searches the AST with no call graph in the paper; the extractor coded call graph, the second coder hybrid, and adjudication AST.

### Extraction, verification, reliability, and adjudication

LLM agents (Claude, Anthropic) extracted each study from its full text under a written codebook. A separate agent re-checked every extracted number at source: {{verification.claims}} claims, {{verification.confirmed}} confirmed ({{verification.pct_confirmed}}%), {{verification.wrong}} wrong and corrected. A second agent of the same model family re-coded all {{kappa_coding.n}} studies blind. Before adjudication, κ was {{kappa_coding.mechanism.kappa}} for mechanism, {{kappa_coding.evaluation.kappa}} for evaluation, and {{kappa_coding.repr_primary.kappa}} for representation.

*How disagreements were resolved.* Each disagreement was decided by an author against the full text. For representation, a disagreement was decided by the boundary rule above; for evaluation, by the definitions in Table IV. The taxonomy was refined once: rule R1 (retrieved snippets code as embedding retrieval, whatever the retriever) was added when two verifiers flagged retrieval records in opposite directions, and it was then applied to the whole corpus. No class was added or removed after the second coding.

*Evidence audit.* RQ4 depends on whether each comparison holds the context budget fixed, so we re-read the full text of all {{evaudit.n}} studies that compare against an alternative and assigned one of the levels in Table IV. Two checkers worked independently on the same pinned texts: Claude agents, and GPT (OpenAI) given only the paper text and the rule. Each recorded the model and configuration, dataset and metric, budget control, what each arm shows, and anything else that changed (Supplementary Table S2). When a paper contains several comparisons, the cleanest counts.

Table: Evaluation levels for RQ4. "Matched" requires the same model and configuration on the same dataset and metric.

| Level | Definition |
|---|---|
| Budget-matched | Only the representation or selection mechanism differs, and the budget is held: both arms fill the same hard cap, per-arm usage is reported equal, or the structured arm is reported to use no more (tokens, or dollar cost where that is all that is reported) |
| Unmatched | Only the representation or mechanism differs, but the amount of context differs or is not controlled |
| Multi-change | The model, agent scaffold, number of model calls, training, or several components also differ |
| No comparator | No quantitative comparison with an alternative |

The checkers agreed on {{evaudit.agree}} of {{evaudit.n}} studies (κ = {{evaudit.kappa}}). Most disagreements were one question, whether a shared cap or a smaller structured arm counts as matched, which Table IV settles; a third full-text pass recorded the budget tier of every matched candidate, and {{evaudit.decided_by_rule}} disagreements were resolved by that rule. For the remaining {{evaudit.decided_by_authors}}, an assistant proposed a verdict with both checkers' comparisons and a quote, and an author checked it against the paper and accepted it in every case. The same pass recorded whether each matched comparison sets structured context against flat context. The audit replaced the original evaluation codes: of the {{evaudit.was_budget_matched}} studies first coded budget-matched, {{evaudit.kept_budget_matched}} remain so.

### Synthesis

Synthesis is descriptive: frequency counts and cross-tabulations, plus narrative synthesis per cell. Following Petersen, studies are not quality-scored; the evaluation facet records the strength of each comparison instead. Tasks, benchmarks, and metrics differ too much to pool effect sizes, so none are pooled.

### Data availability

The protocol, search strings and hit counts, all screening and adjudication decisions, the extraction database, verification and audit records, and the scripts are released at @@DATA_URL@@. The release regenerates every corpus count and statistic in this paper.

## III. The Map (RQ1–RQ3)

**RQ1: hybrids and graphs lead.** Hybrids are the largest primary class ({{repr_primary.hybrid}}), followed by call/dependency graphs ({{repr_primary.call_dep_graph}}), raw windows ({{repr_primary.raw_window}}), embedding retrieval ({{repr_primary.embedding_retrieval}}), repository maps ({{repr_primary.repo_map_skeleton}}), ASTs ({{repr_primary.ast}}), CPG/dataflow ({{repr_primary.cpg_dataflow}}), and execution traces ({{repr_primary.exec_traces}}). Graph-structured classes (call/dependency graph, AST, CPG) together hold {{n_graph_class}} studies.

**RQ2: retrieval-time selection and in-loop agents dominate.** By mechanism, similarity retrieval ({{mechanism.similarity_retrieval}}), graph-guided retrieval ({{mechanism.graph_guided_retrieval}}), and agentic exploration ({{mechanism.agentic_exploration}}) lead; pruning ({{mechanism.learned_pruning}}), slicing ({{mechanism.slicing_static_analysis}}), skeletonisation ({{mechanism.skeletonization}}), compression ({{mechanism.learned_compression}}), and summarisation ({{mechanism.summarization}}) are smaller. By pipeline position, context is built at retrieval time in {{pipeline_position.retrieval_time}} studies and inside an agent loop in {{pipeline_position.in_loop}}; offline indexing is rarely the contribution ({{pipeline_position.offline_index}}). Agentic exploration moves the budget question rather than answering it: an agent's context is assembled by its trajectory, so its size varies per task and is hard to compare across systems.

**RQ3: budgets are reported more often than they are controlled.** {{budget_reported.true}} of {{N}} studies report a token budget. Where trade-offs are measured, they point the same way: compression and pruning often keep quality at a fraction of the tokens (LongCodeZip [@shi2025longcodezip], SWE-Pruner [@wang2026swepruner]), and more context is not monotonically better (EVOR's returns flatten beyond mid-range budgets [@su2024evor]). These results come mostly from papers built to optimise the trade-off, so they describe what is measured, not typical practice.

Table: Facet distributions (n = {{N}}).

| Facet | Value | n | Facet | Value | n |
|---|---|---|---|---|---|
| Task | completion | {{task.completion}} | Scope | repository | {{scope.repository}} |
| | issue resolution | {{task.editing_issue_resolution}} | | cross-file | {{scope.cross_file}} |
| | generation | {{task.generation}} | Research type | validation | {{wieringa.validation}} |
| | mixed | {{task.general_mixed}} | | evaluation | {{wieringa.evaluation}} |
| | translation / QA / review | {{task.translation}} / {{task.qa_reasoning}} / {{task.review}} | Record type | system/tool | {{record_type.system_tool}} |
| Peer-reviewed | yes | {{peer_reviewed.true}} | | benchmark | {{record_type.benchmark_eval}} |
| | no | {{peer_reviewed.false}} | | empirical study | {{record_type.empirical_study}} |

**Preprints versus peer-reviewed studies.** Only {{peer_reviewed.true}} of {{N}} studies are peer-reviewed. The two groups do not differ in evaluation discipline: {{pr_x_evaluation.peer.budget_matched}} of the {{peer_reviewed.true}} peer-reviewed studies and {{pr_x_evaluation.preprint.budget_matched}} of the {{peer_reviewed.false}} preprints have a budget-matched comparison. They differ in topic: agentic issue resolution is almost entirely preprint ({{pr_x_task.preprint.editing_issue_resolution}} of {{task.editing_issue_resolution}}), so the newest design line rests on unreviewed reports.

## IV. RQ4: Is the Structural Advantage Budget-Isolated?

**Answer: controlled comparisons exist, but few test structure against flat context, and they disagree.** Of the {{evaudit.n}} studies with a comparator, {{evaudit.final.budget_matched}} hold the budget fixed or show the structured variant uses no more of it, {{evaudit.final.unmatched_single}} change only the representation but not the amount of context, {{evaudit.final.multi_change}} change several things at once, and {{evaudit.final.no_comparator}} have no comparator after all (Table VI).

Table: Outcome of the evidence audit ({{evaudit.n}} studies with a comparator).

| Level | Studies | Of which: budget tier |
|---|---|---|
| Budget-matched | {{evaudit.final.budget_matched}} | shared cap {{evaudit.tier.cap_filled}}; measured equal {{evaudit.tier.measured_equal}}; structured arm smaller {{evaudit.tier.structured_smaller}} |
| Unmatched | {{evaudit.final.unmatched_single}} | |
| Multi-change | {{evaudit.final.multi_change}} | |
| No comparator | {{evaudit.final.no_comparator}} | |

*Most matched comparisons do not test structure.* Many compare two flat retrievers, two compressors, or two pruning models at the same budget. Only {{evaudit.svf.n}} set structured context (graph, AST, CPG, or repository map) against flat context at a matched budget; {{evaudit.svf_graph_primary}} of these come from studies whose primary class is graph-based, so the earlier reading that graph classes contain no matched test does not hold.

*What the {{evaudit.svf.n}} show.* Structure is better in {{evaudit.svf.structure_better}}: GraphCoder's context graph beats similarity retrieval at near-equal measured tokens (e.g., API-level EM 48.75 vs 35.80 with CodeGen2-16B) [@liu2024graphcoder]; HCP's dependency-pruned prompt beats a full random-context window with far fewer tokens [@zhang2024hcp]; RepoScope, ReCUBE, monitor-guided type context [@agrawal2023mgd], and import-ordered context in Long Code Arena (on perplexity, by small margins) point the same way. Flat context is better in {{evaudit.svf.flat_better}}: REPOFUSE's dependency-only context loses to similarity-retrieved context at the same cap, though combining the two wins [@liang2024repofuse], and MHRC-Bench's graph retriever loses on every hardware language at a fixed window [@zou2026mhrcbench]. {{evaudit.svf.no_difference}} show no clear difference, including R2C2-Coder [@deng2024r2c2coder] and SeeRepo, which matches flat accuracy with 25% fewer tokens.

*How to read this.* The controlled evidence is too small, too heterogeneous (completion, repair, QA; EM, pass@1, perplexity), and too dependent on single papers to support either "structure beats flat retrieval" or its negation. The {{evaudit.final.unmatched_single}} unmatched comparisons, where structure is usually *added* to the context, cannot separate structure from quantity and should not be read as evidence that structure is superior. Absence of controlled evidence in a cell is not evidence that structure fails there.

*A hypothesis, not a result.* Several matched wins come from structure that *selects* what fills a budget (HCP, GraphCoder) rather than adding to it. We therefore state as a testable hypothesis, not a finding, that structure acts as a relevance prior: it helps by choosing which tokens fill a fixed budget. No study in the corpus tests this directly.

## V. Implications and Recommended Practice

**For builders.** Treat structure as one way to choose what fills a budget, and compare it against strong flat retrieval at the same budget before paying its cost. The controlled evidence favours structure that selects (dependency-pruned or graph-guided context) and shows that composition can beat either source alone (REPOFUSE), but it is not consistent enough to recommend structure by default.

**Recommended evaluation practice.** For studies of repository-level context, we recommend:

1. *Report realised context per arm*, in tokens, not only the cap or the nominal target.
2. *Hold the budget fixed when varying the representation*: one model, one benchmark, one token budget, several representations.
3. *Include strong flat baselines* at that budget: a dense or BM25 retriever and a random-context control, not only "no context".
4. *Change one factor per comparison*; when an agent's number of calls or turns changes, report it as a separate factor.
5. *Report the trade-off curve*: quality at two or more budgets, so readers can see whether the gain is selection or quantity.
6. *Report variance*: several runs or seeds, since many differences in the corpus are a few points from one run.
7. *Release the context-construction code and the prompts*, so the budget accounting can be checked.

**For benchmark designers.** Budget-normalised metrics (Agent Retrieval Bench's yield at a fixed budget [@qin2026agent]) and matched-budget harnesses make practice 2 cheap; 18 of the 20 systems we checked for public code (a purposive selection; Section VI) release it, so the missing matched comparison could be run from existing artifacts.

## VI. Threats to Validity

We use Petersen's four categories [@petersen2015guidelines].

**Descriptive validity.** Every extracted number was re-checked at source ({{verification.wrong}} of {{verification.claims}} corrected). Extraction used selected full-text passages; the evidence audit, which carries RQ4, re-read the full text of every audited study, and it changed many evaluation codes (Section IV). The descriptive facets of the remaining studies may carry residual errors of the kinds verification found.

**Theoretical validity.** (i) *Coverage.* We measured three sources of loss. The cap removed {{funnel.cap_removed}} records, neither eligible. The keyword pre-filter removed {{funnel.prefilter_removed}}; screening all of them on title and abstract found {{prefilter_check.include}} likely eligible and {{prefilter_check.uncertain}} uncertain, mostly cross-file completion papers that say "retrieval" or "cross-file" rather than "context". A bounded reference-list check over {{snowball.papers}} studies ({{snowball.refs}} references) found {{snowball.include}} more likely eligible and {{snowball.uncertain}} uncertain. Against {{N}} included studies, the corpus is a substantial but incomplete sample, weakest on retrieval-for-completion work. We did not add these studies, because neither check is a systematic search; they are listed in the replication package. (ii) *Classification.* Representation agreement was moderate (κ = {{kappa_coding.repr_primary.kappa}}), concentrated on the hybrid boundary, so class-level counts should be read as approximate; RQ4 rests instead on the audit, which uses its own explicit definitions.

**Interpretive validity.** (i) *LLM coding.* All coding was done by LLM agents. The facet κ compares two runs of the same model family, so it shows stability across runs, not human agreement; shared biases would not appear in it. Only the evidence audit used a second family (GPT). No blind human coding was done, so human-versus-agent agreement is unknown. (ii) *Absence of evidence.* A missing comparison in this corpus is not evidence that structure does not help; it only means the claim has not been tested there. (iii) *Heterogeneity.* Tasks, benchmarks, and metrics differ, so results are reported by direction and range, never pooled. (iv) *Artifact survey.* The 20 systems checked for public code were chosen purposively during the original study (headline systems plus diversity); "18/20" describes that selection, not the corpus. (v) *Preprints.* Only {{peer_reviewed.true}} of {{N}} studies are peer-reviewed; the map describes a young, mostly unreviewed literature.

**Repeatability.** Searches are scripted with logged strings and hit counts; seeds are fixed; all decisions, corrections, and audit records are released; every corpus count and statistic is generated from the released data. Values quoted from individual studies are taken from the audit records (Supplementary Table S2).

## VII. Conclusion

Repository-context engineering is large, fast-moving, and mostly unreviewed. Its central comparative claim, that structured context beats flat retrieval, has been tested under a matched budget by {{evaudit.svf.n}} of {{N}} studies, with mixed results that lean towards structure. Most reported gains change the amount of context or several factors at once. The question is open rather than settled either way, and the recommended practices in Section V would close it.

## Declaration on the Use of AI {-}

LLM agents (Claude, Anthropic; and GPT, OpenAI, for the second audit check) carried out the scripted search, screening, full-text extraction, number verification, blind second coding, coverage checks, and evidence audit described in Section II, under written instructions from the authors. AI assistance was also used in drafting the manuscript. The authors wrote every boundary rule and made all analytical decisions; disagreements in the evidence audit were decided by an author checking an assistant-proposed verdict. The authors take full responsibility for the content, data, and conclusions.

## Appendix A — Complete corpus

{{table:corpus}}

## Appendix B — Evidence audit, study by study

{{table:audit}}
