import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.category_symbol import category_symbol
from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option


def _empty_dd(parent):
    dd = ET.SubElement(parent, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(root, "Option", {"name": "properties"})
    ET.SubElement(
        root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )


def _scrub_dots(style=None):
    """A denser plant grid than scattered scrub. Scattered already uses third_arc at 5 mm."""
    style = style or STYLE
    dots = style["vegetation"]["scrub_dots"]
    ink = rgba(dots["colour"], 255)
    dist = str(dots["distance_mm"])
    layer = ET.Element(
        "layer",
        {
            "class": "PointPatternFill",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    for name, value, kind in (
        ("angle", "0", "double"),
        ("clip_mode", "centroid_within", "QString"),
        ("coordinate_reference", "feature", "QString"),
        ("displacement_x", "0", "QString"),
        ("displacement_x_unit", "MM", "QString"),
        ("displacement_y", "0", "QString"),
        ("displacement_y_unit", "MM", "QString"),
        ("distance_x", dist, "QString"),
        ("distance_x_unit", "MM", "QString"),
        ("distance_y", dist, "QString"),
        ("distance_y_unit", "MM", "QString"),
        ("offset_x", "0", "QString"),
        ("offset_x_unit", "MM", "QString"),
        ("offset_y", "0", "QString"),
        ("offset_y_unit", "MM", "QString"),
    ):
        ET.SubElement(options, "Option", {"name": name, "type": kind, "value": value})
    _empty_dd(layer)
    symbol = ET.SubElement(
        layer,
        "symbol",
        {
            "alpha": "1",
            "clip_to_extent": "1",
            "force_rhr": "0",
            "frame_rate": "10",
            "is_animated": "0",
            "name": "@scrub",
            "type": "marker",
        },
    )
    _empty_dd(symbol)
    marker = ET.SubElement(
        symbol,
        "layer",
        {
            "class": "SimpleMarker",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    marker_opt = ET.SubElement(marker, "Option", {"type": "Map"})
    for name, value in (
        ("angle", "0"),
        ("cap_style", "square"),
        ("color", ink),
        ("horizontal_anchor_point", "1"),
        ("joinstyle", "bevel"),
        ("name", dots["marker"]),
        ("offset", "0,0"),
        ("offset_unit", "MM"),
        ("outline_color", ink),
        ("outline_style", "solid"),
        ("outline_width", str(dots["stroke_mm"])),
        ("outline_width_unit", "MM"),
        ("scale_method", "diameter"),
        ("size", str(dots["size_mm"])),
        ("size_unit", "MM"),
        ("vertical_anchor_point", "1"),
    ):
        ET.SubElement(
            marker_opt, "Option", {"name": name, "type": "QString", "value": value}
        )
    _empty_dd(marker)
    return layer


def _sync_scrub_dots(pattern, style):
    dots = style["vegetation"]["scrub_dots"]
    dist = str(dots["distance_mm"])
    ink = rgba(dots["colour"], 255)
    set_option(pattern, "distance_x", dist)
    set_option(pattern, "distance_y", dist)
    set_option(pattern, "clip_mode", "centroid_within")
    simple = pattern.find("symbol/layer[@class='SimpleMarker']")
    if simple is None:
        raise RuntimeError("scrub dots have no marker")
    set_option(simple, "name", dots["marker"])
    set_option(simple, "size", str(dots["size_mm"]))
    set_option(simple, "color", ink)
    set_option(simple, "outline_color", ink)
    set_option(simple, "outline_width", str(dots["stroke_mm"]))


def patch_vegetation(layer, style=None):
    style = style or STYLE
    native_ink = style["vegetation"]["native"]
    scrub_ink = style["vegetation"]["scrub"]
    native = category_symbol(layer, "native")
    scrub = category_symbol(layer, "scrub")
    native_fill = native.find("layer[@class='SimpleFill']")
    scrub_fill = scrub.find("layer[@class='SimpleFill']")
    set_option(native_fill, "color", rgba(native_ink["colour"], native_ink["alpha"]))
    set_option(scrub_fill, "color", rgba(scrub_ink["colour"], scrub_ink["alpha"]))
    _paint_native_marker(native, style)
    # Colour alone does not separate these fills in greyscale (R-10).
    # Scattered scrub keeps its stock dots. Scrub gets a denser plant grid.
    for hatch in list(scrub.findall("layer[@class='LinePatternFill']")):
        scrub.remove(hatch)
    existing = scrub.find("layer[@class='PointPatternFill']")
    if existing is None:
        scrub.insert(0, _scrub_dots(style))
    else:
        _sync_scrub_dots(existing, style)


MARKER_CLASSES = (
    "PointPatternFill",
    "CentroidFill",
    "SimpleMarker",
    "FontMarker",
    "SvgMarker",
)


def _paint_native_marker(native, style):
    marker = style["vegetation"]["native"].get("marker")
    if not marker:
        return
    ink = rgba(marker["colour"], 255)
    for layer in native.findall(".//layer"):
        if layer.get("class") not in MARKER_CLASSES:
            continue
        option = layer.find("Option")
        if option is None:
            continue
        for name in ("color", "outline_color"):
            child = option.find(f"Option[@name='{name}']")
            if child is not None:
                child.set("value", ink)
