#!/usr/bin/env python3
"""Study 5: author adjudication of the verification pass + blind-second-coder disagreements.
Applies accepted corrections onto extraction.json (in place, path via arg). Decisions and
rationale in corrections_log.md. Run order: merge_extraction.py -> apply_adjudications.py ->
summarize_verification.py -> make_map.py. Usage: apply_adjudications.py [base]"""
import json, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
P = f"{BASE}/stage3_extraction/extraction.json"
rows = json.load(open(P))
by = {r["arxiv_id"]: r for r in rows}

def fix_num(aid, metric_sub, value=None, metric=None, where=None):
    r = by[aid]
    for n in r.get("key_numbers", []):
        if metric_sub.lower() in n["metric"].lower():
            if value: n["value"] = value
            if metric: n["metric"] = metric
            if where: n["where"] = where
            return
    raise KeyError(f"{aid}: no key_number matching '{metric_sub}'")

# ---- 1. Number corrections (13 WRONG, all accepted; details in corrections_log.md)
fix_num("2602.05892", "File-level F1", value="SWE-agent 0.544 vs mini-SWE-Agent 0.634 (File-level F1; 0.625 is SWE-agent's Block-level Recall)")
fix_num("2607.06065", "Resolve-rate-after-revision", value="27.5% -> 35.8% (+8.3pp)", where="Table 2")
fix_num("2503.15301", "Unseen-language", value="TypeScript +19.2% (46.96->55.96 EM); C# +20.6% (46.32->55.88 EM)")
fix_num("2406.18294", "EM improvement, Starcoder2-7B", value="31.45% -> 35.76%", where="Table 4 (top-k=5)")
fix_num("2503.18305", "Pass@1 (Claude-3.5-Sonnet", value="67.7% vs 49.1% (paper: 'surpassing the best baseline PE by 18.6%'); the 135.9% max-relative gain belongs to Qwen-2.5-Coder-14B vs Basic RAG")
fix_num("2603.28119", "issue resolution rate", value="GPT-5.2: 0.578 vs 0.532 (+4.6pp, +8.6% relative); DeepSeek-V3.2 is the +9.2%-relative case")
fix_num("2603.28119", "compression ratio", value="5.95x-6.55x across models (min Qwen3-Coder-Next 5.95x, max GPT-5.2 6.55x)", where="Table 2")
fix_num("2606.08135", "Pass@1 (DevEval", value="31.01% (+22.76% RELATIVE over AllianceCoder 25.26%, not points)")
fix_num("2606.08135", "Pass@1 (CoderEval", value="56.09% (relative improvement over AllianceCoder ~52.17%; absolute gap ~3.9-4.1 pts)")
fix_num("2504.10046", "Pass@1 CoderEval", value="58.14/53.91 vs GPT-4o baseline 40.87%")
fix_num("2410.21157", "Baseline (in-file only) EM", value="22.6%")
fix_num("2602.05780", "model size", value="uncustomized 8B models (Llama-8B, Granite-8B) competitive with uncustomized Qwen2.5-72B — a baseline-vs-baseline comparison, not customized-vs-uncustomized")
fix_num("2607.01425", "benchmark scale", value="turicreate: 237 files / 1,725 functions (293 files belongs to the pants repository in the same table)")

# ---- 2. Construct rule R1 (logged): a context COMPOSED OF similarity-retrieved snippets (lexical
# or dense) codes repr=embedding_retrieval; raw_window means contiguous local windows without
# retrieval. Under R1 the two opposite-direction verifier flags on 2312.10101 and 2310.11248 are
# REJECTED (keep embedding_retrieval).

def set_facet(aid, **kw):
    r = by[aid]
    for k, v in kw.items():
        if k == "repr_primary":
            rc = r.get("repr_classes") or []
            r["repr_classes"] = [v] + [x for x in rc if x != v]
        else:
            r[k] = v

# repr_primary recodes (accepted)
set_facet("2406.11612", repr_primary="hybrid")
set_facet("2605.26177", repr_primary="repo_map_skeleton")
set_facet("2601.13933", repr_primary="hybrid")
set_facet("2406.04464", repr_primary="ast")
# mechanism recodes (accepted)
set_facet("2601.10112", mechanism="skeletonization")
set_facet("2607.26805", mechanism="similarity_retrieval")
set_facet("2510.08850", mechanism="learned_compression")
set_facet("2508.21433", mechanism="none_fixed_window")
# evaluation recodes — strict budget-matched rule (representation/mechanism varied at
# held-constant realized budget). Verifier+second-coder concurrence or verifier full-text
# evidence accepted; second-coder-only downgrades where the verifier's full-text check
# AGREED with the extractor (2303.12570, 2406.01359, 2510.00446) are REJECTED.
for aid, val in [("2306.10763", "ablated_measured"), ("2402.03630", "ablated_measured"),
                 ("2406.18294", "ablated_measured"), ("2306.10998", "ablated_measured"),
                 ("2504.08862", "ablated_measured"), ("2508.08322", "demonstrated"),
                 ("2601.16746", "ablated_measured"), ("2604.24678", "ablated_measured"),
                 ("2607.25431", "ablated_measured")]:
    set_facet(aid, evaluation=val)
# stop_detail amendments (fair-paraphrase flags)
by["2504.08862"]["stop_detail"] = (by["2504.08862"].get("stop_detail","").rstrip() +
    " [Adjudication: retrieved chunks are CONCATENATED with in-file context (Sec 3.3), not a replacement for it.]")
by["2508.02998"]["stop_detail"] = (by["2508.02998"].get("stop_detail","").rstrip() +
    " [Adjudication: failure attribution is by LLM voting, not human manual annotation.]")
by["2607.24884"]["stop_detail"] = (by["2607.24884"].get("stop_detail","").rstrip() +
    " [Adjudication: evidence filtering/ranking uses Eq. 6, distinct from the generation-uncertainty formula.]")

# ---- Evidence audit (amendment A2, 2026-10-09; reviewer request). Every record with a comparator was re-judged at
# full text by two independent checkers (Claude agents; GPT) on four levels; disagreements decided by the authors.
LEVEL = {"budget-matched": "budget_matched", "unmatched-single": "unmatched_single",
         "multi-change": "multi_change", "no-comparator": "demonstrated"}
audit = json.load(open(f"{BASE}/stage3_extraction/evaudit_final.json"))
assert {a["arxiv_id"] for a in audit} == {r["arxiv_id"] for r in rows if r.get("eligible", True)
                                          and r.get("evaluation") in ("budget_matched_ablation", "ablated_measured")}
for a in audit:
    by[a["arxiv_id"]]["evaluation"] = LEVEL[a["verdict"]]
    by[a["arxiv_id"]]["evidence_audit"] = a

for r in rows: r["adjudicated"] = True  # compute_kappa.py refuses post-adjudication data
json.dump(rows, open(P, "w"), indent=1)
print("Study 5 adjudications applied:", len(rows), "records")
