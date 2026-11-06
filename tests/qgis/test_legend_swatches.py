import re
import xml.etree.ElementTree as ET

from nzat.qgis.legend_box_extent import legend_box_extent
from nzat.qgis.legend_metres_per_px import legend_metres_per_px
from nzat.qgis.legend_swatches import LEGEND_DPI, LEGEND_SIZE, SWATCHES
from nzat.qgis.legend_wkt import legend_wkt
from nzat.qgis.patch_legend_picture import patch_legend_picture
from nzat.qgis.render_legend_main import known_swatch_attrs
from nzat.site.symbol_rows import SYMBOLS

# Stock legend boxes share a few pixels between rows. That is not a wiped symbol.
ROW_BLEED_PX = 16
PAINTED_PROPOSED = frozenset({"fumarole", "marine_farm", "waterfall"})


def _overlap_wh(a, b):
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    return dx, dy


def _contained(inner, outer):
    return (
        outer[0] <= inner[0]
        and inner[2] <= outer[2]
        and outer[1] <= inner[1]
        and inner[3] <= outer[3]
    )


def test_unknown_swatch_attrs_are_skipped():
    # Catches a KeyError when a swatch sets feature_type on a layer that has only type.
    assert known_swatch_attrs(
        {"type", "status"}, {"type": "gate", "feature_type": "gate"}
    ) == {"type": "gate"}


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
    for i, left in enumerate(SWATCHES):
        for right in SWATCHES[i + 1 :]:
            dx, dy = _overlap_wh(left["box"], right["box"])
            assert not (dx > ROW_BLEED_PX and dy > ROW_BLEED_PX), (
                left["key"],
                right["key"],
            )
    for swatch in SWATCHES:
        x0, y0, x1, y1 = swatch["box"]
        assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height
        for _table, _attrs, wkt in swatch["features"]:
            numbers = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", wkt)]
            for x, y in zip(numbers[::2], numbers[1::2], strict=True):
                assert x0 <= x <= x1, swatch["key"]
                assert y0 <= y <= y1, swatch["key"]


def test_swatches_do_not_wipe_stock_rows():
    # Catches a swatch that clears a blocked row, or a proposed row with no sample.
    leave = [
        symbol
        for symbol in SYMBOLS
        if symbol["box"]
        and (
            symbol["status"] == "blocked"
            or (
                symbol["status"] == "proposed" and symbol["key"] not in PAINTED_PROPOSED
            )
        )
    ]
    for symbol in leave:
        for swatch in SWATCHES:
            dx, dy = _overlap_wh(swatch["box"], symbol["box"])
            assert not (dx > ROW_BLEED_PX and dy > ROW_BLEED_PX), (
                swatch["key"],
                symbol["key"],
            )


def test_group_swatch_is_union_of_drawable_boxes():
    # Catches a group box that extends onto a stock row we cannot redraw.
    by_key = {symbol["key"]: symbol for symbol in SYMBOLS if symbol["box"]}
    drawable = [
        symbol["box"]
        for symbol in SYMBOLS
        if symbol["box"]
        and (
            symbol["status"] == "done"
            or symbol["key"] in PAINTED_PROPOSED
            or symbol["redrawn"]
        )
    ]
    for swatch in SWATCHES:
        if swatch["key"] in by_key:
            continue
        inside = [box for box in drawable if _contained(box, swatch["box"])]
        assert inside, swatch["key"]
        union = (
            min(box[0] for box in inside),
            min(box[1] for box in inside),
            max(box[2] for box in inside),
            max(box[3] for box in inside),
        )
        assert swatch["box"] == union, swatch["key"]


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
