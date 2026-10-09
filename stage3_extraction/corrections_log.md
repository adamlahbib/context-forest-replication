# Stage 3 — Author Adjudication Log (Study 5, 2026-08-30)

Independent verification covered **all 83 eligible records, 235 numeric claims** (94.5% confirmed,
13 wrong, 0 unretrievable) plus non-blind facet spot-checks; a blind second coder re-coded all 83 on
three facets (κ: repr_primary 0.41, mechanism 0.67, evaluation 0.56). Every flagged item was
adjudicated below; corrections apply programmatically via `apply_adjudications.py`.

## Number corrections — 13 WRONG, all ACCEPTED

All thirteen verifier corrections were specific to a table cell and accepted verbatim (see
`apply_adjudications.py` for exact replacement values). The recurring error shapes: adjacent-column
misreads (SWE-agent File-F1 0.544 vs Block-Recall 0.625; GraphCodeAgent's GPT-4o baseline 40.87 vs
the Gemini value 42.17 in the same row), **relative-vs-absolute mislabels** (two "+pts" figures that
are relative-% improvements; a 135.9% max-relative gain misattributed to the headline model whose
paper-stated gain is 18.6%), swapped language pairs (aiXcoder-7B-v2 TypeScript/C#), a wrong-config
citation (HCP Table 4 vs Table 5), a range floor from the wrong model (5.95× not 6.03×), an
overclaimed customization comparison (Finkler26 is baseline-vs-baseline), and a wrong-repo file
count (turicreate 237, not 293).

## Construct rule R1 (added; applied corpus-wide)

Two verifiers flagged retrieval-based records in OPPOSITE directions (2312.10101 → raw_window;
2310.11248 → raw_window vs. many retrieval systems coded embedding_retrieval). Rule: a context
**composed of similarity-retrieved snippets** (lexical or dense) codes `repr = embedding_retrieval`;
`raw_window` is contiguous local file text without retrieval. The representation facet describes what
the context is made of; the mechanism facet already captures how it was selected. Both flags REJECTED
under R1.

## Facet recodes — ACCEPTED

- repr_primary: 2406.11612 → hybrid (per-task representations differ); 2605.26177 →
  repo_map_skeleton (structured editing-location map is the artifact); 2601.13933 → hybrid
  (NL analysis report + embedded snippets); 2406.04464 → ast (AutoCodeRover's AST search tools;
  no call graph in the paper).
- mechanism: 2601.10112 → skeletonization (deterministic whole-repo architectural map);
  2607.26805 → similarity_retrieval (BM25 + API-overlap rules); 2510.08850 → learned_compression
  (retrieval compiled into weights); 2508.21433 → none_fixed_window (observation masking is the
  paper's central finding).
- evaluation — **strict budget-matched rule** (representation/mechanism varied at held-constant
  *realized* budget): 9 records downgraded (2306.10763, 2402.03630 → ablated_measured not
  demonstrated since baselines exist, 2406.18294, 2306.10998, 2504.08862, 2601.16746 — nominal
  targets exceeded, so realized budgets differ, 2604.24678 — representation constant, adaptation
  varied, 2607.25431 — holds quality constant and measures tokens, the inverse design; 2508.08322 →
  demonstrated — 5-task single-codebase case study, no comparator). Net effect: the RQ4
  budget-matched set is **10/83**, down from 17 as extracted — reported as the paper's headline
  evidence-integrity finding, not hidden.

## Adjudicated divergence from a verifier suggestion (noted explicitly)

For 2402.03630 (IDECoder) the verifier suggested `demonstrated`; the adjudication instead applied
`ablated_measured`, because the paper compares against in-file/all-import/RAG baselines — a
comparator exists, which is the F5 boundary; what it lacks is budget matching. The applied value
therefore differs from the suggested one deliberately, with this rationale.

## Suggestions REJECTED (rationale)

- 2312.10101 and 2310.11248 repr flags — rejected under R1 (above).
- Second-coder-only budget-matched downgrades of 2303.12570, 2406.01359, 2510.00446 — rejected: the
  full-text verifier independently confirmed the extractor's budget-matched coding for all three,
  and the second coder read two of the three from the abstract only.
- 2607.01138 mechanism → "hybrid" — rejected: not a mechanism-facet value; extractor's coding kept.

## stop_detail amendments (3)

2504.08862 (retrieved chunks concatenate with, not replace, in-file context); 2508.02998 (failure
attribution is LLM-voting, not human annotation); 2607.24884 (evidence ranking uses Eq. 6, distinct
from the generation-uncertainty formula).

## Blind second-coder reliability (context for the κ table)

repr_primary κ = 0.41 is dominated by X → hybrid confusions (27 of 40 disagreements involve the
hybrid boundary); the paper therefore anchors headline claims to groupings robust to that boundary
(structural-vs-flat aggregate) and reports the hybrid construct as the least reliable facet.
Evaluation κ = 0.56: 9 of 12 disagreements were the second coder downgrading budget_matched — the
same direction the verifiers flagged and the adjudication above largely upheld.
