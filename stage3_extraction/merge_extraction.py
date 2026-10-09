#!/usr/bin/env python3
"""merge extraction chunks -> extraction.json + corpus.jsonl + facet count printout.
Usage: merge_extraction.py [out_base]  (default: the study folder). Downstream counts must
re-derive from extraction.json; nothing hand-maintained."""
import json, glob, sys, os, collections

BASE = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else BASE
os.makedirs(f"{OUT}/stage3_extraction", exist_ok=True)

meta = {}
for l in open(f"{BASE}/stage2_screening/candidates.jsonl"):
    r = json.loads(l)
    if r.get("arxiv_id"): meta[r["arxiv_id"]] = r

rows, seen = [], set()
for f in sorted(glob.glob(f"{BASE}/stage3_extraction/extraction_chunk*.json")):
    for r in json.load(open(f)):
        aid = r.get("arxiv_id")
        if not aid or aid in seen:
            if aid in seen: print("DUP", aid)
            continue
        seen.add(aid)
        m = meta.get(aid, {})
        r["title"] = m.get("title", r.get("title", ""))
        r["authors"] = m.get("authors", r.get("authors", []))
        # normalize mechanism-vocabulary leakage in repr_classes (logged normalization, not recoding):
        # 'similarity_retrieval' is retrieval over embeddings/lexical index -> embedding_retrieval;
        # 'agentic_exploration' describes the mechanism; the representation the agent reads is raw file
        # windows -> raw_window (mechanism field already captures agentic_exploration).
        NORM = {"similarity_retrieval": "embedding_retrieval", "agentic_exploration": "raw_window"}
        if r.get("repr_classes"):
            seen_rc, rc = set(), []
            for x in r["repr_classes"]:
                x = NORM.get(x, x)
                if x not in seen_rc:
                    seen_rc.add(x); rc.append(x)
            r["repr_classes"] = rc
        rows.append(r)
rows.sort(key=lambda r: r["arxiv_id"])
eligible = [r for r in rows if r.get("eligible", True)]
json.dump(rows, open(f"{OUT}/stage3_extraction/extraction.json", "w"), indent=1)
with open(f"{OUT}/corpus.jsonl", "w") as f:
    for r in eligible:
        f.write(json.dumps({"arxiv_id": r["arxiv_id"], "system": r.get("system",""), "title": r["title"],
                            "authors": r.get("authors", []), "year": r.get("year"),
                            "venue": r.get("venue","arXiv"), "peer_reviewed": r.get("peer_reviewed", False)}) + "\n")
print(f"total={len(rows)} eligible={len(eligible)} demoted={len(rows)-len(eligible)}")
for r in rows:
    if not r.get("eligible", True):
        print("  DEMOTED:", r["arxiv_id"], r.get("system",""), r.get("demote_criterion"), "-", str(r.get("demote_reason",""))[:90])
def prim(v): return v[0] if isinstance(v, list) and v else v
for facet, listy in [("repr_classes", True), ("mechanism", False), ("pipeline_position", False),
                     ("task", False), ("evaluation", False), ("wieringa", False), ("record_type", False),
                     ("scope", False), ("budget_reported", False), ("year", False)]:
    c = collections.Counter()
    for r in eligible:
        v = r.get(facet)
        if listy:
            for x in (v or []): c[x] += 1
        else: c[prim(v)] += 1
    print(f"== {facet} ==", dict(c.most_common()))
c = collections.Counter(prim(r.get("repr_classes")) for r in eligible)
print("== repr_primary ==", dict(c.most_common()))
