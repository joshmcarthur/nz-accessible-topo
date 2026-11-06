import re
import xml.etree.ElementTree as ET

from nzat.qgis.legend_box_extent import legend_box_extent
from nzat.qgis.legend_metres_per_px import legend_metres_per_px
from nzat.qgis.legend_swatches import LEGEND_DPI, LEGEND_SIZE, SWATCHES
from nzat.qgis.legend_wkt import legend_wkt
from nzat.qgis.patch_legend_picture import patch_legend_picture
from nzat.site.symbol_rows import SYMBOLS


def test_swatches_draw_at_sheet_size():
    # Catches a swatch drawn at a scale other than the 1:50,000 sheet, or a y axis left pointing down.
    metres = legend_metres_per_px(LEGEND_DPI)
    assert round(600 * metres, 6) == 1270
    assert legend_wkt("LINESTRING (10 20.5, 600 300)", 2) == (
        "LINESTRING (20.0000 -41.0000, 1200.0000 -600.0000)"
    )
    assert legend_box_extent((10, 20, 40, 60), 2) == (20, -120, 80, -40, 30, 40)


def test_swatch_features_sit_in_their_boxes():
    # Catches a feature outside its box, which would not draw, and two boxes that overlap, where one would wipe the other.
    width, height = LEGEND_SIZE
    boxes = sorted(swatch["box"] for swatch in SWATCHES)
    for (_, _, _, y1), (_, y0, _, _) in zip(boxes, boxes[1:], strict=False):
        assert y1 <= y0
    for swatch in SWATCHES:
        x0, y0, x1, y1 = swatch["box"]
        assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height
        for _table, _attrs, wkt in swatch["features"]:
            numbers = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", wkt)]
            for x, y in zip(numbers[::2], numbers[1::2], strict=True):
                assert x0 <= x <= x1, swatch["key"]
                assert y0 <= y <= y1, swatch["key"]


def test_swatch_boxes_match_symbol_rows():
    # Catches a swatch box that drifted from symbol_rows (some rows share one swatch).
    by_key = {symbol["key"]: symbol for symbol in SYMBOLS if symbol["box"]}
    for swatch in SWATCHES:
        symbol = by_key.get(swatch["key"])
        if symbol is None:
            continue
        assert swatch["box"] == symbol["box"], swatch["key"]


def test_layout_legend_picture_points_at_the_accessible_legend():
    # Catches the accessible page left on the stock legend image, or a logo picture moved by mistake.
    root = ET.fromstring(
        """
        <qgis><Layouts><Layout name="tiff-50">
          <LayoutItem type="65640" file="./topo-legend-1.tif"/>
          <LayoutItem type="65640" file="./linz_logo_main_2022.png"/>
          <LayoutItem type="65641" file="./topo-legend-1.tif"/>
        </Layout></Layouts></qgis>
        """
    )
    assert patch_legend_picture(root) == 1
    assert patch_legend_picture(root) == 1
    files = [item.get("file") for item in root.iter("LayoutItem")]
    assert files == [
        "./topo-legend-accessible.png",
        "./linz_logo_main_2022.png",
        "./topo-legend-1.tif",
    ]
