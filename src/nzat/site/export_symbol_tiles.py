"""Score the symbol test tiles and write the table the site reads."""

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image

from nzat.paths import ROOT
from nzat.qgis.legend_swatches import SWATCHES
from nzat.qgis.symbol_tile_scenes import (
    ALONE_SUFFIX,
    CONFLICTS,
    gated_conditions,
    scene_exception,
)
from nzat.render.tile_visibility import (
    ACUITY,
    CONDITIONS,
    CONTRAST_FLOOR,
    DELTA_E_FLOOR,
    covered_share,
    visible_fractions,
)
from nzat.site.symbol_rows import SYMBOLS

TILES_DIR = ROOT / "render" / "symbol-tiles"
TABLE_PATH = ROOT / "site" / "src" / "data" / "symbol-tiles.json"
IMAGE_DIR = ROOT / "site" / "public" / "symbol-tiles"
# Legend rows that hold more than one symbol on the symbol table.
GROUP_LABELS = {
    "poled_route_connector": "Poled route and track connector",
    "sealed": "Sealed road",
    "metalled": "Metalled road",
    "unmetalled": "Unmetalled road",
    "watercourse_drain": "Watercourse and drain",
    "vegetation": "Vegetation fills",
}
# Our own floor: under half of the ink left counts as a fail. Grade D.
VISIBLE_FLOOR = 0.5


def swatch_label(key, symbols=SYMBOLS):
    """Return the symbol-table label for a swatch key."""
    for symbol in symbols:
        if symbol["key"] == key:
            return symbol["label"]
    return GROUP_LABELS[key]


def score_rows(tiles_dir, manifest, swatches=SWATCHES):
    """Return one row per swatch key that has ink and ground around it."""
    features = {swatch["key"]: swatch["features"] for swatch in swatches}
    rows = []
    for key, scenes in manifest.items():
        paper = Image.open(tiles_dir / key / "paper.png")
        gated = gated_conditions(features[key], [*CONDITIONS, ACUITY])
        scored = []
        for scene in scenes:
            tile = Image.open(tiles_dir / key / f"{scene}.png")
            alone = None
            if scene in CONFLICTS:
                alone = Image.open(tiles_dir / key / f"{scene}{ALONE_SUFFIX}.png")
            named = scene == "name"
            visible = visible_fractions(
                paper, tile, scene in CONFLICTS, alone, yields=named
            )
            if visible is None:
                break
            exception = scene_exception(
                key,
                scene,
                features[key],
                visible["normal"],
                covered_share(paper, alone) if named else 0.0,
            )
            fails = [c for c in gated if visible[c] < VISIBLE_FLOOR]
            scored.append(
                {
                    "scene": scene,
                    "kind": "conflict" if scene in CONFLICTS else "fill",
                    "visible": visible,
                    "exception": exception,
                    "fails": [] if exception else fails,
                }
            )
        else:
            rows.append(
                {
                    "key": key,
                    "label": swatch_label(key),
                    "gated": gated,
                    "scenes": scored,
                }
            )
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
        "conditions": [*CONDITIONS, ACUITY],
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
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for row in rows:
        shutil.copyfile(
            tiles_dir / f"{row['key']}.png", IMAGE_DIR / f"{row['key']}.png"
        )
    fails = sum(1 for row in rows for scene in row["scenes"] if scene["fails"])
    total = sum(len(row["scenes"]) for row in rows)
    print(f"wrote {TABLE_PATH}: {len(rows)} symbols, {total} tiles, {fails} fail")
