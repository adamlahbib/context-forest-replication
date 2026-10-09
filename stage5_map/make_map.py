#!/usr/bin/env python3
"""derive ALL map statistics from extraction.json -> _map_stats.json +
systematic_map.md. Usage: make_map.py [base_with_extraction] [out_base]."""
import json, sys, os, collections, re

BASE = sys.argv[1] if len(sys.argv) > 1 else __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
OUT = sys.argv[2] if len(sys.argv) > 2 else BASE
os.makedirs(f"{OUT}/stage5_map", exist_ok=True)
rows = [r for r in json.load(open(f"{BASE}/stage3_extraction/extraction.json")) if r.get("eligible", True)]
N = len(rows)
def prim(v): return v[0] if isinstance(v, list) and v else v

stats = {"N": N}
def cnt(name, fn, multi=False):
    c = collections.Counter()
    for r in rows:
        v = fn(r)
        if multi:
            for x in (v or []): c[x] += 1
        else: c[v] += 1
    stats[name] = dict(c.most_common()); return c

cnt("repr_primary", lambda r: prim(r.get("repr_classes")))
cnt("repr_any", lambda r: r.get("repr_classes"), multi=True)
cnt("mechanism", lambda r: r.get("mechanism"))
cnt("pipeline_position", lambda r: r.get("pipeline_position"))
cnt("task", lambda r: r.get("task"))
cnt("evaluation", lambda r: r.get("evaluation"))
cnt("wieringa", lambda r: r.get("wieringa"))
cnt("record_type", lambda r: r.get("record_type"))
cnt("scope", lambda r: r.get("scope"))
cnt("budget_reported", lambda r: bool(r.get("budget_reported")))
cnt("year", lambda r: r.get("year"))
cnt("peer_reviewed", lambda r: bool(r.get("peer_reviewed")))

# central cross-tab: repr_primary x evaluation
xt = collections.defaultdict(collections.Counter)
for r in rows: xt[prim(r.get("repr_classes"))][r.get("evaluation")] += 1
stats["repr_x_eval"] = {k: dict(v) for k, v in xt.items()}
# repr_primary x task
xt2 = collections.defaultdict(collections.Counter)
for r in rows: xt2[prim(r.get("repr_classes"))][r.get("task")] += 1
stats["repr_x_task"] = {k: dict(v) for k, v in xt2.items()}
norm = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())
GRAPH = {"call_dep_graph", "ast", "cpg_dataflow"}
# RQ4 isolation set
iso = [r for r in rows if r.get("evaluation") == "budget_matched"]
stats["budget_matched_records"] = [{"id": r["arxiv_id"], "system": r.get("system"),
                                    "confound_note": r.get("confound_note","")} for r in iso]
