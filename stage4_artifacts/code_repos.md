# Stage 4 — Code Artifact Survey

**Survey date:** 2026-08-30

**Methodology:** For each of the 20 systems selected below, one targeted WebSearch was run (e.g. "`<system>` github repository code") to locate a public code repository. Where a repository URL surfaced, a single WebFetch of the repository's GitHub page was performed to record stars, license, and any visible activity signal. No repository surfacing after the single targeted search is recorded as **"no public artifact found (single-search check)"** — this is a lower bound on artifact availability, not an exhaustive absence claim (repos could exist under different names, in supplementary material, or behind non-indexed pages).

Selection: the 13 systems named in the task brief (RepoCoder, GraphCoder, STALL+, CodePlan, RepoFusion, Monitor-Guided Decoding, Hierarchical Context Pruning, aiXcoder-7B-v2, SWE-Pruner, LongCodeZip, SWE-Explore, RepoBench, CrossCodeEval) plus 7 additional prominent systems chosen from the corpus (`corpus.jsonl`, 83 records) for topical coverage of retrieval-augmented completion, static/graph-based context construction, and agentic issue resolution: Repoformer, DraCo, Alibaba LingmaAgent, CodeAgent, Long Code Arena, Prometheus, RepoHyper.

## 1. Surveyed systems

