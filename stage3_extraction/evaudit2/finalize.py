#!/usr/bin/env python3
"""Final isolation verdicts: checker A (full-text agents) and checker B (GPT) agree -> that verdict;
disagree -> the authors' decision in human_decisions.json ({arxiv_id: {"verdict", "reason"}}).
Writes ../evaudit_final.json, consumed by apply_adjudications.py. Fails if any disagreement is undecided."""
import json, glob, os, re
here = os.path.dirname(os.path.abspath(__file__))
PRIOR = {r["arxiv_id"]: r["evaluation"] for f in sorted(glob.glob(f"{here}/../evaudit_in/batch*.json")) for r in json.load(open(f))}
A = [r for f in sorted(glob.glob(f"{here}/../evaudit_out/batch*.json")) for r in json.load(open(f))]
B = {os.path.basename(f)[:-5]: json.loads(re.search(r"\{.*\}", open(f).read(), re.S).group(0))
     for f in glob.glob(f"{here}/out/*.json") if open(f).read().strip()}
TIER = {t["arxiv_id"]: t for f in ("tier_out.json", "tier_out_b.json") if os.path.exists(f"{here}/{f}")
        for t in json.load(open(f"{here}/{f}"))}
H = json.load(open(f"{here}/human_decisions.json")) if os.path.exists(f"{here}/human_decisions.json") else {}
out, missing = [], []
for a in A:
    i = a["arxiv_id"]; b = B.get(i)
    assert b, f"no checker-B verdict for {i}"
    t = TIER.get(i)
    if a["verdict"] == b["verdict"]:
        v, by = a["verdict"], "both checkers"
    elif i in H:
        v, by = H[i]["verdict"], "authors (checkers disagreed)"
    elif {a["verdict"], b["verdict"]} == {"budget-matched", "unmatched-single"} and t:
        # written rule (Table III): matched iff the tier pass found a shared filled cap or per-arm counts showing
        # the structured arm no larger; otherwise unmatched
        v, by = ("budget-matched" if t["tier"] != "not-matched" else "unmatched-single"), "tier rule"
    else:
        missing.append(i); continue
    src = b if (i in H and v == b["verdict"]) else a   # describe the comparison the final verdict judged
    out.append({k: src.get(k) or a.get(k) for k in ("arxiv_id", "system", "source_checked", "comparison", "model_config",
                                      "dataset_metric", "budget_control", "arm_a", "arm_b", "other_changes", "delta", "graph_class_check")}
               | {"verdict": v, "prior": PRIOR[i], "verdict_A": a["verdict"], "verdict_B": b["verdict"], "decided_by": by,
                  "rationale": a.get("rationale"), "human_reason": H.get(i, {}).get("reason")}
               | ({"tier": t["tier"], "structure_vs_flat": t["structure_vs_flat"], "structured_arm": t.get("structured_arm"),
                   "flat_arm": t.get("flat_arm"), "outcome": t.get("outcome"), "tier_evidence": t.get("evidence"),
                   "tier_note": t.get("note")} if t else {}))
assert not missing, f"undecided disagreements: {missing}"
json.dump(out, open(f"{here}/../evaudit_final.json", "w"), indent=1)
print(f"evaudit_final.json: {len(out)} records, {sum(o['decided_by'].startswith('authors') for o in out)} decided by authors, "
      f"{sum(o['decided_by'] == 'tier rule' for o in out)} by the tier rule")
