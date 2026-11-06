import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option


def _field_names(layer):
    return [field.get("name") for field in layer.findall("fieldConfiguration/field")]


def _type_field(layer):
    names = _field_names(layer)
    if "type" in names:
        return "type"
    if "feature_type" in names:
        return "feature_type"
    raise RuntimeError("relief_point map has no type field")


def _empty_dd(parent):
    dd = ET.SubElement(parent, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(root, "Option", {"name": "properties"})
    ET.SubElement(
        root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )


def _saddle_marker(spec):
    ink = rgba("#000000", 255)
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
        ("color", ink),
        ("fixedAspectRatio", "0"),
        ("horizontal_anchor_point", "1"),
        ("name", spec["marker"]),
        ("offset", "0,0"),
        ("offset_unit", "MM"),
        ("outline_color", ink),
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


def _saddle_symbol(spec):
    symbol = ET.Element(
        "symbol",
        {
            "alpha": "1",
            "clip_to_extent": "1",
            "force_rhr": "0",
            "frame_rate": "10",
            "is_animated": "0",
            "name": "1",
            "type": "marker",
        },
    )
    _empty_dd(symbol)
    symbol.append(_saddle_marker(spec))
    return symbol


def _convert_single(renderer, spec, saddle_filter):
    renderer.set("type", "RuleRenderer")
    symbols = renderer.find("symbols")
    base = symbols.find("symbol")
    base.set("name", "0")
    symbols.append(_saddle_symbol(spec))
    rules = ET.Element("rules")
    ET.SubElement(
        rules,
        "rule",
        {"filter": saddle_filter, "label": "saddle", "symbol": "1"},
    )
    ET.SubElement(rules, "rule", {"filter": "ELSE", "label": "height", "symbol": "0"})
    renderer.insert(0, rules)


def patch_relief_point(layer, style=None):
    style = style or STYLE
    field = _type_field(layer)
    spec = style["relief"]["saddle"]
    saddle_filter = f"coalesce(\"{field}\", '') = 'saddle'"
    renderer = layer.find("renderer-v2")
    if renderer is None:
        raise RuntimeError("relief_point map has no renderer")
    if renderer.get("type") != "RuleRenderer":
        _convert_single(renderer, spec, saddle_filter)
    else:
        for rule in renderer.findall("rules/rule"):
            if "saddle" in (rule.get("filter") or ""):
                name = rule.get("symbol")
                for symbol in renderer.findall("symbols/symbol"):
                    if symbol.get("name") == name:
                        marker = symbol.find("layer[@class='SvgMarker']")
                        if marker is None:
                            for child in list(symbol):
                                if child.tag == "layer":
                                    symbol.remove(child)
                            symbol.append(_saddle_marker(spec))
                        else:
                            set_option(marker, "name", spec["marker"])
                            set_option(marker, "size", str(spec["size_mm"]))
                        break
                break
        else:
            symbols = renderer.find("symbols")
            extra = _saddle_symbol(spec)
            extra.set("name", "1")
            symbols.append(extra)
            renderer.find("rules").insert(
                0,
                ET.Element(
                    "rule",
                    {"filter": saddle_filter, "label": "saddle", "symbol": "1"},
                ),
            )
    for rule in renderer.findall("rules/rule"):
        if (rule.get("filter") or "").strip() != "ELSE":
            continue
        name = rule.get("symbol")
        for symbol in renderer.findall("symbols/symbol"):
            if symbol.get("name") != name:
                continue
            marker = symbol.find("layer[@class='SimpleMarker']")
            if marker is None:
                continue
            set_option(marker, "size", "0.3")
