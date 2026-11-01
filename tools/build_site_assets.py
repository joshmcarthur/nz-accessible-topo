#!/usr/bin/env python3
"""
build_site_assets.py — pre-render every comparison variant under every condition.

Reads site/src/data/comparisons.json and conditions.json; writes
site/public/compare/<comparison>/<variant-index>-<condition>.webp plus
site/src/data/compare-assets.json (sizes, for layout without shift).

Same models as tools/palette_audit.py, so the site shows exactly what the
audits measure. Adding a comparison = adding an entry to comparisons.json.
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


def main():
    comps = json.load(open(os.path.join(DATA, "comparisons.json")))
    conds = json.load(open(os.path.join(DATA, "conditions.json")))
    index = {}
    for c in comps:
        d = os.path.join(OUT, c["id"])
        os.makedirs(d, exist_ok=True)
        index[c["id"]] = []
        for i, v in enumerate(c["variants"]):
            img = load_image(os.path.join(ROOT, v["src"]))
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
