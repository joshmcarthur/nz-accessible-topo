import json
import os

from PIL import Image

from nzat.colour.apply_matrix import GREYSCALE, RED_HEADTORCH, apply_matrix
from nzat.colour.simulate import MACHADO
from nzat.paths import ROOT
from nzat.render.load_image import load_image

DATA = ROOT / "site" / "src" / "data"
OUT = ROOT / "site" / "public" / "compare"
MAX_W = 1400
REAL = ROOT / "docs" / "visuals" / "real"
SCENARIOS = ROOT / "tools" / "screenshots" / "scenarios.json"

MODELS = {
    None: None,
    "deuteranopia": MACHADO["deuteranopia"],
    "protanopia": MACHADO["protanopia"],
    "tritanopia": MACHADO["tritanopia"],
    "greyscale": GREYSCALE,
    "red": RED_HEADTORCH,
}


def _discover_real():
    """Live-tile captures from tools/screenshots/compare.mjs become comparisons."""
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
        out.append(
            {
                "id": f"real-{sid}",
                "title": sid.replace("-", " ").capitalize() + " (live LINZ tiles)",
                "summary": m.get("why", "Live-tile capture."),
                "attribution": (
                    "Basemap tiles: Toitū Te Whenua LINZ, CC BY 4.0. "
                    "Left: LINZ topographic-v2. Right: accessible-v0."
                ),
                "variants": [
                    {
                        "label": "LINZ topographic-v2",
                        "src": rel,
                        "crop": [0, 0, half - gap, h],
                    },
                    {
                        "label": "accessible-v0",
                        "src": rel,
                        "crop": [half + gap, 0, w, h],
                    },
                ],
                "links": ["R-03", "R-04", "R-05", "R-07"],
            }
        )
    json.dump(
        out,
        open(os.path.join(DATA, "real-comparisons.json"), "w"),
        indent=1,
        ensure_ascii=False,
    )
    return out


def main():
    comps = json.load(open(os.path.join(DATA, "comparisons.json"))) + _discover_real()
    conds = json.load(open(os.path.join(DATA, "conditions.json")))
    index = {}
    for c in comps:
        d = os.path.join(OUT, c["id"])
        os.makedirs(d, exist_ok=True)
        index[c["id"]] = []
        for i, v in enumerate(c["variants"]):
            img = load_image(os.path.join(ROOT, v["src"]))
            if v.get("crop"):
                img = img.crop(tuple(v["crop"]))
            if img.width > MAX_W:
                img = img.resize(
                    (MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS
                )
            files = {}
            lossless = not c.get("lossy")
            for cond in conds:
                name = f"{i}-{cond['id']}.webp"
                apply_matrix(img, MODELS[cond["model"]]).save(
                    os.path.join(d, name), "WEBP", lossless=lossless, quality=80
                )
                files[cond["id"]] = f"compare/{c['id']}/{name}"
            index[c["id"]].append(
                {"width": img.width, "height": img.height, "files": files}
            )
        print("built", c["id"])
    json.dump(index, open(os.path.join(DATA, "compare-assets.json"), "w"), indent=1)
