# Seeing the Forest: A Systematic Mapping of Structure-Aware Context Engineering for Repository-Level Code LLMs and Agents

<!-- SOURCE OF report.md. Edit this file, never report.md: every corpus count is a double-brace placeholder
filled by render_report.py from stage5_map/_map_stats.json. -->

## Abstract

Code LLMs and coding agents see a repository only through the context they are given, and a large design space now builds that context from syntax trees, call and dependency graphs, repository maps, retrieved snippets, and compression. A common claim is that structured context beats flat retrieval, but structured context often also changes how much the model sees. We map {{N}} studies (2023–2026) by what the context is made of, how it is selected, and how gains are tested, and two independent checkers re-read the full text of the {{evaudit.n}} studies that report a comparison to see whether the context budget was held fixed. Both checkers agree that {{evaudit.strict.matched}} do; a more lenient rule, which also accepts a shared token cap, gives {{evaudit.final.budget_matched}}. Few of these compare structured against flat context: {{evaudit.strict.svf}} under the strict reading ({{evaudit.strict.structure_better}} favour structure, {{evaudit.strict.flat_better}} flat, {{evaudit.strict.no_difference}} neither) and {{evaudit.svf.n}} under the lenient one ({{evaudit.svf.structure_better}}, {{evaudit.svf.flat_better}}, {{evaudit.svf.no_difference}}). The other comparisons change the amount of context or several things at once. Structure may help, but the controlled evidence is thin and mixed, not absent. We close with evaluation practices that would settle the question.

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
| Hybrids, retrieved snippets, and call/dependency graphs lead the design space; agents increasingly select context themselves (RQ1–2) | Descriptive | Representation κ is moderate | Taxonomies of this field should state their hybrid rule |
| Budgets are reported far more often than controlled (RQ3) | Descriptive | Trade-off papers optimise the trade-off | Report realised tokens per arm |
| {{evaudit.strict.svf}}–{{evaudit.svf.n}} matched structured-vs-flat comparisons (strict–lenient reading), with mixed outcomes (RQ4) | Controlled, but few and heterogeneous | Under the lenient reading, {{evaudit.svf_cap_only}} of the {{evaudit.svf.n}} only share a token cap | "Structure beats flat retrieval" is neither established nor refuted |
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
| Raw window | contiguous text, not selected by retrieval (e.g., the current file, or tool outputs an agent reads) | LaMR's pruned file reads [@wang2026lamr] |
| Embedding retrieval | snippets selected by lexical or dense similarity (rule R1) | RepoCoder's iterative retrieval [@zhang2023repocoder] |
| Call/dependency graph | code selected or ordered by call, import, or type edges | HCP's dependency-pruned prompt [@zhang2024hcp] |
| AST | code or facts derived from the syntax tree | Monitor-guided decoding [@agrawal2023mgd] |
| CPG/dataflow | code selected by data- or control-flow relations | DraCo's dataflow-guided retrieval [@cheng2024draco] |
| Repository map/skeleton | a compressed whole-repository view (signatures, structure) | Agent Retrieval Bench's RepoMap arm [@qin2026agent] |
| Execution traces | runtime or agent-trajectory content | Observation masking of agent histories [@lindenbauer2025lindenbauer2] |
| Hybrid | two or more of the above as *co-equal* parts of the contribution | REPOFUSE's analogy plus dependency context [@liang2024repofuse] |

*The hybrid boundary.* A study is hybrid only when its contribution is the combination; if one family carries the contribution and another is incidental, the study takes that family's class. Most coding disagreements were exactly this judgement: of the {{kappa_coding.repr_disagreements}} representation disagreements in the blind re-coding, {{kappa_coding.repr_disagreements_hybrid}} involve the hybrid class. Adjudication kept the extractor's code in {{kappa_coding.repr_primary.final_first}}, the second coder's in {{kappa_coding.repr_primary.final_second}}, and a third code in {{kappa_coding.repr_primary.final_other}}; for mechanism the figures are {{kappa_coding.mechanism.final_first}}, {{kappa_coding.mechanism.final_second}}, and {{kappa_coding.mechanism.final_other}}. The typical case is a system combining two families: the second coder called it hybrid, and adjudication kept the family the paper's contribution is about. Atypical cases went to a third code, e.g., Kovrigin24, whose agent searches the AST with no call graph (extractor: call graph; second coder: hybrid; adjudication: AST).

