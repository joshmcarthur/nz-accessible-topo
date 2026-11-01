#!/usr/bin/env python3
"""
analyse_qgis_project.py — summarise LINZ's Topo50 QGIS cartography.

Reads a checkout of github.com/linz/topographic-qgis (MIT) and, optionally, a
carto_text GeoParquet sample (e.g. linz/topographic-system
packages/map/assets/project/nztopo50_carto_text.parquet).

Reports: the spot-colour palette, fonts/styles in the layer QMLs, and label
font/style/size distribution in the carto_text data (labels are data-defined).

Usage: python3 tools/analyse_qgis_project.py /path/to/topographic-qgis [carto_text.parquet]
"""
import collections
import glob
import os
import re
import sys


def main(repo, parquet=None):
    base = os.path.join(repo, "map-series", "nztopo50", "style-layer")
    print("## Palette (nztopo50_colours.gpl)\n\n| Name | RGB |\n|---|---|")
    for line in open(os.path.join(base, "nztopo50_colours.gpl")):
        m = re.match(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+(\S+)", line)
        if m:
            print(f"| {m.group(4)} | {m.group(1)}, {m.group(2)}, {m.group(3)} |")
    fonts = collections.Counter()
    for f in glob.glob(os.path.join(base, "*.qml")):
        s = open(f, encoding="utf-8", errors="ignore").read()
        for t in re.findall(r"<text-style[^>]*>", s):
            fam = re.search(r'fontFamily="([^"]+)"', t)
            st = re.search(r'namedStyle="([^"]*)"', t)
            fonts[f"{fam.group(1) if fam else '?'} / {st.group(1) if st else ''}"] += 1
    print("\n## Fonts in layer QMLs (default text styles)\n\n| Font / style | Uses |\n|---|---:|")
    for k, v in fonts.most_common():
        print(f"| {k} | {v} |")
    if parquet:
        import pyarrow.parquet as pq
        d = pq.read_table(parquet).to_pydict()
        n = len(d["style"])
        ital = sum(1 for s in d["style"] if "Italic" in (s or ""))
        print(f"\n## Label data sample: {n} carto_text rows\n")
        print(f"Italic (any): **{ital} of {n} ({100 * ital / n:.0f}%)**\n")
        for col in ("style", "text_font", "size"):
            print(f"| {col} | count |\n|---|---:|")
            for k, v in collections.Counter(d[col]).most_common():
                print(f"| {k!s} | {v} |")
            print()


if __name__ == "__main__":
    main(*sys.argv[1:3])
