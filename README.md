# Replication package: "Seeing the Forest"

A systematic mapping study of structure-aware context engineering for repository-level code LLMs and agents
(83 studies, 2023–2026). This package holds everything needed to check or regenerate every corpus count and statistic in the paper.

## Rebuild every number

```bash
cd stage3_extraction
python3 merge_extraction.py      # extraction chunks -> extraction.json
python3 compute_kappa.py         # reliability, PRE-adjudication (refuses adjudicated data)
python3 apply_adjudications.py   # corrections, recodes, evidence audit (amendment A2)
python3 summarize_verification.py
python3 ../stage5_map/make_map.py              # -> stage5_map/_map_stats.json
python3 ../stage6_report/render_report.py      # fills report.tmpl.md -> report.md; fails on any unfilled value
```

Python 3 standard library only. `build/slr_build_pdf.sh <stage6_report> "<title>" split anon a4` builds the PDFs (needs pandoc and tectonic).

## What is where

| Stage | Contents |
|---|---|
| `00_protocol.md` | Research questions, criteria, facet scheme, seeds and the 200-record cap; fixed before retrieval |
| `stage1_search/` | Search scripts, every query with hit counts (`search_log.md`), retrieved records, gold-set recall; coverage checks: screening of all pre-filter rejects (`_prefilter_screen.json`) and a bounded reference-list check (`snowball_check.py`, `_snowball_check.json`, `_snowball_screen.json`) |
| `stage2_screening/` | Screening decisions, the blind 20% dual-screen sample, adjudication and amendments |
| `stage3_extraction/` | `extraction.json` (single source of truth), number verification, blind second coding, `corrections_log.md` |
| `stage3_extraction/evaudit_*`, `evaudit2/` | Full-text evidence audit: checker A (`evaudit_out/`), checker B (`evaudit2/out/`, prompt and runner), budget tiers (`evaudit2/tier_out.json`), author decisions (`evaudit2/human_decisions.json`), final verdicts (`evaudit_final.json`) |
| `stage4_artifacts/` | Public-code survey of 20 purposively selected systems |
| `stage5_map/` | `make_map.py` and the derived statistics every manuscript count is read from |
| `stage6_report/` | Manuscript template, renderer, bibliography |

## Not included

Full texts of the primary studies (copyright); each audit record names the arXiv version read. Raw model transcripts are omitted;
each checker's structured verdict, the comparison it judged and a deciding quote are included. The arXiv and OpenAlex search
helpers come from github.com/lingzhi227/agent-research-skills (commit 9e6c085) and are not redistributed; set `ARS_DIR` to re-run.

## Tools used

LLM agents (Claude, Anthropic) did screening, extraction, verification, second coding, coverage checks and the first audit pass;
GPT (OpenAI, via the Codex CLI) was the second audit checker. Disagreements were decided by an author checking an
assistant-proposed verdict, as recorded in the files above.
