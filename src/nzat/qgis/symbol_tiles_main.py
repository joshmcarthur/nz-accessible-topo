import argparse
import json
import os
import sys

from nzat.qgis.font_files import font_files
from nzat.qgis.legend_box_extent import legend_box_extent
from nzat.qgis.legend_metres_per_px import legend_metres_per_px
from nzat.qgis.legend_swatches import LEGEND_DPI, SWATCHES
from nzat.qgis.open_map import open_map
from nzat.qgis.qgis_prefix import qgis_prefix
from nzat.qgis.render_image import render_image
from nzat.qgis.swatch_layers import swatch_layers
from nzat.qgis.symbol_tile_scenes import (
    ALONE_SUFFIX,
    CONFLICTS,
    TILE_PX,
    conflict_alone,
    tile_box,
    tile_scenes,
)

MANIFEST_FILE = "tiles.json"


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    parser = argparse.ArgumentParser(
        description="Draw each legend symbol on each fill and across each conflict."
    )
    parser.add_argument("--project", required=True, help="Applied or stock .qgs file")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument(
        "--font",
        action="append",
        default=[],
        help="A font file or a directory of .otf and .ttf files",
    )
    parser.add_argument("--theme", default="Map5View-all", help="QGIS map theme")
    parser.add_argument(
        "--key",
        action="append",
        default=[],
        help="Draw only this swatch key. Repeat for more. The default is all",
    )
    args = parser.parse_args()

    # QGIS is installed in the map container only. A top-level import fails on the host.
    from qgis.core import QgsApplication  # noqa: E402
    from qgis.PyQt.QtGui import QImage, QPainter  # noqa: E402

    swatches = [s for s in SWATCHES if not args.key or s["key"] in args.key]
    missing = set(args.key) - {s["key"] for s in swatches}
    if missing:
        print(f"no swatch for {sorted(missing)}", file=sys.stderr)
        return 1

    QgsApplication.setPrefixPath(qgis_prefix(os.environ.get("QGIS_PREFIX_PATH")), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        try:
            session = open_map(args.project, font_files(args.font), args.theme)
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 1
        session = {**session, "hillshade": False}
        metres_per_px = legend_metres_per_px(LEGEND_DPI)
        manifest = {}
        for swatch in swatches:
            key = swatch["key"]
            scenes = tile_scenes(swatch)
            os.makedirs(os.path.join(args.out, key), exist_ok=True)
            xmin, ymin, xmax, ymax, w, h = legend_box_extent(
                tile_box(swatch["box"]), metres_per_px
            )
            strip = QImage(TILE_PX * len(scenes), TILE_PX, QImage.Format.Format_RGB888)
            painter = QPainter(strip)
            try:
                for column, (name, features) in enumerate(scenes):
                    layers = swatch_layers(
                        session["layers"],
                        features,
                        metres_per_px,
                        labels=swatch.get("labels", True),
                    )
                    image = render_image(
                        {**session, "layers": layers},
                        xmin,
                        ymin,
                        xmax,
                        ymax,
                        w,
                        h,
                        LEGEND_DPI,
                    )
                    path = os.path.join(args.out, key, f"{name}.png")
                    if image.isNull() or not image.save(path):
                        print(f"tile {key} {name} did not draw", file=sys.stderr)
                        return 1
                    painter.drawImage(column * TILE_PX, 0, image)
                    if name in CONFLICTS:
                        # The score needs to know which pixels the other class
                        # inks, so a black name on a black mark is not a pass.
                        alone = render_image(
                            {
                                **session,
                                "layers": swatch_layers(
                                    session["layers"],
                                    conflict_alone(name, tile_box(swatch["box"])),
                                    metres_per_px,
                                ),
                            },
                            xmin,
                            ymin,
                            xmax,
                            ymax,
                            w,
                            h,
                            LEGEND_DPI,
                        )
                        alone_path = os.path.join(
                            args.out, key, f"{name}{ALONE_SUFFIX}.png"
                        )
                        if alone.isNull() or not alone.save(alone_path):
                            print(
                                f"tile {key} {name} alone did not draw", file=sys.stderr
                            )
                            return 1
            finally:
                painter.end()
            if not strip.save(os.path.join(args.out, f"{key}.png")):
                print(f"strip {key} not written", file=sys.stderr)
                return 1
            manifest[key] = [name for name, _features in scenes]
            print(f"tiles {key} scenes {len(scenes)}")
        with open(
            os.path.join(args.out, MANIFEST_FILE), "w", encoding="utf-8"
        ) as handle:
            json.dump(manifest, handle, indent=1)
            handle.write("\n")
        print(f"wrote {os.path.join(args.out, MANIFEST_FILE)}")
    finally:
        qgs.exitQgis()
    return 0
