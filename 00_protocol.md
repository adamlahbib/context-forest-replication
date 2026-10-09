# Review Protocol — Systematic Mapping Study (Study 5)

**Working title:** *Seeing the Forest: A Systematic Mapping of Structure-Aware Context Engineering for
Repository-Level Code LLMs and Agents.*

**Document type:** Technical report (systematic mapping study), Petersen et al. (2008; 2015) + Kitchenham
& Charters (2007). **Not** peer-reviewed. **Authorship:** `[REDACTED]` (double-blind).
**Search/compile cutoff:** 2026-08-30. **Eligible window:** 2023-01-01 – 2026-08-30.
**Protocol fixed before retrieval**; amendments will be logged with timestamps.

## 1. Motivation, research questions, target audience

A code LLM or coding agent sees a repository only through the context it is handed, and repositories do
not fit in context windows. A design space has grown around *constructing* that context — abstract syntax
trees, call/dependency graphs, code property graphs, repo maps and skeletons, static-analysis slices,
embedding retrieval — and around *compressing* it (pruning, summarization, learned compression) to a token
budget. No systematic review maps this space: which structural representations feed contexts, which
selection/compression mechanisms are used where, what token-budget↔task-success trade-offs are actually
measured, and whether "structure beats flat retrieval" claims are supported by budget-matched comparisons
or confounded by giving the structured condition more or different context. (This study maps the
*engineering* of the loop's perceive/context stage, whose attack surface program Study 3 mapped.)

- **RQ1 (Representations).** What structural representations of a repository are used to construct LLM
  context — raw text windows, AST, call/dependency graph, code property graph, repo map/skeleton,
  embedding retrieval, hybrids?
- **RQ2 (Mechanisms).** What selection/compression mechanisms operate on them — static-analysis slicing,
  graph-guided retrieval, learned pruning/compression, summarization, skeletonization — and at which
  pipeline position (offline index, retrieval time, prompt assembly, in-loop)?
- **RQ3 (Trade-offs).** Where measured, what token-budget-versus-task-success trade-offs are reported,
  on which tasks and benchmarks?
- **RQ4 (Evidence integrity).** When the token budget is held constant, does structural context
  demonstrably beat unstructured retrieval — i.e., which comparisons are budget-matched,
  representation-only ablations, and which confound representation with context amount or retriever?

**Target audience:** builders of coding agents and code-assist systems deciding how to spend a context
budget on a repository; benchmark designers, for whom the unmeasured cells (budget-matched ablations,
cross-task comparability) locate missing evaluation conventions.

## 2. Sources & search — three strategies

1. **Database search:** arXiv API (≥3 s throttle) + OpenAlex, scripted (`stage1_search/run_search.sh`,
   full strings + per-query hit counts in `search_log.md`). Justified as in Studies 1–4: the field is
   preprint-dominated; Semantic Scholar unavailable (no API key). The 2-database ceiling is a disclosed
   limitation (DARE QC2), mitigated by strategies 2–3.
2. **Snowballing:** known-item seed queries now (`run_known_items.sh`); after screening, one backward
   +forward snowballing pass over included records' reference lists and citers (logged per record).
3. **Manual venue checks:** ICSE/FSE/ASE, ICLR/NeurIPS/ICML, ACL/EMNLP proceedings checked for
   repository-context work the indices miss (logged in `search_log.md`).

**Search evaluation (quasi-gold standard with borderline + negative controls).** Recall is tested against
a pre-declared test set that includes *borderline* cases and *expected-exclusion* negative controls — not
only canonical papers (a test the instrument cannot fail measures nothing): RepoCoder; GraphCoder; STALL+;
CodePlan; RepoFusion; Monitor-Guided Decoding; Hierarchical Context Pruning; aiXcoder-7B-v2; SWE-Pruner;
ACON; *borderline:* RepoBench and CrossCodeEval (benchmarks — in scope only as context-utilization
measurements), A3-CodGen; *negative controls (must be excluded if retrieved):* In-context Autoencoder
(general-text compression, E2), LongCoder/position-interpolation work (model-internal long context, E1).
Recall and control outcomes reported in `search_log.md`.

**Caps (declared before any draw).** If pre-filter candidates exceed **200**, screening uses a seeded
random sample of 200 (`seed=20260830`), reported as sampling in PRISMA. No cap below that.

## 3. Inclusion / exclusion

**Include** iff: **I1** the record concerns an LLM-based code task (completion, generation, editing/issue
resolution, code QA/reasoning, translation, review, repair) at repository/cross-file scope, OR context
construction/compression for code LLMs or coding agents at any scope; **I2** it proposes, implements,
measures, or benchmarks a **context-construction, selection, compression, or structural-representation
mechanism** that shapes what enters the model's context (or empirically studies context utilization);
**I3** enough detail to code the facets; **I4** 2023–2026, English, retrievable.
**Exclude:** **E1** model-internal long-context work only (position encodings, attention/KV-cache
architecture) with no context-construction mechanism; **E2** general-text RAG/compression with no
code/repository instantiation; **E3** structural code representation for non-LLM models only (GNN
classifiers etc.) with no LLM-context use; **E4** function-level prompting with no cross-file/structural/
budget concern; **E5** duplicate/superseded; **E6** not retrievable.

**Record** = publication/study unit. Dedup key = normalized title (never title+year; preprint/venue pairs
collapse), then title-Jaccard ≥ 0.8, collisions human-glanced.

## 4. Screening — with a reliability action on inclusion/exclusion

Identification → title-only dedup → automated pre-filter (code∧context∧LLM signal conjunction; audited
against the gold set for false negatives) → LLM screening against I1–I4/E1–E6 in disjoint batches →
author adjudication of all uncertains + logged overrides. **Reliability action:** a seeded
(`seed=20260830`) **20% sample of screened candidates is independently double-screened** by a second,
blind LLM screener; include/exclude agreement and Cohen's κ are reported, disagreements author-adjudicated
under a written rule (default to full-text check). This closes the no-screening-κ gap of program Studies 1–4.

## 5. Classification scheme

- **F1 Representation (multiple; primary flagged):** raw-window · AST · call/dependency graph ·
  code-property-graph/dataflow · repo-map/skeleton-signature · embedding-retrieval · execution/runtime
  traces · hybrid.
- **F2 Mechanism:** static-analysis slicing · graph-guided retrieval · similarity retrieval · learned
  pruning/selection · learned compression (soft/latent) · summarization · skeletonization · agentic
  exploration (model navigates) · none (fixed window).
- **F3 Pipeline position:** offline index · retrieval-time · prompt-assembly · in-loop/iterative.
- **F4 Task:** completion · generation · editing/issue-resolution · QA/reasoning · translation · review ·
  repair · general/mixed.
- **F5 Evaluation:** budget-matched representation ablation · ablated/measured vs baseline (not
  budget-matched) · demonstrated (no comparator) · not evaluated; plus benchmark(s) used and whether a
  token/cost budget is *reported* at all.
- **F6 Research type (Wieringa):** validation (lab) · evaluation (practice) · solution proposal ·
  philosophical · opinion · experience. **F7 record type:** system/tool · benchmark/eval · empirical
  study · survey · position.

## 6. Extraction schema (per record)

`system, citation_key, year, venue, peer_reviewed, F1(primary flagged), F2, F3, F4, F5(+benchmark,
budget_reported), F6, F7, scope(function/file/cross-file/repo), key_numbers(1–3, tied to source+location),
budget_tradeoff_detail, confound_note(what varies between compared conditions), stop_detail(mechanism as
the paper states it), threats_to_that_datum`. **Full-corpus independent number verification** (every
extracted number re-checked at its in-source location) + **blind full-corpus second coding** of F1-primary,
F2, F5 with per-facet κ, as in Study 4.

## 7. Analysis & synthesis (named)

Synthesis is the standard mapping-study combination of **frequency-count synthesis over the facet map plus
structured narrative synthesis** of exemplars per cell (Petersen 2008), with a representation × evaluation
cross-tabulation as the central map and an RQ4 confound table (compared conditions and what varies).
Evidence-proportional; [EVIDENCE]/[SYNTHESIS]/[HYPOTHESIS] labels; all counts derived programmatically
from `extraction.json`.

**Quality assessment:** none, by design, per Petersen — a map charts what exists; excluding early-stage
proposals would delete the records that show where the field is heading. F5 captures evaluation rigor
descriptively. (Disclosed in the report.)

## 8. Threats to validity — Petersen's four categories by name

Organized as **descriptive** (extraction fidelity; mitigated by full-corpus verification), **theoretical**
(missed studies: 2-database ceiling, terminology bias, snowballing depth; misclassification: facet κ,
screening κ), **interpretive** (documenting-subset caveat — budget trade-offs are reported by papers built
to optimize them; conclusions scoped to corpus), **repeatability** (scripted search, logged decisions,
seeds, released pipeline).

## 9. Reporting

Main body ≤ 8 pages (IEEE, split build); Appendices (verification, κ, complete per-record corpus table) in
`supplementary.pdf`. AI-tooling disclosure as Studies 1–4 (scripted search; LLM screening/extraction,
author-adjudicated; independent verification; blind second coder; dual-screened sample with κ).

## 10. Stage map

0 protocol · 1 search_log (3 strategies + gold-set recall) · 2 prisma + corpus (+ dual-screen κ) ·
3 extraction + verification + second coding · 4 artifacts (code-release survey of corpus systems) ·
5 map + synthesis · 6 report + references + paper.pdf + supplementary.pdf.
