import argparse
import os
import sys

from nzat.qgis.font_files import font_files
from nzat.qgis.legend_box_extent import legend_box_extent
from nzat.qgis.legend_metres_per_px import legend_metres_per_px
from nzat.qgis.legend_swatches import (
    ACCESSIBLE_LEGEND_FILE,
    LEGEND_DPI,
    LEGEND_SIZE,
    SWATCHES,
)
from nzat.qgis.map_layers import SHEET_PRESET
from nzat.qgis.open_map import open_map
from nzat.qgis.qgis_prefix import qgis_prefix
from nzat.qgis.render_image import render_image
from nzat.qgis.swatch_layers import swatch_layers
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    parser = argparse.ArgumentParser(
        description="Draw the applied map symbols over the stock Topo50 legend image."
    )
    parser.add_argument("--project", required=True, help="Applied .qgs file")
    parser.add_argument("--stock-legend", required=True, help="Stock topo-legend-1.tif")
    parser.add_argument(
        "--font",
        action="append",
        default=[],
        help="A font file or a directory of .otf and .ttf files",
    )
    parser.add_argument(
        "--output",
        help=f"Output PNG. The default is {ACCESSIBLE_LEGEND_FILE} beside the project",
    )
    parser.add_argument(
        "--theme",
        default=SHEET_PRESET,
        help="QGIS map theme. Map5View-all draws hidden layers into swatches.",
    )
    args = parser.parse_args()
    output = args.output or os.path.join(
        os.path.dirname(os.path.abspath(args.project)), ACCESSIBLE_LEGEND_FILE
    )

    # QGIS is installed in the map container only. A top-level import fails on the host.
    from osgeo import gdal  # noqa: E402
    from qgis.core import QgsApplication  # noqa: E402
    from qgis.PyQt.QtGui import QImage, QPainter  # noqa: E402

    QgsApplication.setPrefixPath(qgis_prefix(os.environ.get("QGIS_PREFIX_PATH")), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        # Qt does not read the WEBP-compressed stock TIFF. GDAL does.
        stock = gdal.Open(args.stock_legend)
        if stock is None or stock.RasterCount < 3:
            print(f"cannot read {args.stock_legend}", file=sys.stderr)
            return 1
        size = (stock.RasterXSize, stock.RasterYSize)
        if size != LEGEND_SIZE:
            print(f"stock legend is {size}, expected {LEGEND_SIZE}", file=sys.stderr)
            return 1
        pixels = (
            stock.ReadAsArray(band_list=[1, 2, 3]).transpose(1, 2, 0).copy(order="C")
        )
        width, height = size
        legend = QImage(
            pixels.data, width, height, width * 3, QImage.Format.Format_RGB888
        ).copy()
        try:
            session = open_map(args.project, font_files(args.font), args.theme)
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 1
        session = {**session, "hillshade": False}
        metres_per_px = legend_metres_per_px(LEGEND_DPI)
        style_rules = load_rules()
        painter = QPainter(legend)
        try:
            for swatch in SWATCHES:
                if swatch.get("tiles_only"):
                    continue
                marker_size_mm = None
                size_path = swatch.get("legend_marker_size_mm")
                if size_path:
                    marker_size_mm = float(lookup_style_path(style_rules, size_path))
                layers = swatch_layers(
                    session["layers"],
                    swatch["features"],
                    metres_per_px,
                    labels=swatch.get("labels", True),
                    marker_size_mm=marker_size_mm,
                )
                xmin, ymin, xmax, ymax, w, h = legend_box_extent(
                    swatch["box"], metres_per_px
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
                if image.isNull():
                    print(f"swatch {swatch['key']} did not draw", file=sys.stderr)
                    return 1
                painter.drawImage(swatch["box"][0], swatch["box"][1], image)
                print(f"swatch {swatch['key']} layers {len(layers)}")
        finally:
            painter.end()
        legend.setDotsPerMeterX(round(LEGEND_DPI / 0.0254))
        legend.setDotsPerMeterY(round(LEGEND_DPI / 0.0254))
        if not legend.save(output):
            print(f"failed to write {output}", file=sys.stderr)
            return 1
        print(f"wrote {output}")
    finally:
        qgs.exitQgis()
    return 0
