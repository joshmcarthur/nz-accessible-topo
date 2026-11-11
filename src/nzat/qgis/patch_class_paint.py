"""Owned symbols for the classes on `landuse` and `structure_line`.

Both layers categorise on a `feature_type` column the data does not have,
so stock paints every feature with the NULL category. The per-type
categories are unstyled QGIS random colours (log 0114). This patch reads
`type`, draws each class in `class_paint` from the printed LINZ legend, and
gives every other class a copy of the NULL symbol, so none draws in a
random colour.
"""

import copy
import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba

CLEAR = "0,0,0,0"
# Marker shapes that are a stroke with no area to fill.
STROKE_SHAPES = ("line", "cross", "cross2", "arrowhead")
PLACEMENTS = {
    "ends": "LastVertex|FirstVertex",
    "start": "FirstVertex",
    "end": "LastVertex",
    "interval": "Interval",
}


def _layer(cls, options):
    layer = ET.Element(
        "layer",
        {
            "class": cls,
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    holder = ET.SubElement(layer, "Option", {"type": "Map"})
    for name, value in options.items():
        ET.SubElement(
            holder, "Option", {"name": name, "type": "QString", "value": str(value)}
        )
    return layer


def _line(spec):
    options = {
        "line_color": rgba(spec["colour"], 255),
        "line_style": "solid",
        "line_width": spec["width_mm"],
        "line_width_unit": "MM",
        "capstyle": "flat",
        "joinstyle": "round",
        "use_custom_dash": "1" if "dash" in spec else "0",
        "customdash": spec.get("dash", "5;2"),
        "customdash_unit": "MM",
    }
    return _layer("SimpleLine", options)


def _marker_symbol(spec, name):
    ink = rgba(spec["colour"], 255)
    stroke_only = spec["shape"] in STROKE_SHAPES
    filled = spec.get("filled", False) and not stroke_only
    marker = _layer(
        "SimpleMarker",
        {
            "name": spec["shape"],
            "size": spec["size_mm"],
            "size_unit": "MM",
            "angle": spec.get("angle", 0),
            "color": ink if filled else rgba(spec.get("fill", "#FFFFFF"), 255),
            "outline_color": ink,
            "outline_style": "solid",
            "outline_width": spec["stroke_mm"],
            "outline_width_unit": "MM",
            "joinstyle": "miter",
            "cap_style": "flat",
        },
    )
    symbol = ET.Element(
        "symbol",
        {"alpha": "1", "clip_to_extent": "1", "name": name, "type": "marker"},
    )
    symbol.append(marker)
    return symbol


def _markers(spec, name):
    layer = _layer(
        "MarkerLine",
        {
            "placements": PLACEMENTS[spec["at"]],
            "interval": spec.get("interval_mm", 3),
            "interval_unit": "MM",
            "offset_along_line": spec.get("start_mm", 0),
            "offset_along_line_unit": "MM",
            "rotate": "1",
            "place_on_every_part": "true",
        },
    )
    layer.append(_marker_symbol(spec, name))
    return layer


def _pattern(spec, name):
    layer = _layer(
        "PointPatternFill",
        {
            "distance_x": spec["spacing_mm"][0],
            "distance_x_unit": "MM",
            "distance_y": spec["spacing_mm"][1],
            "distance_y_unit": "MM",
            "offset_x": spec.get("offset_mm", (0, 0))[0],
            "offset_x_unit": "MM",
            "offset_y": spec.get("offset_mm", (0, 0))[1],
            "offset_y_unit": "MM",
            "coordinate_reference": "feature",
            "clip_mode": "shape",
        },
    )
    layer.append(_marker_symbol(spec, name))
    return layer


def symbol_layers(spec, name):
    """Return the QGIS symbol layers for one class spec, bottom first."""
    layers = []
    if "pattern" in spec:
        layers.append(_pattern(spec["pattern"], f"@{name}@{len(layers)}"))
    for line in spec.get("lines", ()):
        layers.append(_line(line))
    for marker in spec.get("markers", ()):
        layers.append(_markers(marker, f"@{name}@{len(layers)}"))
    return layers


def _fill(symbol, layers):
    for old in symbol.findall("layer"):
        symbol.remove(old)
    for layer in layers:
        symbol.append(layer)


def patch_class_paint(layer, style=None):
    """Read `type`, draw owned classes, and keep the stock paint on the rest."""
    style = style or STYLE
    table = layer.findtext("layername") or ""
    spec = style["class_paint"].get(table)
    renderer = layer.find("renderer-v2")
    if spec is None or renderer is None:
        return
    if renderer.get("attr") not in ("feature_type", "type"):
        return
    categories = renderer.find("categories")
    symbols = renderer.find("symbols")
    by_name = {symbol.get("name"): symbol for symbol in symbols.findall("symbol")}
    null = next(c for c in categories.findall("category") if c.get("value") == "NULL")
    stock = by_name[null.get("symbol")]
    renderer.set("attr", "type")
    known = {c.get("value"): c for c in categories.findall("category")}
    wanted = [*spec["classes"], *spec.get("stock_paint", ())]
    for value in wanted:
        if value in known:
            continue
        name = str(max(int(n) for n in by_name) + 1)
        fresh = copy.deepcopy(stock)
        fresh.set("name", name)
        symbols.append(fresh)
        by_name[name] = fresh
        known[value] = ET.SubElement(
            categories,
            "category",
            {
                "label": value,
                "render": "true",
                "symbol": name,
                "type": "string",
                "uuid": "{" + str(uuid.uuid4()) + "}",
                "value": value,
            },
        )
    for value, category in known.items():
        if value == "NULL":
            continue
        symbol = by_name[category.get("symbol")]
        if value in spec["classes"]:
            _fill(symbol, symbol_layers(spec["classes"][value], symbol.get("name")))
        else:
            _fill(symbol, [copy.deepcopy(old) for old in stock.findall("layer")])
