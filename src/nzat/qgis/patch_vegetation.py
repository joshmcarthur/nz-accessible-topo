import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.category_symbol import category_symbol
from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option

MAP_UNIT_SCALE = "3x:0,0,0,0,0,0"
MARKER_CLASSES = (
    "PointPatternFill",
    "CentroidFill",
    "SimpleMarker",
    "FontMarker",
    "SvgMarker",
)
TREE_MARKER_CLASSES = ("SimpleMarker", "SvgMarker")


def _empty_dd(parent):
    dd = ET.SubElement(parent, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(root, "Option", {"name": "properties"})
    ET.SubElement(
        root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )


def _plant_grid(dots, distance_mm, clip_mode):
    ink = rgba(dots["colour"], 255)
    dist = str(distance_mm)
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
        ("clip_mode", clip_mode, "QString"),
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
            "name": "@plant",
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


def _sync_plant_grid(pattern, dots, distance_mm, clip_mode=None):
    dist = str(distance_mm)
    ink = rgba(dots["colour"], 255)
    set_option(pattern, "distance_x", dist)
    set_option(pattern, "distance_y", dist)
    if clip_mode is not None:
        set_option(pattern, "clip_mode", clip_mode)
    simple = pattern.find("symbol/layer[@class='SimpleMarker']")
    if simple is None:
        raise RuntimeError("plant grid has no marker")
    set_option(simple, "name", dots["marker"])
    set_option(simple, "size", str(dots["size_mm"]))
    set_option(simple, "color", ink)
    set_option(simple, "outline_color", ink)
    set_option(simple, "outline_width", str(dots["stroke_mm"]))


def _tree_marker(style):
    trees = style["vegetation"]["trees"]
    ink = rgba(style["reference_inks"]["shelterbelt"], 255)
    layer = ET.Element(
        "layer",
        {
            "class": "SvgMarker",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    for name, value in (
        ("angle", "0"),
        ("color", ink),
        ("fixedAspectRatio", "0"),
        ("horizontal_anchor_point", "1"),
        ("name", trees["marker"]),
        ("offset", "0,0"),
        ("offset_map_unit_scale", MAP_UNIT_SCALE),
        ("offset_unit", "MM"),
        ("outline_color", ink),
        ("outline_width", "0"),
        ("outline_width_map_unit_scale", MAP_UNIT_SCALE),
        ("outline_width_unit", "MM"),
        ("scale_method", "diameter"),
        ("size", str(trees["size_mm"])),
        ("size_map_unit_scale", MAP_UNIT_SCALE),
        ("size_unit", "MM"),
        ("vertical_anchor_point", "1"),
    ):
        ET.SubElement(
            options, "Option", {"name": name, "type": "QString", "value": value}
        )
    ET.SubElement(options, "Option", {"name": "parameters"})
    _empty_dd(layer)
    return layer


def _patch_trees(layer, style):
    symbol = layer.find("renderer-v2/symbols/symbol")
    if symbol is None:
        raise RuntimeError("vegetation_point has no symbol")
    for child in list(symbol):
        if child.tag == "layer" and child.get("class") in TREE_MARKER_CLASSES:
            symbol.remove(child)
    symbol.append(_tree_marker(style))


def _paint_outlines(layer, style):
    outline = rgba(style["reference_inks"]["vegetation_outline"], 255)
    renderer = layer.find("renderer-v2")
    for category in renderer.findall("categories/category"):
        value = category.get("value")
        if not value or value == "NULL":
            continue
        symbol = category_symbol(layer, value)
        fill = symbol.find("layer[@class='SimpleFill']")
        if fill is None:
            continue
        set_option(fill, "outline_color", outline)


def _paint_plant_grid(symbol, dots, distance_mm, clip_mode=None):
    existing = symbol.find("layer[@class='PointPatternFill']")
    if existing is None:
        symbol.insert(0, _plant_grid(dots, distance_mm, clip_mode or "centroid_within"))
        return
    _sync_plant_grid(existing, dots, distance_mm, clip_mode)


def patch_vegetation(layer, style=None):
    style = style or STYLE
    if (layer.findtext("layername") or "") == "vegetation_point map":
        _patch_trees(layer, style)
        return
    native_ink = style["vegetation"]["native"]
    scrub_ink = style["vegetation"]["scrub"]
    dots = style["vegetation"]["scrub_dots"]
    native = category_symbol(layer, "native")
    scrub = category_symbol(layer, "scrub")
    scattered = category_symbol(layer, "scattered_scrub")
    native_fill = native.find("layer[@class='SimpleFill']")
    scrub_fill = scrub.find("layer[@class='SimpleFill']")
    set_option(native_fill, "color", rgba(native_ink["colour"], native_ink["alpha"]))
    set_option(scrub_fill, "color", rgba(scrub_ink["colour"], scrub_ink["alpha"]))
    _paint_native_marker(native, style)
    # Colour alone does not separate these fills in greyscale (R-10).
    # Scrub gets a denser plant grid. Scattered keeps the stock 5 mm grid.
    for hatch in list(scrub.findall("layer[@class='LinePatternFill']")):
        scrub.remove(hatch)
    _paint_plant_grid(scrub, dots, dots["distance_mm"], "centroid_within")
    _paint_plant_grid(
        scattered,
        dots,
        style["vegetation"]["scattered"]["distance_mm"],
        "completely_within",
    )
    _paint_outlines(layer, style)


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