### Extraction, verification, reliability, and adjudication

LLM agents (Claude, Anthropic) extracted each study from its full text under a written codebook. A separate agent re-checked every extracted number at source: {{verification.claims}} claims, {{verification.confirmed}} confirmed ({{verification.pct_confirmed}}%), {{verification.wrong}} wrong and corrected. A second agent of the same model family re-coded all {{kappa_coding.n}} studies blind. Before adjudication, κ was {{kappa_coding.mechanism.kappa}} for mechanism, {{kappa_coding.evaluation.kappa}} for evaluation, and {{kappa_coding.repr_primary.kappa}} for representation.

*How disagreements were resolved.* Flagged disagreements were decided by an author against the full text, and the decisions with written rationale are in the released correction log; unflagged facet disagreements kept the extractor's full-text code unless a verifier objected. For representation, a disagreement was decided by the boundary rule above; for evaluation, by the definitions in Table IV. The taxonomy was refined once: rule R1 (retrieved snippets code as embedding retrieval, whatever the retriever) was added when two verifiers flagged retrieval records in opposite directions. In this revision we found five studies still coded raw window although their context is retrieved, and recoded them under R1. No class was added or removed after the second coding. The evaluation κ refers to the original evaluation codes, which the audit below replaced.

*Evidence audit (amendment A2).* RQ4 depends on whether each comparison holds the context budget fixed, so in this revision we re-read the full text of all {{evaudit.n}} studies coded as reporting a comparison and assigned one of the levels in Table IV. Two checkers worked independently on the same pinned texts: Claude agents, and GPT (OpenAI) given only the paper text and a *strict* rule (the realised budget must be shown equal; unreported usage does not count). Each recorded the model and configuration, dataset and metric, budget control, what each arm shows, and anything else that changed (Supplementary Table S2). When a paper contains several comparisons, each checker judged the one most favourable to a matched budget.

Table: Evaluation levels for RQ4. "Matched" requires the same model and configuration on the same dataset and metric.

| Level | Definition |
|---|---|
| Budget-matched (lenient) | Only the representation or selection mechanism differs, and the budget is held: both arms share the same hard cap (usage unreported), per-arm usage is reported equal, or the structured arm is reported to use no more (tokens, or dollar cost where that is all that is reported) |
| Budget-matched (strict) | As above, and both independent checkers judged the realised budget held |
| Unmatched | Only the representation or mechanism differs, but the amount of context differs or is not controlled |
| Multi-change | The model, agent scaffold, number of model calls, training, or several components also differ |
| No comparator | No quantitative comparison with an alternative |

The checkers agreed on {{evaudit.agree}} of {{evaudit.n}} studies (κ = {{evaudit.kappa}}). Most disagreements turned on one question: does a shared cap, or a structured arm that measurably used less, count as matched? The strict rule says no; Table IV's lenient rule, fixed after the checkers ran, says yes. We therefore report both readings throughout. The *strict* reading counts only studies both checkers called matched ({{evaudit.strict.matched}}; GPT alone found {{evaudit.strict.matched_B}}). The *lenient* reading applies Table IV, using a third full-text pass that recorded each candidate's budget tier ({{evaudit.decided_by_rule}} disagreements resolved this way); the remaining {{evaudit.decided_by_authors}} were decided by an author checking an assistant-proposed verdict, which was accepted in every case. The same pass recorded whether each matched comparison sets structured against flat context; where a paper had such a comparison, it was used even if the checkers had judged another, and these switches are marked in Table S2. The audit replaced the original evaluation codes, which had used a strict rule: of the {{evaudit.was_budget_matched}} studies first coded budget-matched, {{evaudit.kept_budget_matched}} remain so under the lenient reading.

### Synthesis

