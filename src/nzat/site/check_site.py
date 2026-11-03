"""
check_site.py — the site must meet the standards the project argues for.

Serves site/dist, then on every page:
  S1  axe-core: no WCAG 2.0/2.1/2.2 A/AA or best-practice violations
  S2  no rendered italic text (R-05 applies to the site too)
  S3  every internal link resolves, including #anchors on the target page

Needs: playwright (Python) with Chromium; site/node_modules/axe-core.
Usage: python3 tools/check_site.py
"""

import glob
import os
import re
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

from nzat.paths import ROOT

DIST = os.path.join(ROOT, "site", "dist")
AXE = open(os.path.join(ROOT, "site", "node_modules", "axe-core", "axe.min.js")).read()
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]
PORT = 4329

ITALIC_JS = """() => [...document.querySelectorAll('body *')]
  .filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))
  .filter(e => getComputedStyle(e).fontStyle !== 'normal')
  .map(e => e.tagName.toLowerCase() + ': ' + e.textContent.trim().slice(0, 40))"""


def internal_links(pages):
    """S3: static check over the built HTML — no browser needed."""
    problems, ids_cache = [], {}

    def ids(page_file):
        if page_file not in ids_cache:
            ids_cache[page_file] = set(
                re.findall(r'\bid="([^"]+)"', open(page_file, encoding="utf-8").read())
            )
        return ids_cache[page_file]

    for path in pages:
        src = os.path.join(DIST, path.lstrip("/"), "index.html")
        for href in set(
            re.findall(r'href="(/[^"]*)"', open(src, encoding="utf-8").read())
        ):
            target, _, anchor = href.partition("#")
            f = os.path.join(DIST, target.lstrip("/"))
            page = f if os.path.isfile(f) else os.path.join(f, "index.html")
            if not os.path.exists(page):
                problems.append(f"S3 {path} broken link {href}")
            elif anchor and page.endswith(".html") and anchor not in ids(page):
                problems.append(f"S3 {path} missing anchor {href}")
    return problems


def main():
    pages = sorted(
        "/" + os.path.relpath(p, DIST).replace("index.html", "")
        for p in glob.glob(DIST + "/**/index.html", recursive=True)
    )
    srv = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--directory", DIST],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    problems = internal_links(pages)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1280, "height": 900})
            for path in pages:
                pg.goto(f"http://localhost:{PORT}{path}")
                pg.add_script_tag(content=AXE)
                v = pg.evaluate(
                    "async (tags) => (await axe.run(document, {runOnly: {type: 'tag', values: tags}}))"
                    ".violations.map(v => `${v.id} (${v.nodes.length}): ${v.help}`)",
                    TAGS,
                )
                problems += [f"S1 {path} {x}" for x in v]
                problems += [f"S2 {path} italic {x}" for x in pg.evaluate(ITALIC_JS)]
            b.close()
    finally:
        srv.terminate()
    print(f"{len(pages)} pages checked")
    if problems:
        print("FAIL\n  " + "\n  ".join(problems))
        sys.exit(1)
    print("OK — S1, S2, S3 pass")


if __name__ == "__main__":
    main()