| System | arXiv ID | Repo | Stars | License | Activity signal |
|---|---|---|---|---|---|
| RepoCoder | 2303.12570 | [microsoft/CodeT/tree/main/RepoCoder](https://github.com/microsoft/CodeT/tree/main/RepoCoder) | 678 | MIT | 7 open issues, 3 open PRs (whole CodeT repo; appears actively watched) |
| RepoBench | 2306.03091 | [Leolty/repobench](https://github.com/Leolty/repobench) | 212 | CC-BY-4.0 | 117 commits; v1.1 data refresh Feb 2024 |
| Monitor-Guided Decoding (MGD) | 2306.10763 | [microsoft/monitors4codegen](https://github.com/microsoft/monitors4codegen) | 280 | MIT | 38 commits; ships reusable `multispy` LSP client library beyond the paper's scope |
| RepoFusion | 2306.10998 | [ServiceNow/RepoFusion](https://github.com/ServiceNow/RepoFusion) | 13 | License file present, type not shown on page | 1 commit — minimal/stub release |
| CodePlan | 2309.12499 | [microsoft/CodePlan](https://github.com/microsoft/CodePlan) | 89 | MIT | 11 commits; **repo archived by owner (2026-06-15), now read-only** |
| CrossCodeEval | 2310.11248 | [amazon-science/cceval](https://github.com/amazon-science/cceval) | 182 | Apache-2.0 | 29 commits |
| GraphCoder | 2406.07003 | [oceaneLIU/GraphCoder](https://github.com/oceaneLIU/GraphCoder) | 65 | Not shown on page | 33 commits |
| STALL+ | 2406.10018 | NONE FOUND | — | — | no public artifact found (single-search check) |
| Hierarchical Context Pruning (HCP) | 2406.18294 | [Hambaobao/HCP-Coder](https://github.com/Hambaobao/HCP-Coder) | 17 | MIT | 12 commits |
| aiXcoder-7B-v2 | 2503.15301 | [aixcoder-plugin/aixcoder-7b-v2](https://github.com/aixcoder-plugin/aixcoder-7b-v2) | 10 | Not shown on page | 2 commits — minimal/stub release (separate, larger `aiXcoder-7B` base-model repo exists under the same org) |
| SWE-Pruner | 2601.16746 | [Ayanami1314/swe-pruner](https://github.com/Ayanami1314/swe-pruner) | 314 | MIT | 54 commits; updates through Aug 2026 (training data + eval pipeline); ByteDance Research authorship confirmed in README |
| LongCodeZip | 2510.00446 | [YerbaPage/LongCodeZip](https://github.com/YerbaPage/LongCodeZip) | 166 | MIT | 31 commits; pip-installable |
| SWE-Explore | 2606.07297 | [Qiushao-E/SWE-Explore-Bench](https://github.com/Qiushao-E/SWE-Explore-Bench) | 42 | MIT | 7 commits; "paper, code, dataset released 2026-06-08" |
| Repoformer | 2403.10059 | [amazon-science/Repoformer](https://github.com/amazon-science/Repoformer) | 67 | Apache-2.0 | 18 commits |
| DraCo | 2405.19782 | [nju-websoft/DraCo](https://github.com/nju-websoft/DraCo) | 34 | GPL-3.0 | 4 commits |
| Alibaba LingmaAgent | 2406.01422 | [RepoUnderstander/RepoUnderstander](https://github.com/RepoUnderstander/RepoUnderstander) | 97 | Not shown on page | 13 commits; described in paper as an open-sourced "Python prototype" (production system is internal to Alibaba/TONGYI Lingma) |
| CodeAgent | 2401.07339 | NONE FOUND (official) | — | — | no public artifact found (single-search check); only an unofficial third-party replication surfaced (`PatrizioAcquadro/code-agent-replication`), not counted as a released artifact |
| Long Code Arena | 2406.11612 | [JetBrains-Research/lca-baselines](https://github.com/JetBrains-Research/lca-baselines) | 38 | MIT | 163 commits; paired with a maintained HuggingFace Spaces leaderboard |
| Prometheus | 2507.19942 | [EuniAI/Prometheus](https://github.com/EuniAI/Prometheus) | ~1,100 | GPLv3 (dual-licensed; commercial license also offered) | 1,083 commits; 7 open issues, 2 open PRs — most actively developed repo in this sample |
| RepoHyper | 2403.06095 | [FSoft-AI4Code/RepoHyper](https://github.com/FSoft-AI4Code/RepoHyper) | 75 | Apache-2.0 (README also references an MIT LICENSE file) | 11 commits |

## 2. No-artifact list

- **STALL+** (2406.10018) — no public artifact found (single-search check).
- **CodeAgent** (2401.07339) — no official public artifact found (single-search check); only an unofficial third-party replication repository was found, not an author-released artifact.

## 3. Observations

- **Benchmark/dataset papers release code near-universally; single-mechanism research prototypes are the ones that go missing.** All four benchmark-flavored artifacts surveyed (RepoBench, CrossCodeEval, Long Code Arena, SWE-Explore) have public repos with dataset + eval harness, since a benchmark is worthless without a shared artifact. By contrast, the two no-artifact cases (STALL+, CodeAgent) are both "framework"-style contributions (a static-analysis integration pipeline; a tool-use agent) from academic groups, where the empirical study/framework itself was apparently never packaged for release.

- **Industrial-lab releases (Microsoft, Amazon, ServiceNow, Alibaba) skew toward thin, low-commit "reproducibility snapshots" rather than maintained tools.** RepoFusion (1 commit), aiXcoder-7B-v2's v2 repo (2 commits), DraCo (4 commits), Repoformer (18 commits) and LingmaAgent's open-sourced prototype (13 commits, explicitly framed as a "prototype" vs. the internal production system) all read as one-time code drops accompanying a paper, not ongoing projects — even though stars are moderate (13–97). CodePlan goes a step further and has since been archived outright (read-only as of 2026-06-15), signalling Microsoft treats it as a closed research artifact rather than a living tool.

- **The newest agentic context-management systems (2026) show materially higher adoption signals than older RAG-completion systems (2023–2024).** SWE-Pruner (314 stars, 54 commits, updates through Aug 2026) and especially Prometheus (~1,100 stars, 1,083 commits, active issues/PRs) dwarf the classic retrieval-augmented completion line (RepoCoder 678★ is the outlier there, likely from being an early/foundational citation magnet rather than sustained engineering activity). This tracks the field's centre of gravity moving from "retrieve-then-complete" toward full coding-agent context/memory management, where a usable open-source agent has direct practical pull (SWE-Pruner is explicitly pitched as cutting real Claude Code API costs).

- **Structural/graph-based context-construction mechanisms (GraphCoder, RepoHyper, DraCo, LingmaAgent's knowledge graph, Prometheus's knowledge graph) all did release code**, suggesting graph-construction methods are not harder to open-source than plain retrieval methods — release behavior tracks lab/venue norms more than mechanism class.

- **License choice correlates loosely with commercial intent.** Permissive licenses (MIT, Apache-2.0) dominate across academic and industrial-lab artifacts (12 of 18 found repos). The two GPL-3.0-licensed projects in the sample (DraCo, Prometheus) are notable outliers; Prometheus explicitly dual-licenses with a paid commercial tier, i.e. GPL is being used here as a copyleft "open-core" gate rather than a purely academic-sharing choice.
