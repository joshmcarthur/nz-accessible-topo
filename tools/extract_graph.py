#!/usr/bin/env python3
"""
extract_graph.py — build the source → finding → recommendation → change graph
from the markdown docs, for the site's Sankey and trace pages.

Writes site/src/data/graph.json. Exits 1 (lint) if any finding has no source
or any recommendation rests on nothing — the evidence chain must be complete.

Rules for implicit citations (documented so they can be argued with):
  W1–W8, "audit (D)"     → S-OUR-AUDIT-WEB
  P1–P9                  → S-OUR-AUDIT-PRINT
  font_check             → S-OUR-FONTCHECK
  visuals/06             → S-OUR-SHAPING-TEST
  palette v0             → S-OUR-PALETTE-V0
  real Kawarau render    → S-OUR-REAL-RENDER
"""
import json
import os
import re
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
GRADE_ORDER = {"A": 0, "A–": 0.5, "B": 1, "B–": 1.5, "B/C": 1.5, "C": 2, "C/D": 2.5, "D": 3}

IMPLICIT = [
    (re.compile(r"\bW[1-8]\b|audit \(D\)|our audit|\baudit\b"), "S-OUR-AUDIT-WEB"),
    (re.compile(r"\bP[1-9]\b"), "S-OUR-AUDIT-PRINT"),
    (re.compile(r"font_check"), "S-OUR-FONTCHECK"),
    (re.compile(r"visuals/06"), "S-OUR-SHAPING-TEST"),
    (re.compile(r"palette v0", re.I), "S-OUR-PALETTE-V0"),
    (re.compile(r"real Kawarau|real Topo50 slopes", re.I), "S-OUR-REAL-RENDER"),
]
CHANGE_NOUN = {
    "R-03": "hillshade light direction", "R-04": "contour colours and widths", "R-05": "italic fonts replaced",
    "R-07": "label colours darkened", "R-08": "letter-spacing added", "R-09": "text sizes floored",
    "R-10": "vegetation fills and stipple", "R-11": "track, hazard and red-label changes",
}


def read(p):
    return open(os.path.join(DOCS, p), encoding="utf-8").read()


def sources():
    out = {}
    for line in read("sources.md").splitlines():
        m = re.match(r"\|\s*(S-[A-Z0-9-]+)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            sid, grade, text = m.groups()
            title = re.sub(r"\s*https?://\S+", "", text).strip()
            url = (re.search(r"https?://[^\s)|]+", text) or [None])[0]
            out[sid] = {"id": sid, "grade": grade.strip(), "title": title, "url": url}
    return out


def sections(text, level, prefix):
    pat = re.compile(rf"^{'#' * level} ({prefix}-\d+) — (.+)$", re.M)
    hits = list(pat.finditer(text))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        nxt = re.search(r"^#{1,%d} " % level, text[m.end():end], re.M)
        body = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():end]
        yield m.group(1), m.group(2).strip(), body.strip()


def cited(body, known):
    ids = set(re.findall(r"\bS-[A-Z0-9-]+[A-Z0-9]\b", body)) & set(known)
    for rx, sid in IMPLICIT:
        if rx.search(body):
            ids.add(sid)
    return sorted(ids)


def main():
    S = sources()
    findings = {}
    for fn in sorted(os.listdir(os.path.join(DOCS, "findings"))):
        text = read(f"findings/{fn}")
        topic = re.match(r"# Findings: (.+)", text).group(1)
        for fid, title, body in sections(text, 2, "F"):
            findings[fid] = {"id": fid, "title": title, "topic": topic, "file": f"findings/{fn}",
                             "body": body, "sources": cited(body, S)}

    recs = {}
    rtext = read("recommendations.md")
    for rid, title, body in sections(rtext, 3, "R"):
        rests = re.search(r"\*\*Rests on:\*\*([^\n]+)", body)
        line = rests.group(1) if rests else ""
        fids = sorted(set(re.findall(r"\bF-\d+\b", line + " " + body)) & set(findings))
        sids = cited(line + " " + body, S)
        provisional = "provisional" in (title + body[:200]).lower()
        recs[rid] = {"id": rid, "title": re.sub(r"\s*—\s*\*\*.*?\*\*", "", title).strip(),
                     "provisional": provisional, "body": body, "findings": fids, "sources": sids}

    changes = []
    clog = os.path.join(DOCS, "styles", "accessible-v0-changes.md")
    for m in re.finditer(r"^## (R-\d+) \((\d+)\)", open(clog, encoding="utf-8").read(), re.M):
        rid, n = m.group(1), int(m.group(2))
        if rid in recs:
            changes.append({"id": f"C-{rid}", "rec": rid, "count": n,
                            "title": f"{n} × {CHANGE_NOUN.get(rid, 'style edits')}"})

    # best evidence grade along each chain
    def best(grades):
        g = [x for x in grades if x in GRADE_ORDER]
        return min(g, key=GRADE_ORDER.get) if g else "D"

    for f in findings.values():
        f["grade"] = best(S[s]["grade"] for s in f["sources"])
    for r in recs.values():
        r["grade"] = best([findings[f]["grade"] for f in r["findings"]] + [S[s]["grade"] for s in r["sources"]])
        r["implemented"] = any(c["rec"] == r["id"] for c in changes)

    problems = [f"{f['id']} cites no source" for f in findings.values() if not f["sources"]]
    problems += [f"{r['id']} rests on nothing" for r in recs.values() if not (r["findings"] or r["sources"])]
    used = {s for f in findings.values() for s in f["sources"]} | {s for r in recs.values() for s in r["sources"]}
    unused = sorted(set(S) - used)

    md = markdown.Markdown(extensions=["tables"])
    for item in list(findings.values()) + list(recs.values()):
        # Snippets sit under the page's h1, so their ### headings become h2.
        html = md.reset().convert(item.pop("body"))
        item["html"] = re.sub(r"<(/?)h3>", r"<\1h2>", html)

    graph = {"sources": [S[k] | {"used": k in used} for k in S], "findings": list(findings.values()),
             "recommendations": sorted(recs.values(), key=lambda r: int(r["id"][2:])), "changes": changes,
             "unusedSources": unused}
    out = os.path.join(ROOT, "site", "src", "data", "graph.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(graph, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(S)} sources ({len(unused)} not cited), {len(findings)} findings, {len(recs)} recommendations, "
          f"{len(changes)} change groups")
    if unused:
        print("  not cited by any finding/recommendation:", ", ".join(unused))
    if problems:
        print("LINT FAIL\n  " + "\n  ".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