stats["n_budget_matched"] = len(iso)
stats["n_budget_reported"] = sum(1 for r in rows if r.get("budget_reported"))
# ---- evidence audit (amendment A2): two full-text checkers, authors decide disagreements
import glob
S1, S2, S3 = f"{BASE}/stage1_search", f"{BASE}/stage2_screening", f"{BASE}/stage3_extraction"
aud = [r["evidence_audit"] for r in rows if r.get("evidence_audit")]
if aud:
    V = ("budget-matched", "unmatched-single", "multi-change", "no-comparator")
    pa = [(a["verdict_A"], a["verdict_B"]) for a in aud]; n = len(pa)
    po = sum(x == y for x, y in pa) / n
    pe = sum(sum(x == v for x, _ in pa) * sum(y == v for _, y in pa) for v in V) / n / n
    fin = collections.Counter(a["verdict"] for a in aud)
    stats["evaudit"] = {"n": n, "agree": sum(x == y for x, y in pa), "kappa": round((po - pe) / (1 - pe), 2),
                        "decided_by_authors": sum(a["decided_by"].startswith("authors") for a in aud),
                        "decided_by_rule": sum(a["decided_by"] == "tier rule" for a in aud),
                        "rule_to_matched": sum(a["decided_by"] == "tier rule" and a["verdict"] == "budget-matched" for a in aud),
                        "final": {k.replace("-", "_"): fin.get(k, 0) for k in V},
                        "was_budget_matched": sum(a.get("prior") == "budget_matched_ablation" for a in aud),
                        "kept_budget_matched": sum(a.get("prior") == "budget_matched_ablation" and a["verdict"] == "budget-matched" for a in aud),
                        "graph_budget_matched": sum(r["evaluation"] == "budget_matched" and prim(r.get("repr_classes")) in GRAPH for r in rows)}
    mt = [a for a in aud if a["verdict"] == "budget-matched"]
    tc = collections.Counter(a.get("tier") for a in mt)
    stats["evaudit"]["tier"] = {k.replace("-", "_"): tc.get(k, 0) for k in ("measured-equal", "structured-smaller", "cap-filled")}
    stats["evaudit"]["compared"] = sum(a["verdict"] != "no-comparator" for a in aud)
    # strict reading: matched by BOTH independent checkers (no post-hoc rule)
    both = [a for a in aud if a["verdict_A"] == a["verdict_B"] == "budget-matched"]
    bsvf = [a for a in both if a.get("structure_vs_flat")]
    stats["evaudit"]["strict"] = {"matched": len(both), "matched_B": sum(a["verdict_B"] == "budget-matched" for a in aud),
                                  "svf": len(bsvf),
                                  "structure_better": sum(a["outcome"].lower().startswith("structure better") for a in bsvf),
                                  "flat_better": sum(a["outcome"].lower().startswith("flat better") for a in bsvf),
                                  "no_difference": sum(a["outcome"].lower().startswith("no clear") for a in bsvf)}
    stats["evaudit"]["svf_cap_only"] = sum(a.get("tier") == "cap-filled" for a in mt if a.get("structure_vs_flat"))
    svf = [a for a in mt if a.get("structure_vs_flat")]
    oc = collections.Counter(a["outcome"].split(":")[0].split(";")[0].split(".")[0].strip().lower() for a in svf)
    stats["evaudit"]["svf"] = {"n": len(svf), "structure_better": sum(o.startswith("structure better") for o in (a["outcome"].lower() for a in svf)),
                               "flat_better": sum(o.startswith("flat better") for o in (a["outcome"].lower() for a in svf)),
                               "no_difference": sum(o.startswith("no clear") for o in (a["outcome"].lower() for a in svf))}
    stats["evaudit"]["svf_graph_primary"] = sum(1 for r in rows if r.get("evidence_audit", {}).get("structure_vs_flat")
                                                and r["evaluation"] == "budget_matched" and prim(r.get("repr_classes")) in GRAPH)
    stats["evidence_audit"] = [dict(a, system=r.get("system"), evaluation=r["evaluation"], repr=prim(r.get("repr_classes")))
                               for r in rows for a in [r.get("evidence_audit")] if a]
stats["n_graph_class"] = sum(prim(r.get("repr_classes")) in GRAPH for r in rows)

# peer-reviewed vs preprint profile
for facet in ("evaluation", "scope", "task"):
    t = collections.defaultdict(collections.Counter)
    for r in rows: t["peer" if r.get("peer_reviewed") else "preprint"][r.get(facet)] += 1
    stats[f"pr_x_{facet}"] = {k: dict(v) for k, v in t.items()}

# ---- method facts from their own source files
ver = json.load(open(f"{S3}/verification.json"))
verdicts = [x.get("verdict") for v in ver for x in v.get("numbers", [])]
vc = collections.Counter(verdicts)
stats["verification"] = {"records": len(ver), "claims": len(verdicts), "confirmed": vc.get("CONFIRMED", 0),
                         "wrong": vc.get("WRONG", 0), "unretrievable": vc.get("UNRETRIEVABLE", 0),
                         "pct_confirmed": round(100 * vc.get("CONFIRMED", 0) / len(verdicts), 1)}
stats["kappa_coding"] = json.load(open(f"{S3}/_kappa.json"))
kdall = json.load(open(f"{S3}/_kappa_disagreements.json"))
kd = kdall["repr_primary"]
def kept_first(facet, key):
    final = {r["arxiv_id"]: (prim(r.get("repr_classes")) if key == "repr" else r.get(key)) for r in rows}
    ds = [x for x in kdall[facet] if x["arxiv_id"] in final]
    return sum(final[x["arxiv_id"]] == x["first"] for x in ds), sum(final[x["arxiv_id"]] == x["second"] for x in ds), len(ds)
for facet, key in (("repr_primary", "repr"), ("mechanism", "mechanism")):
    f1, f2, n_ = kept_first(facet, key)
    stats["kappa_coding"][facet]["final_first"], stats["kappa_coding"][facet]["final_second"] = f1, f2
    stats["kappa_coding"][facet]["final_other"] = n_ - f1 - f2
stats["kappa_coding"]["repr_disagreements"] = len(kd)
stats["kappa_coding"]["repr_disagreements_hybrid"] = sum("hybrid" in (x["first"], x["second"]) for x in kd)
first = {d["id"]: d["decision"] for f in glob.glob(f"{S2}/decisions_chunk*.json") for d in json.load(open(f))}
dual = [(first[d["id"]], d["decision"]) for d in json.load(open(f"{S2}/decisions_dual.json")) if d["id"] in first]
def kap(pairs, labels):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    pe = sum(sum(a == k for a, _ in pairs) * sum(b == k for _, b in pairs) for k in labels) / n / n
    return round((po - pe) / (1 - pe), 2) if pe < 1 else 1.0
