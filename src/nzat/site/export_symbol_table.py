"""Build the site symbol table: crops of each LINZ legend swatch and our checks.

Needs local inputs outside the repo, so CI does not run it. Commit its outputs:
site/src/data/symbols.json and site/public/symbols/*.png.
"""

import json
import os
from pathlib import Path

from PIL import Image

from nzat.paths import ROOT
from nzat.qgis.cover_set import map_paint_note, map_png_name, paints_on_map_all
from nzat.qgis.legend_swatches import ACCESSIBLE_LEGEND_FILE, LEGEND_SIZE
from nzat.qgis.symbol_queries import queries_by_key
from nzat.site.symbol_checks import (
    GRAPHIC_FLOOR,
    LINE_FLOOR_MM,
    MARK_FLOOR_MM,
    RED_FLOOR,
    evaluate,
    measure_pair,
    passes,
)
from nzat.site.symbol_rows import EXCLUDED, SECTIONS, STATUSES, SYMBOLS

DATA_PATH = ROOT / "site" / "src" / "data" / "symbols.json"
IMAGE_DIR = ROOT / "site" / "public" / "symbols"
PROJECTS = Path.home() / "Projects" / "github.com" / "linz"
STOCK_LEGEND = PROJECTS / "topographic-system" / "e2e" / "assets" / "topo-legend-1.tif"
ACCESSIBLE_LEGEND = (
    PROJECTS / "topo50-bx24" / "squares" / "accessible" / ACCESSIBLE_LEGEND_FILE
)


def _read_stock(path):
    import tifffile

    return Image.fromarray(tifffile.imread(path)[..., :3])


def _ink_rows(inks):
    rows = []
    for item in inks:
        m = measure_pair(item["hex"], item.get("on") or "#FFFFFF")
        rows.append({**item, **m})
    return rows


def _side(spec, merged_with=None):
    if spec is None:
        return None
    checks = evaluate(spec, merged_with)
    return {
        "text": spec["text"],
        "source": spec["source"],
        "inks": _ink_rows(spec["inks"]),
        "checks": checks,
        "pass": passes(checks),
    }


def symbol_row(symbol):
    parquet = queries_by_key()[symbol["key"]]["parquet"]
    map_name = map_png_name(symbol["key"])
    show_map = paints_on_map_all(parquet) and (IMAGE_DIR / map_name).is_file()
    return {
        "key": symbol["key"],
        "section": symbol["section"],
        "label": symbol["label"],
        "layer": symbol["layer"],
        "drawn": symbol["drawn"],
        "status": symbol["status"],
        "note": symbol["note"],
        "linz_image": f"symbols/{symbol['key']}-linz.png" if symbol["box"] else None,
        "current_image": (
            f"symbols/{symbol['key']}-ours.png" if symbol["redrawn"] else None
        ),
        "map_image": f"symbols/{map_name}" if show_map else None,
        "map_note": map_paint_note(parquet),
        "measured": _side(symbol["measured"], symbol["merged_with"]),
        "proposal": _side(symbol["proposal"]),
    }


def build_table():
    rows = [symbol_row(symbol) for symbol in SYMBOLS]
    counts = {status: 0 for status in STATUSES}
    for row in rows:
        counts[row["status"]] += 1
    return {
        "source_rows": "src/nzat/site/symbol_rows.py",
        "floors": {
            "contrast": GRAPHIC_FLOOR,
            "red": RED_FLOOR,
            "line_mm": LINE_FLOOR_MM,
            "mark_mm": MARK_FLOOR_MM,
        },
        "counts": counts,
        "excluded": list(EXCLUDED),
        "sections": [
            {"name": name, "rows": [r for r in rows if r["section"] == name]}
            for name in SECTIONS
        ],
    }


def clear_legend_crops(image_dir):
    """Drop legend-box crops. Keep in-situ `{key}-map.png` files."""
    for pattern in ("*-linz.png", "*-ours.png"):
        for old in Path(image_dir).glob(pattern):
            old.unlink()


def write_crops():
    stock = _read_stock(STOCK_LEGEND)
    ours = Image.open(ACCESSIBLE_LEGEND).convert("RGB")
    if stock.size != LEGEND_SIZE or ours.size != LEGEND_SIZE:
        raise SystemExit(f"legend images must be {LEGEND_SIZE}")
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    clear_legend_crops(IMAGE_DIR)
    for symbol in SYMBOLS:
        if not symbol["box"]:
            continue
        stock.crop(symbol["box"]).save(IMAGE_DIR / f"{symbol['key']}-linz.png")
        if symbol["redrawn"]:
            ours.crop(symbol["box"]).save(IMAGE_DIR / f"{symbol['key']}-ours.png")


def main():
    write_crops()
    payload = build_table()
    DATA_PATH.write_text(
        json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"{len(SYMBOLS)} symbols: "
        + ", ".join(f"{k} {v}" for k, v in payload["counts"].items())
        + f". Images in {os.path.relpath(IMAGE_DIR, ROOT)}"
    )
