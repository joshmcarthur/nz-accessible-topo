import copy
import shutil
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from nzat.qgis.category_symbol import category_symbol
from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_contour_numbers import _put, _rule_symbol
from nzat.qgis.properties_map import properties_map
from nzat.qgis.require_field import require_field
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option

SYMBOLS_DIR = Path(__file__).resolve().parent / "symbols"
BIVOUAC_SVG = SYMBOLS_DIR / "nztopo50_bivouac.svg"
MARKER_CLASSES = ("SvgMarker", "SimpleMarker")
SVG_FILL_NONE = "0,0,0,0"
# Structure-point rules whose LINZ SVG has a fixed-colour stroke under 0.15 mm.
# Needles match the stock filter or label. Missing rules are left alone.
OWNED_POINT_SVGS = (
    ("beacon", ("beacon",)),
    ("mast", ("mast",)),
    ("redoubt", ("redoubt",)),
    ("tower", ("tower",)),
    ("shipwreck", ("wreck_of", "ship")),
    ("lighthouse", ("lighthouse",)),
    ("shaft", ("shaft",)),
    ("stockyard", ("stockyard",)),
    ("tank_water", ("stored_item", "water")),
)


def _empty_dd(parent):
    dd = ET.SubElement(parent, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(root, "Option", {"name": "properties"})
    ET.SubElement(
        root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )


def _marker_name(layer_el):
    option = layer_el.find("Option/Option[@name='name']")
    return None if option is None else option.get("value")


def _simple_marker(name, size_mm, ink, *, filled):
    layer = ET.Element(
        "layer",
        {
            "class": "SimpleMarker",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "1",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    outline_style = "no" if filled else "solid"
    outline_width = "0" if filled else "0.2"
    for option_name, value in (
        ("angle", "0"),
        ("cap_style", "square"),
        ("color", ink),
        ("horizontal_anchor_point", "1"),
        ("joinstyle", "bevel"),
        ("name", name),
        ("offset", "0,0"),
        ("offset_unit", "MM"),
        ("outline_color", ink),
        ("outline_style", outline_style),
        ("outline_width", outline_width),
        ("outline_width_unit", "MM"),
        ("scale_method", "diameter"),
        ("size", str(size_mm)),
        ("size_unit", "MM"),
        ("vertical_anchor_point", "1"),
    ):
        ET.SubElement(
            options, "Option", {"name": option_name, "type": "QString", "value": value}
        )
    _empty_dd(layer)
    return layer


def _copy_angle(src, dest):
    src_props = src.find("data_defined_properties/Option/Option[@name='properties']")
    if src_props is None:
        return
    angle = src_props.find("Option[@name='angle']")
    if angle is None:
        return
    dest_dd = dest.find("data_defined_properties")
    dest_props = properties_map(dest_dd)
    dest_props.append(copy.deepcopy(angle))


def _svg_marker(spec, _ink):
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
    for option_name, value in (
        ("angle", "0"),
        ("color", SVG_FILL_NONE),
        ("fixedAspectRatio", "0"),
        ("horizontal_anchor_point", "1"),
        ("name", spec["marker"]),
        ("offset", "0,0"),
        ("offset_unit", "MM"),
        ("outline_color", rgba("#000000", 255)),
        ("outline_width", "0"),
        ("outline_width_unit", "MM"),
        ("scale_method", "diameter"),
        ("size", str(spec["size_mm"])),
        ("size_unit", "MM"),
        ("vertical_anchor_point", "1"),
    ):
        ET.SubElement(
            options, "Option", {"name": option_name, "type": "QString", "value": value}
        )
    ET.SubElement(options, "Option", {"name": "parameters"})
    _empty_dd(layer)
    return layer


def _patch_locked_gate(layer, style):
    symbol = _rule_symbol(layer, "locked")
    spec = style["structures"]["locked_gate"]
    ink = rgba(spec["bar_colour"], 255)
    _keep_named_markers(symbol, {"line"})
    bar = None
    for marker in symbol.findall("layer[@class='SimpleMarker']"):
        if _marker_name(marker) == "line":
            bar = marker
            break
    if bar is None:
        raise RuntimeError("locked gate has no bar")
    set_option(bar, "outline_color", ink)
    set_option(bar, "color", ink)
    set_option(bar, "size", str(spec["bar_size_mm"]))
    set_option(bar, "outline_width", str(spec["bar_stroke_mm"]))
    square = _simple_marker("square", spec["lock_size_mm"], ink, filled=True)
    _copy_angle(bar, square)
    symbol.append(square)
    bars = [
        marker
        for marker in symbol.findall("layer[@class='SimpleMarker']")
        if _marker_name(marker) == "line"
    ]
    if len(bars) != 1:
        raise RuntimeError("locked gate must keep one bar")


def _find_rule_symbol(layer, *needles):
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return None
    for rule in renderer.iter("rule"):
        blob = f"{rule.get('filter') or ''} {rule.get('label') or ''}".lower()
        if not all(needle.lower() in blob for needle in needles):
            continue
        name = rule.get("symbol")
        for symbol in renderer.findall("symbols/symbol"):
            if symbol.get("name") == name:
                return symbol
    return None


def _drop_circle_markers(symbol):
    for marker in list(symbol.findall("layer[@class='SimpleMarker']")):
        if _marker_name(marker) in (None, "circle"):
            symbol.remove(marker)


def _keep_named_markers(symbol, keep):
    for marker in list(symbol.findall("layer[@class='SimpleMarker']")):
        if _marker_name(marker) not in keep:
            symbol.remove(marker)


def _clear_stroke_only_svg_fill(symbol):
    marker = symbol.find("layer[@class='SvgMarker']")
    if marker is None:
        return
    _put(marker, "color", SVG_FILL_NONE)
    _put(marker, "outline_color", rgba("#000000", 255))
    _drop_circle_markers(symbol)


def _set_svg_marker(symbol, spec):
    marker = symbol.find("layer[@class='SvgMarker']")
    if marker is None:
        raise RuntimeError("symbol has no SvgMarker")
    set_option(marker, "name", spec["marker"])
    set_option(marker, "size", str(spec["size_mm"]))
    _clear_stroke_only_svg_fill(symbol)


def _patch_owned_point_svgs(layer, style):
    for key, needles in OWNED_POINT_SVGS:
        symbol = _find_rule_symbol(layer, *needles)
        if symbol is None:
            continue
        _set_svg_marker(symbol, style["structures"][key])


def _patch_bivouac(layer, style):
    symbol = _rule_symbol(layer, "bivouac")
    spec = style["structures"]["bivouac"]
    ink = rgba(spec["colour"], 255)
    for child in list(symbol):
        if child.tag == "layer" and child.get("class") in MARKER_CLASSES:
            symbol.remove(child)
    symbol.append(_svg_marker(spec, ink))


def patch_building_point(layer, style=None):
    style = style or STYLE
    church = _find_rule_symbol(layer, "church")
    if church is not None:
        spec = style["structures"]["church"]
        _set_svg_marker(church, spec)
        for marker in church.findall("layer[@class='SimpleMarker']"):
            if _marker_name(marker) == "line":
                set_option(marker, "outline_width", str(spec["bar_stroke_mm"]))
    hut = _find_rule_symbol(layer, "hut")
    if hut is not None:
        _set_svg_marker(hut, style["structures"]["hut"])


def _gas_symbol(layer):
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return None
    for rule in renderer.iter("rule"):
        blob = f"{rule.get('filter') or ''} {rule.get('label') or ''}".lower()
        if "gas" not in blob:
            continue
        name = rule.get("symbol")
        for symbol in renderer.findall("symbols/symbol"):
            if symbol.get("name") == name:
                return symbol
    for category in renderer.findall("categories/category"):
        blob = f"{category.get('value') or ''} {category.get('label') or ''}".lower()
        if "gas" not in blob:
            continue
        return category_symbol(layer, category.get("value"))
    return None


def _patch_gas_pipeline(layer, style):
    symbol = _gas_symbol(layer)
    if symbol is None:
        return
    spec = style["structures"]["buried_gas_pipeline"]
    line = symbol.find("layer[@class='SimpleLine']")
    if line is None:
        raise RuntimeError("buried gas pipeline has no line")
    _put(line, "line_color", rgba(spec["colour"], 255))
    _put(line, "line_width", str(spec["width_mm"]))
    _put(line, "customdash", spec["dash"])
    _put(line, "use_custom_dash", "1")


def _gate_else_symbol(layer):
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return None
    for rule in renderer.iter("rule"):
        blob = f"{rule.get('filter') or ''} {rule.get('label') or ''}".lower()
        if "gate" not in blob or "flood" in blob:
            continue
        for child in rule.findall("rule"):
            if (child.get("filter") or "").strip() != "ELSE":
                continue
            name = child.get("symbol")
            for symbol in renderer.findall("symbols/symbol"):
                if symbol.get("name") == name:
                    return symbol
    return None


def _patch_unlocked_gate(layer, style):
    symbol = _gate_else_symbol(layer)
    if symbol is None:
        return
    spec = style["structures"]["floodgate"]
    _keep_named_markers(symbol, {"line"})
    bar = None
    for marker in symbol.findall("layer[@class='SimpleMarker']"):
        if _marker_name(marker) == "line":
            bar = marker
            break
    if bar is None:
        return
    set_option(bar, "color", rgba("#000000", 255))
    set_option(bar, "outline_color", rgba("#000000", 255))
    set_option(bar, "size", str(spec["bar_size_mm"]))
    set_option(bar, "outline_width", str(spec["bar_stroke_mm"]))


def _patch_floodgate(layer, style):
    symbol = _find_rule_symbol(layer, "floodgate")
    if symbol is None:
        return
    spec = style["structures"]["floodgate"]
    _keep_named_markers(symbol, {"line"})
    bar = None
    for marker in symbol.findall("layer[@class='SimpleMarker']"):
        if _marker_name(marker) == "line":
            bar = marker
            break
    if bar is None:
        raise RuntimeError("floodgate has no bar")
    set_option(bar, "color", rgba("#000000", 255))
    set_option(bar, "outline_color", rgba("#000000", 255))
    set_option(bar, "size", str(spec["bar_size_mm"]))
    set_option(bar, "outline_width", str(spec["bar_stroke_mm"]))


def _patch_windmill(layer):
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return
    names = set()
    for rule in renderer.iter("rule"):
        blob = f"{rule.get('filter') or ''} {rule.get('label') or ''}".lower()
        if "windmill" not in blob:
            continue
        if rule.get("symbol"):
            names.add(rule.get("symbol"))
        for child in rule.findall("rule"):
            if child.get("symbol"):
                names.add(child.get("symbol"))
    for symbol in renderer.findall("symbols/symbol"):
        if symbol.get("name") in names:
            _clear_stroke_only_svg_fill(symbol)


def _greenhouse_fill():
    layer = ET.Element(
        "layer",
        {
            "class": "SimpleFill",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    for option_name, value in (
        ("color", rgba("#000000", 0)),
        ("offset", "0,0"),
        ("outline_color", rgba("#000000", 255)),
        ("outline_style", "solid"),
        ("outline_width", "0.2"),
        ("style", "no"),
    ):
        ET.SubElement(
            options, "Option", {"name": option_name, "type": "QString", "value": value}
        )
    _empty_dd(layer)
    return layer


def patch_building(layer, style=None):
    style = style or STYLE
    require_field(layer, "subtype")
    spec = style["structures"]["glasshouse"]
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return
    greenhouse_filter = "coalesce(\"subtype\", '') = 'greenhouse'"
    if renderer.get("type") != "RuleRenderer":
        renderer.set("type", "RuleRenderer")
        symbols = renderer.find("symbols")
        base = symbols.find("symbol")
        base.set("name", "0")
        extra = copy.deepcopy(base)
        extra.set("name", "1")
        for child in list(extra):
            if child.tag == "layer":
                extra.remove(child)
        extra.append(_greenhouse_fill())
        symbols.append(extra)
        rules = ET.Element("rules")
        ET.SubElement(
            rules,
            "rule",
            {
                "filter": greenhouse_filter,
                "label": "greenhouse",
                "symbol": "1",
            },
        )
        ET.SubElement(
            rules, "rule", {"filter": "ELSE", "label": "building", "symbol": "0"}
        )
        renderer.insert(0, rules)
        return
    symbol = _find_rule_symbol(layer, "greenhouse")
    if symbol is None:
        return
    fill = symbol.find("layer[@class='SimpleFill']")
    if fill is None:
        return
    set_option(fill, "style", "no")
    set_option(fill, "outline_width", str(spec["outline_mm"]))
    set_option(fill, "outline_color", rgba("#000000", 255))


def patch_structure_point(layer, style=None):
    style = style or STYLE
    _patch_locked_gate(layer, style)
    _patch_unlocked_gate(layer, style)
    _patch_bivouac(layer, style)
    _patch_owned_point_svgs(layer, style)
    _patch_floodgate(layer, style)
    _patch_windmill(layer)


def patch_structure_line(layer, style=None):
    style = style or STYLE
    _patch_gas_pipeline(layer, style)


def install_owned_symbols(project_dir):
    dest_dir = Path(project_dir) / "symbol"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for svg in SYMBOLS_DIR.glob("*.svg"):
        shutil.copyfile(svg, dest_dir / svg.name)