bp = [(a == "include", b == "include") for a, b in dual]
stats["screening_dual"] = {"n": len(dual), "agree_binary": sum(a == b for a, b in bp), "kappa_binary": kap(bp, (True, False)),
                           "agree_3way": sum(a == b for a, b in dual), "kappa_3way": kap(dual, ("include", "exclude", "uncertain")),
                           "include_vs_exclude_flips": sum({a, b} == {"include", "exclude"} for a, b in dual)}
nl = lambda f: sum(1 for l in open(f) if l.strip())
stats["funnel"] = {"identified": nl(f"{S1}/identified.jsonl"), "prefilter_pass": nl(f"{S2}/candidates.jsonl"),
                   "screened": nl(f"{S2}/candidates_sampled.jsonl")}
stats["funnel"]["prefilter_removed"] = stats["funnel"]["identified"] - stats["funnel"]["prefilter_pass"]
stats["funnel"]["cap_removed"] = stats["funnel"]["prefilter_pass"] - stats["funnel"]["screened"]
stats["funnel"]["extracted"] = sum(1 for r in json.load(open(f"{S3}/extraction.json")))
stats["funnel"]["demoted"] = stats["funnel"]["extracted"] - N
pf = json.load(open(f"{S1}/_prefilter_screen.json"))
capped = {norm(json.loads(l)["title"]) for l in open(f"{S2}/candidates.jsonl") if l.strip()} - \
         {norm(json.loads(l)["title"]) for l in open(f"{S2}/candidates_sampled.jsonl") if l.strip()}
stats["prefilter_check"] = {"screened": len(pf), **{d: sum(x["decision"] == d for x in pf) for d in ("include", "uncertain", "exclude")},
                            "cap_records": len(capped), "cap_included": sum(norm(x["title"]) in capped and x["decision"] != "exclude" for x in pf)}
sc = json.load(open(f"{S1}/_snowball_check.json")); scr = json.load(open(f"{S1}/_snowball_screen.json"))
new_ = [x for x in scr if not x.get("already_in_corpus")]
stats["snowball"] = {"papers": len(sc["papers"]), "resolved": sum(p["n_refs"] is not None for p in sc["papers"]),
                     "refs": sum(p["n_refs"] or 0 for p in sc["papers"]), "flagged": len(scr),
                     **{d: sum(x["decision"] == d for x in new_) for d in ("include", "uncertain", "exclude")}}
aid = lambda t: (re.search(r"\d{4}\.\d{4,5}", t or "") or [None])[0]
missed = {x.get("arxiv_id") or norm(x["title"]) for x in pf if x["decision"] == "include"} | \
         {aid(x.get("source_id")) or norm(x["title"]) for x in new_ if x["decision"] == "include"}
stats["coverage"] = {"missed_likely": len(missed), "recall_denominator": N + len(missed), "recall_pct": round(100 * N / (N + len(missed)))}

json.dump(stats, open(f"{OUT}/stage5_map/_map_stats.json", "w"), indent=1)

md = [f"# Stage 5 — Systematic Map (auto-derived from extraction.json; N={N})", ""]
for name in ("repr_primary","repr_any","mechanism","pipeline_position","task","evaluation",
             "wieringa","record_type","scope","budget_reported","year","peer_reviewed"):
    md += [f"## {name}", "", "| value | n |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in stats[name].items()]; md += [""]
md += ["## repr_primary × evaluation", "", "| repr | budget_matched | unmatched_single | multi_change | demonstrated | not_eval |", "|---|---|---|---|---|---|"]
for k, v in stats["repr_x_eval"].items():
    md.append(f"| {k} | {v.get('budget_matched',0)} | {v.get('unmatched_single',0)} | {v.get('multi_change',0)} | {v.get('demonstrated',0)} | {v.get('not_evaluated',0)} |")
md += ["", f"## RQ4: budget-matched ablations ({len(iso)}/{N})", ""]
md += [f"- {r['system']} ({r['id']}): {r['confound_note'][:160]}" for r in stats["budget_matched_records"]]
open(f"{OUT}/stage5_map/systematic_map.md", "w").write("\n".join(md) + "\n")
print(f"map written: N={N}, budget_matched={len(iso)}, budget_reported={stats['n_budget_reported']}")
