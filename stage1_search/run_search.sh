#!/usr/bin/env bash
# Study 5 stage 1: database search (arXiv + OpenAlex). Strategy 1 of 3 (see 00_protocol.md §2).
set -u
# Helpers: github.com/lingzhi227/agent-research-skills @ 9e6c085 (not redistributed). Set ARS_DIR to a checkout.
DR="${ARS_DIR:?set ARS_DIR to a checkout of agent-research-skills}/skills/deep-research/scripts"
LS="$ARS_DIR/skills/literature-search/scripts"
R="$(cd "$(dirname "$0")" && pwd)/results"
mkdir -p "$R"
ax() { python3 "$DR/search_arxiv.py" --query "$1" --max-results "${3:-40}" --sort-by relevance --start-date 2023-01-01 -o "$R/$2" 2>&1 | tail -1; sleep 3; }
oa() { python3 "$LS/search_openalex.py" --query "$1" --max-results "${3:-40}" --year-range 2023-2026 --output "$R/$2" 2>&1 | tail -1; sleep 1; }

ax "repository-level code completion context LLM" ax_repocomp.jsonl
ax "repository level code generation context retrieval" ax_repogen.jsonl
ax "abstract syntax tree LLM code context prompt" ax_ast.jsonl
ax "call graph dependency context code large language model" ax_callgraph.jsonl
ax "repo map skeleton code agent context" ax_repomap.jsonl
ax "context compression coding agent LLM" ax_ctxcompress.jsonl
ax "code context pruning selection completion LLM" ax_prune.jsonl
ax "static analysis context code completion language model" ax_static.jsonl
ax "structure-aware code retrieval augmented generation" ax_structrag.jsonl
ax "code property graph retrieval LLM generation" ax_cpg.jsonl
ax "cross-file context code completion benchmark" ax_crossfile.jsonl
ax "context window budget tokens coding agent" ax_budget.jsonl
ax "repository knowledge graph code generation LLM" ax_kg.jsonl
ax "agent codebase exploration navigation context" ax_explore.jsonl
ax "prompt construction repository code LLM cross-file" ax_promptcon.jsonl
ax "issue resolution context localization repository agent" ax_issue.jsonl

oa "repository-level context code large language model" oa_repo.jsonl
oa "abstract syntax tree context large language model code" oa_ast.jsonl
oa "context compression code generation LLM" oa_compress.jsonl
oa "cross-file code completion context retrieval" oa_crossfile.jsonl
echo "Study 5 database search done: $(ls "$R" | wc -l) result files"
