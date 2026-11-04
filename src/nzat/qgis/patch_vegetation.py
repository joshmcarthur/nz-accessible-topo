import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.category_symbol import category_symbol
from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option


def _scrub_hatch(style=None):
    """Diagonal lines. Scattered scrub already uses a dot pattern."""
    style = style or STYLE
    hatch = style["vegetation"]["scrub_hatch"]
    ink = rgba(hatch["colour"], 255)
    layer = ET.Element(
        "layer",
        {
            "class": "LinePatternFill",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    for name, value, kind in (
        ("angle", str(hatch["angle_deg"]), "QString"),
        ("clip_mode", "during_render", "QString"),
        ("color", ink, "QString"),
        ("coordinate_reference", "feature", "QString"),
        ("distance", str(hatch["distance_mm"]), "QString"),
        ("distance_unit", "MM", "QString"),
        ("line_width", str(hatch["line_width_mm"]), "QString"),
        ("line_width_unit", "MM", "QString"),
        ("offset", "0", "QString"),
        ("offset_unit", "MM", "QString"),
    ):
        ET.SubElement(options, "Option", {"name": name, "type": kind, "value": value})
    dd = ET.SubElement(layer, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(root, "Option", {"name": "properties"})
    ET.SubElement(
        root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )
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
            "type": "line",
        },
    )
    symbol_dd = ET.SubElement(symbol, "data_defined_properties")
    symbol_opt = ET.SubElement(symbol_dd, "Option", {"type": "Map"})
    ET.SubElement(
        symbol_opt, "Option", {"name": "name", "type": "QString", "value": ""}
    )
    ET.SubElement(symbol_opt, "Option", {"name": "properties"})
    ET.SubElement(
        symbol_opt, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )
    line = ET.SubElement(
        symbol,
        "layer",
        {
            "class": "SimpleLine",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    line_opt = ET.SubElement(line, "Option", {"type": "Map"})
    for name, value in (
        ("capstyle", "square"),
        ("joinstyle", "bevel"),
        ("line_color", ink),
        ("line_style", "solid"),
        ("line_width", str(hatch["line_width_mm"])),
        ("line_width_unit", "MM"),
        ("offset", "0"),
        ("offset_unit", "MM"),
        ("use_custom_dash", "0"),
    ):
        ET.SubElement(
            line_opt, "Option", {"name": name, "type": "QString", "value": value}
        )
    line_dd = ET.SubElement(line, "data_defined_properties")
    line_root = ET.SubElement(line_dd, "Option", {"type": "Map"})
    ET.SubElement(line_root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(line_root, "Option", {"name": "properties"})
    ET.SubElement(
        line_root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )
    return layer


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
    # Scattered scrub keeps its dot pattern. Scrub gets a line hatch.
    if scrub.find("layer[@class='LinePatternFill']") is None:
        scrub.insert(0, _scrub_hatch(style))


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