Synthesis is descriptive: frequency counts and cross-tabulations, plus narrative synthesis per cell. Following Petersen, studies are not quality-scored; the evaluation facet records the strength of each comparison instead. Tasks, benchmarks, and metrics differ too much to pool effect sizes, so none are pooled.

### Data availability

The protocol, search strings and hit counts, all screening and adjudication decisions, the extraction database, verification and audit records, and the scripts are released at https://anonymous.4open.science/r/context-forest-replication-2BC9/ (anonymised for review). The release regenerates every corpus count and statistic in this paper.

## III. The Map (RQ1–RQ3)

**RQ1: hybrids, retrieved snippets, and graphs lead.** Hybrids are the largest primary class ({{repr_primary.hybrid}}), followed by embedding retrieval ({{repr_primary.embedding_retrieval}}), call/dependency graphs ({{repr_primary.call_dep_graph}}), raw windows ({{repr_primary.raw_window}}), repository maps ({{repr_primary.repo_map_skeleton}}), ASTs ({{repr_primary.ast}}), CPG/dataflow ({{repr_primary.cpg_dataflow}}), and execution traces ({{repr_primary.exec_traces}}). Graph-structured classes (call/dependency graph, AST, CPG) together hold {{n_graph_class}} studies.

**RQ2: retrieval-time selection and in-loop agents dominate.** By mechanism, similarity retrieval ({{mechanism.similarity_retrieval}}), graph-guided retrieval ({{mechanism.graph_guided_retrieval}}), and agentic exploration ({{mechanism.agentic_exploration}}) lead; pruning ({{mechanism.learned_pruning}}), slicing ({{mechanism.slicing_static_analysis}}), skeletonisation ({{mechanism.skeletonization}}), compression ({{mechanism.learned_compression}}), and summarisation ({{mechanism.summarization}}) are smaller. By pipeline position, context is built at retrieval time in {{pipeline_position.retrieval_time}} studies, inside an agent loop in {{pipeline_position.in_loop}}, and at prompt assembly in {{pipeline_position.prompt_assembly}}; offline indexing is rarely the contribution ({{pipeline_position.offline_index}}), and {{mechanism.none_fixed_window}} use a fixed window. Agentic exploration moves the budget question rather than answering it: an agent's context is assembled by its trajectory, so its size varies per task and is hard to compare across systems.

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

**Answer: controlled comparisons exist, but few test structure against flat context, and they disagree.** We audited {{evaudit.n}} studies; {{evaudit.compared}} have a comparison. Under the lenient reading, {{evaudit.final.budget_matched}} hold the budget fixed, {{evaudit.final.unmatched_single}} vary the representation without controlling the amount of context, and {{evaudit.final.multi_change}} change several factors; the other {{evaudit.final.no_comparator}} turned out to have no comparison (Table VI). Under the strict reading, {{evaudit.strict.matched}} hold the budget fixed.

Table: Outcome of the evidence audit ({{evaudit.n}} studies audited).

| Level | Studies | Of which: budget tier |
|---|---|---|
| Budget-matched, lenient | {{evaudit.final.budget_matched}} | shared cap {{evaudit.tier.cap_filled}}; measured equal {{evaudit.tier.measured_equal}}; structured arm smaller {{evaudit.tier.structured_smaller}} |
| Budget-matched, strict | {{evaudit.strict.matched}} | both checkers agree |
| Structured vs flat, strict / lenient | {{evaudit.strict.svf}} / {{evaudit.svf.n}} | outcomes {{evaudit.strict.structure_better}}–{{evaudit.strict.flat_better}}–{{evaudit.strict.no_difference}} / {{evaudit.svf.structure_better}}–{{evaudit.svf.flat_better}}–{{evaudit.svf.no_difference}} (structure–flat–neither) |
| Unmatched | {{evaudit.final.unmatched_single}} | |
| Multi-change | {{evaudit.final.multi_change}} | |
| No comparator | {{evaudit.final.no_comparator}} | |

*Most matched comparisons do not test structure.* Many compare two flat retrievers, two compressors, or two pruning models at the same budget. Only {{evaudit.strict.svf}} (strict) to {{evaudit.svf.n}} (lenient) set structured context (graph, AST, CPG, or repository map) against flat context at a matched budget. Under the lenient reading, {{evaudit.svf_graph_primary}} of these come from studies whose primary representation is a graph, AST, or CPG. The first version of this paper, which coded evaluation with the strict rule only, reported none in those classes; amendment A2 records the change.

