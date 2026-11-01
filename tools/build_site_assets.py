#!/usr/bin/env python3
"""
build_site_assets.py — pre-render every comparison variant under every condition.

Reads site/src/data/comparisons.json and conditions.json; writes
site/public/compare/<comparison>/<variant-index>-<condition>.webp plus
site/src/data/compare-assets.json (sizes, for layout without shift).

Same models as tools/palette_audit.py, so the site shows exactly what the
audits measure. Adding a comparison = adding an entry to comparisons.json. A variant may
give "crop": [x0, y0, x1, y1] to cut a region from a larger source image.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import palette_audit as pa  # noqa: E402
from simulate_image import load_image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "src", "data")
OUT = os.path.join(ROOT, "site", "public", "compare")
MAX_W = 1400

MODELS = {
    None: None,
    "deuteranopia": pa.MACHADO["deuteranopia"],
    "protanopia": pa.MACHADO["protanopia"],
    "tritanopia": pa.MACHADO["tritanopia"],
    "greyscale": np.array([[0.2126, 0.7152, 0.0722]] * 3),
    "red": np.array([[1.0, 0, 0]] * 3),
}


def simulate(img, m):
    if m is None:
        return img
    lin = pa.srgb_to_linear(np.asarray(img).astype(float))
    return Image.fromarray(np.clip(pa.linear_to_srgb(lin @ m.T), 0, 255).astype(np.uint8))


REAL = os.path.join(ROOT, "docs", "visuals", "real")
SCENARIOS = os.path.join(ROOT, "tools", "screenshots", "scenarios.json")


def discover_real():
    """Live-tile captures from tools/screenshots/compare.mjs become comparisons.

    Each docs/visuals/real/<scenario>/none.png is a side-by-side capture
    (LINZ left, accessible right, 2 CSS px gap at 2x). Split into two variants.
    Written to real-comparisons.json so the site can list them.
    """
    meta = {s["id"]: s for s in json.load(open(SCENARIOS))}
    out = []
    for sid in sorted(os.listdir(REAL)) if os.path.isdir(REAL) else []:
        src = os.path.join(REAL, sid, "none.png")
        if not os.path.exists(src):
            continue
        w, h = Image.open(src).size
        half, gap = w // 2, 2
        rel = os.path.relpath(src, ROOT)
        m = meta.get(sid, {})
        out.append({
            "id": f"real-{sid}", "title": sid.replace("-", " ").capitalize() + " (live LINZ tiles)",
            "summary": m.get("why", "Live-tile capture."),
            "attribution": "Basemap tiles: Toitū Te Whenua LINZ, CC BY 4.0. Left: LINZ topographic-v2. Right: accessible-v0.",
            "variants": [{"label": "LINZ topographic-v2", "src": rel, "crop": [0, 0, half - gap, h]},
                         {"label": "accessible-v0", "src": rel, "crop": [half + gap, 0, w, h]}],
            "links": ["R-03", "R-04", "R-05", "R-07"],
        })
    json.dump(out, open(os.path.join(DATA, "real-comparisons.json"), "w"), indent=1, ensure_ascii=False)
    return out


def main():
    comps = json.load(open(os.path.join(DATA, "comparisons.json"))) + discover_real()
    conds = json.load(open(os.path.join(DATA, "conditions.json")))
    index = {}
    for c in comps:
        d = os.path.join(OUT, c["id"])
        os.makedirs(d, exist_ok=True)
        index[c["id"]] = []
        for i, v in enumerate(c["variants"]):
            img = load_image(os.path.join(ROOT, v["src"]))
            if v.get("crop"):  # [x0, y0, x1, y1] in source pixels
                img = img.crop(tuple(v["crop"]))
            if img.width > MAX_W:
                img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
            files = {}
            for cond in conds:
                name = f"{i}-{cond['id']}.webp"
                # lossless: lossy compression would smear exactly the fine lines we're judging
                simulate(img, MODELS[cond["model"]]).save(os.path.join(d, name), "WEBP", lossless=True, quality=80)
                files[cond["id"]] = f"compare/{c['id']}/{name}"
            index[c["id"]].append({"width": img.width, "height": img.height, "files": files})
        print("built", c["id"])
    json.dump(index, open(os.path.join(DATA, "compare-assets.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
