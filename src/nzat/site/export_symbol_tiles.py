"""Score the symbol test tiles and write the table the site reads."""

import argparse
import json
from pathlib import Path

from PIL import Image

from nzat.paths import ROOT
from nzat.qgis.symbol_tile_scenes import CONFLICTS
from nzat.render.tile_visibility import (
    CONDITIONS,
    CONTRAST_FLOOR,
    DELTA_E_FLOOR,
    visible_fractions,
)

TILES_DIR = ROOT / "render" / "symbol-tiles"
TABLE_PATH = ROOT / "site" / "src" / "data" / "symbol-tiles.json"
# Our own floor: under half of the ink left counts as a fail. Grade D.
VISIBLE_FLOOR = 0.5


def score_rows(tiles_dir, manifest):
    """Return one row per swatch key that has ink and ground around it."""
    rows = []
    for key, scenes in manifest.items():
        paper = Image.open(tiles_dir / key / "paper.png")
        scored = []
        for scene in scenes:
            tile = Image.open(tiles_dir / key / f"{scene}.png")
            visible = visible_fractions(paper, tile, scene in CONFLICTS)
            if visible is None:
                break
            scored.append(
                {
                    "scene": scene,
                    "kind": "conflict" if scene in CONFLICTS else "fill",
                    "visible": visible,
                    "fails": [c for c, v in visible.items() if v < VISIBLE_FLOOR],
                }
            )
        else:
            rows.append({"key": key, "scenes": scored})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tiles", default=str(TILES_DIR), help="Tile directory")
    args = parser.parse_args()
    tiles_dir = Path(args.tiles)
    with open(tiles_dir / "tiles.json", encoding="utf-8") as handle:
        manifest = json.load(handle)
    rows = score_rows(tiles_dir, manifest)
    table = {
        "conditions": list(CONDITIONS),
        "floors": {
            "contrast": CONTRAST_FLOOR,
            "delta_e": DELTA_E_FLOOR,
            "visible": VISIBLE_FLOOR,
        },
        "symbols": rows,
    }
    with open(TABLE_PATH, "w", encoding="utf-8") as handle:
        json.dump(table, handle, indent=1)
        handle.write("\n")
    fails = sum(1 for row in rows for scene in row["scenes"] if scene["fails"])
    total = sum(len(row["scenes"]) for row in rows)
    print(f"wrote {TABLE_PATH}: {len(rows)} symbols, {total} tiles, {fails} fail")