*What they show.* Under the strict reading, structure is better in {{evaudit.strict.structure_better}} (HCP's dependency-pruned prompt against a random-context window with far fewer tokens [@zhang2024hcp]; type context in MGD's prompts [@agrawal2023mgd]; RepoScope [@liu2025reposcope], though it changes several components), flat context in {{evaudit.strict.flat_better}} (MHRC-Bench, whose graph retriever, ported to hardware languages by the benchmark authors, loses on every language [@zou2026mhrcbench]), and {{evaudit.strict.no_difference}} show no clear difference (Agent Retrieval Bench [@qin2026agent]; SeeRepo [@ma2026seerepo], which matches flat accuracy with 25% fewer tokens for one of four models). The lenient reading adds GraphCoder (better at near-equal tokens, e.g., API-level EM 48.75 vs 35.80 with CodeGen2-16B [@liu2024graphcoder]), ReCUBE [@hong2026recube] and Long Code Arena [@bogomolov2024longcodearen] (better, by a dollar budget and by small perplexity margins), REPOFUSE (dependency-only context loses to similarity retrieval at the same cap, though combining them wins [@liang2024repofuse]), and R2C2-Coder [@deng2024r2c2coder] and Stingy Context [@ostby2026stingy] (no clear difference). Several of these carry caveats recorded in Table S2: changes in the number of agent turns, added tools or instructions (SeeRepo, ReCUBE), a multi-component system (RepoScope), and caps whose fill is not reported.

*How to read this.* The controlled evidence is too small, too heterogeneous (completion, repair, QA; EM, pass@1, perplexity), and too dependent on single papers to support either "structure beats flat retrieval" or its negation. The {{evaudit.final.unmatched_single}} unmatched comparisons, where structure is usually *added* to the context, cannot separate structure from quantity and should not be read as evidence that structure is superior. Absence of controlled evidence in a cell is not evidence that structure fails there.

*A hypothesis, not a result.* Some matched wins come from structure that *selects* what fills a budget (HCP, GraphCoder) rather than adding to it, but both flat-better results are also graph or dependency selection. We therefore state as a testable hypothesis, not a finding, that structure acts as a relevance prior: it helps by choosing which tokens fill a fixed budget. No study in the corpus tests this directly.

## V. Implications and Recommended Practice

**For builders.** Treat structure as one way to choose what fills a budget, and compare it against strong flat retrieval at the same budget before paying its cost. The controlled evidence is mixed, including for graph-guided selection, and one study shows that combining structured and retrieved context can beat either alone (REPOFUSE); it is not consistent enough to recommend structure by default.

**Recommended evaluation practice.** For studies of repository-level context, we recommend:

1. *Report realised context per arm*, in tokens, not only the cap or the nominal target.
2. *Hold the budget fixed when varying the representation*: one model, one benchmark, one token budget, several representations.
3. *Include strong flat baselines* at that budget: a dense or BM25 retriever and a random-context control, not only "no context".
4. *Change one factor per comparison*; when an agent's number of calls or turns changes, report it as a separate factor.
5. *Report the trade-off curve*: quality at two or more budgets, so readers can see whether the gain is selection or quantity.
6. *Report variance*: several runs or seeds, since many differences in the corpus are a few points from one run.
7. *Release the context-construction code and the prompts*, so the budget accounting can be checked.

