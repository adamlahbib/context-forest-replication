#!/usr/bin/env bash
# known-item / snowball-seed queries (strategy 2 of 3) + quasi-gold-standard
# retrieval, incl. borderline cases and negative controls (00_protocol.md §2).
set -u
# Helpers: github.com/lingzhi227/agent-research-skills @ 9e6c085 (not redistributed). Set ARS_DIR to a checkout.
DR="${ARS_DIR:?set ARS_DIR to a checkout of agent-research-skills}/skills/deep-research/scripts"
R="$(cd "$(dirname "$0")" && pwd)/results"
mkdir -p "$R"
ki() { python3 "$DR/search_arxiv.py" --query "$1" --max-results 5 --sort-by relevance --start-date 2022-06-01 -o "$R/ki_$2" 2>&1 | tail -1; sleep 3; }

ki "RepoCoder repository-level code completion iterative retrieval" repocoder.jsonl
ki "GraphCoder repository code completion code context graph" graphcoder.jsonl
ki "STALL boosting LLM repository code completion static analysis" stall.jsonl
ki "CodePlan repository-level coding planning LLM" codeplan.jsonl
ki "RepoFusion training code models to understand your repository" repofusion.jsonl
ki "monitor-guided decoding code language models static analysis" mgd.jsonl
ki "hierarchical context pruning repository code completion" hcp.jsonl
ki "aiXcoder long context repository code completion training" aixcoder.jsonl
ki "SWE-Pruner self-adaptive context pruning coding agents" swepruner.jsonl
ki "ACON optimizing context compression long-horizon agents" acon.jsonl
ki "RepoBench benchmarking repository-level code auto-completion" repobench.jsonl
ki "CrossCodeEval cross-file code completion benchmark" crosscodeeval.jsonl
ki "A3-CodGen repository-level code generation local global third-party" a3codgen.jsonl
# negative controls (expected exclusions if retrieved):
ki "in-context autoencoder context compression large language model" nc_icae.jsonl
ki "LongCoder long-range pre-trained language model code completion" nc_longcoder.jsonl
echo "known-item search done"
