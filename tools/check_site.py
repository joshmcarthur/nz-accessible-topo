#!/usr/bin/env python3
"""
check_site.py — the site must meet the standards the project argues for.

Serves site/dist, then on every page:
  S1  axe-core: no WCAG 2.0/2.1/2.2 A/AA or best-practice violations
  S2  no rendered italic text (R-05 applies to the site too)

Needs: playwright (Python) with Chromium; site/node_modules/axe-core.
Usage: python3 tools/check_site.py
"""
import glob
import os
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "site", "dist")
AXE = open(os.path.join(ROOT, "site", "node_modules", "axe-core", "axe.min.js")).read()
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]
PORT = 4329

ITALIC_JS = """() => [...document.querySelectorAll('body *')]
  .filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))
  .filter(e => getComputedStyle(e).fontStyle !== 'normal')
  .map(e => e.tagName.toLowerCase() + ': ' + e.textContent.trim().slice(0, 40))"""


def main():
    pages = sorted("/" + os.path.relpath(p, DIST).replace("index.html", "")
                   for p in glob.glob(DIST + "/**/index.html", recursive=True))
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--directory", DIST],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    problems = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1280, "height": 900})
            for path in pages:
                pg.goto(f"http://localhost:{PORT}{path}")
                pg.add_script_tag(content=AXE)
                v = pg.evaluate("async (tags) => (await axe.run(document, {runOnly: {type: 'tag', values: tags}}))"
                                ".violations.map(v => `${v.id} (${v.nodes.length}): ${v.help}`)", TAGS)
                problems += [f"S1 {path} {x}" for x in v]
                problems += [f"S2 {path} italic {x}" for x in pg.evaluate(ITALIC_JS)]
            b.close()
    finally:
        srv.terminate()
    print(f"{len(pages)} pages checked")
    if problems:
        print("FAIL\n  " + "\n  ".join(problems))
        sys.exit(1)
    print("OK — S1, S2 pass")


if __name__ == "__main__":
    main()