**For benchmark designers.** Budget-normalised metrics (Agent Retrieval Bench's yield at a fixed budget [@qin2026agent]) and matched-budget harnesses make practice 2 cheap; Of 20 systems we checked for public code, chosen purposively (Section VI), 18 release some, so some matched comparisons could be rerun.

## VI. Threats to Validity

We use Petersen's four categories [@petersen2015guidelines].

**Descriptive validity.** Every extracted number was re-checked at source ({{verification.wrong}} of {{verification.claims}} corrected). Extraction used selected full-text passages; the evidence audit, which carries RQ4, re-read the full text of every audited study, and it changed many evaluation codes (Section IV). The descriptive facets of the remaining studies may carry residual errors of the kinds verification found.

**Theoretical validity.** (i) *Coverage.* We measured three sources of loss. The cap removed {{funnel.cap_removed}} records, neither eligible. The keyword pre-filter removed {{funnel.prefilter_removed}}; screening all of them on title and abstract found {{prefilter_check.include}} likely eligible and {{prefilter_check.uncertain}} uncertain: retrieval-for-completion papers (RLCoder, the flat arm in one RQ4 comparison, among them), agentic issue-resolution systems, and several explicitly structural ones (AST chunking, repository graphs). A bounded reference-list check, using this study's own keyword conjunction on the titles of references from the {{snowball.papers}} budget-matched and graph-class studies ({{snowball.refs}} references), found {{snowball.include}} more likely eligible and {{snowball.uncertain}} uncertain, none overlapping the pre-filter's misses. Together that is {{coverage.missed_likely}} likely-eligible studies the corpus lacks, so recall is at most about {{N}} of {{coverage.recall_denominator}} ({{coverage.recall_pct}}%). The misses include structural, graph-based systems (e.g., CodexGraph, LocAgent, CoSIL), so RQ1 counts and RQ4's matched set could shift; every finding in this paper describes the searched corpus. We did not add these studies, because neither check is a systematic search; they are listed in the replication package. (ii) *Classification.* Representation agreement was moderate (κ = {{kappa_coding.repr_primary.kappa}}), concentrated on the hybrid boundary, so class-level counts should be read as approximate; RQ4 rests instead on the audit, which uses its own explicit definitions.

**Interpretive validity.** (i) *LLM coding.* All coding was done by LLM agents. The facet κ compares two runs of the same model family, so it shows stability across runs, not human agreement; shared biases would not appear in it. Only the evidence audit used a second family (GPT). No blind human coding was done, so human-versus-agent agreement is unknown. (ii) *Absence of evidence.* A missing comparison in this corpus is not evidence that structure does not help; it only means the claim has not been tested there. (iii) *Heterogeneity.* Tasks, benchmarks, and metrics differ, so results are reported by direction and range, never pooled. (iv) *Artifact survey.* The 20 systems checked for public code were chosen purposively (headline systems plus diversity); "18/20" describes that selection, not the corpus, and two of the 18 are thin snapshots. (v) *Preprints.* Only {{peer_reviewed.true}} of {{N}} studies in this corpus are peer-reviewed; the arXiv-heavy search contributes to that share. (vi) *The audit's rules.* Table IV's lenient rule was fixed after the checkers ran, so we report the strict reading beside it; the author decisions accepted assistant-proposed verdicts, and no blind human judgement of the audit was made.

**Repeatability.** Searches are scripted with logged strings and hit counts; seeds are fixed; all decisions, corrections, and audit records are released; every corpus count and statistic is generated from the released data. Values quoted from individual studies are taken from the audit records (Supplementary Table S2).

## VII. Conclusion

Repository-context engineering is large and fast-moving, and in this corpus mostly unreviewed. Its central comparative claim, that structured context beats flat retrieval, has been tested under a matched budget by {{evaudit.strict.svf}} to {{evaudit.svf.n}} of {{N}} studies, depending on how strictly a matched budget is read, with mixed results. Most reported gains change the amount of context or several factors at once. The question is open rather than settled either way, and the recommended practices in Section V would close it.

## Declaration on the Use of AI {-}

LLM agents (Claude, Anthropic; and GPT, OpenAI, for the second audit check) carried out the scripted search, screening, full-text extraction, number verification, blind second coding, coverage checks, and evidence audit described in Section II, under written instructions from the authors. AI assistance was also used in drafting the manuscript. The authors wrote every boundary rule and made all analytical decisions; disagreements in the evidence audit were decided by an author checking an assistant-proposed verdict. The authors take full responsibility for the content, data, and conclusions.

## Appendix A — Complete corpus

{{table:corpus}}

## Appendix B — Evidence audit, study by study

{{table:audit}}
