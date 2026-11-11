"""Turn sheet GeoTIFFs into one PMTiles archive of web map tiles.

The sheet rasters come from tools/render_sheets.py (EPSG:2193). GDAL warps
them to web mercator tiles in an MBTiles file and builds the lower zooms.
The pmtiles CLI turns that into one file a static site can serve.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

OVERVIEWS = ("2", "4", "8", "16", "32")


def tile_commands(inputs, out, work, extent=None, quality=80):
    """Return the commands that build `out` from the input GeoTIFFs, in order.

    `extent` is west, south, east, north in NZTM metres. `work` is a folder
    for the mosaic and the MBTiles file.
    """
    work = Path(work)
    mosaic = work / "mosaic.vrt"
    mbtiles = work / "tiles.mbtiles"
    translate = [
        "gdal_translate",
        "-q",
        "-of",
        "MBTILES",
        "-co",
        "TILE_FORMAT=WEBP",
        "-co",
        f"QUALITY={quality}",
        # The top zoom is the first one finer than the sheet pixels.
        "-co",
        "ZOOM_LEVEL_STRATEGY=UPPER",
        "-co",
        "RESAMPLING=CUBIC",
    ]
    if extent is not None:
        west, south, east, north = extent
        translate += ["-projwin", str(west), str(north), str(east), str(south)]
    return [
        ["gdalbuildvrt", "-q", str(mosaic), *[str(path) for path in inputs]],
        [*translate, str(mosaic), str(mbtiles)],
        ["gdaladdo", "-q", "-r", "average", str(mbtiles), *OVERVIEWS],
        ["pmtiles", "convert", str(mbtiles), str(out)],
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Sheet GeoTIFFs in EPSG:2193")
    parser.add_argument("--out", required=True, help="Output .pmtiles file")
    parser.add_argument(
        "--extent", help="west,south,east,north in NZTM metres. The default is all"
    )
    parser.add_argument("--quality", type=int, default=80, help="WebP quality")
    args = parser.parse_args()
    extent = None
    if args.extent:
        extent = [float(part) for part in args.extent.split(",")]
        if len(extent) != 4:
            print("--extent needs west,south,east,north", file=sys.stderr)
            return 1
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as work:
        for command in tile_commands(args.inputs, out, work, extent, args.quality):
            done = subprocess.run(command, capture_output=True, text=True)
            if done.returncode != 0:
                print(f"{command[0]} failed: {done.stderr.strip()}", file=sys.stderr)
                return 1
    print(f"wrote {out} {out.stat().st_size} bytes")
    return 0
