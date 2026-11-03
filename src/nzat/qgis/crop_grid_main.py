import argparse
import json
import os
import sys

from PIL import Image

from nzat.qgis.crop_face import crop_face
from nzat.qgis.parse_extent import parse_extent
from nzat.qgis.sample_grid import (
    BX24_EXTENT,
    CELL_M,
    CELL_PX,
    PHASE,
    chequerboard,
    crop_name,
    face_pixels,
    grid_cells,
    grid_shape,
)


def _extent_text(extent):
    return ",".join(str(int(part) if part == int(part) else part) for part in extent)


def main():
    parser = argparse.ArgumentParser(
        description="Crop a 4 km chequerboard from stock and accessible BX24 faces."
    )
    parser.add_argument("--stock", required=True, help="Path to the stock face PNG")
    parser.add_argument(
        "--accessible", required=True, help="Path to the accessible face PNG"
    )
    parser.add_argument("--out", required=True, help="Directory for the cropped PNGs")
    parser.add_argument(
        "--extent",
        default=_extent_text(BX24_EXTENT),
        help="xmin,ymin,xmax,ymax in NZTM",
    )
    parser.add_argument("--cell-m", type=int, default=CELL_M)
    parser.add_argument("--cell-px", type=int, default=CELL_PX)
    parser.add_argument(
        "--phase",
        type=int,
        default=PHASE,
        help="Keep cells whose column plus row modulo 2 equals this value",
    )
    args = parser.parse_args()

    try:
        extent = parse_extent(args.extent)
        cols, rows = grid_shape(extent, args.cell_m)
        cells = chequerboard(grid_cells(extent, args.cell_m), args.phase)
        width, height = face_pixels(cols, rows, args.cell_px)
        stock_paths = crop_face(
            Image.open(args.stock).convert("RGB"),
            cells,
            args.cell_px,
            cols,
            rows,
            "stock",
            args.out,
        )
        accessible_paths = crop_face(
            Image.open(args.accessible).convert("RGB"),
            cells,
            args.cell_px,
            cols,
            rows,
            "accessible",
            args.out,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    manifest = {
        "extent": list(extent),
        "cell_m": args.cell_m,
        "cell_px": args.cell_px,
        "face_px": [width, height],
        "phase": args.phase,
        "cells": [
            {
                "col": col,
                "row": row,
                "east": east,
                "north": north,
                "stock": crop_name(east, north, "stock"),
                "accessible": crop_name(east, north, "accessible"),
            }
            for col, row, east, north in cells
        ],
    }
    os.makedirs(args.out, exist_ok=True)
    manifest_path = os.path.join(args.out, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    print(f"wrote {len(stock_paths)} stock crops")
    print(f"wrote {len(accessible_paths)} accessible crops")
    print(f"wrote {manifest_path}")
    return 0
