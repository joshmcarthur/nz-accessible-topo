import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba

POINT_MM = 25.4 / 72
SIZE_FLOOR_PT = 6.0


def _rule_symbol(layer, token):
    renderer = layer.find("renderer-v2")
    symbol_name = None
    for rule in renderer.iter("rule"):
        filt = rule.get("filter") or ""
        if token in filt:
            symbol_name = rule.get("symbol")
            break
    if symbol_name is None:
        raise RuntimeError(f"no rule {token!r} on {layer.findtext('layername')}")
    for symbol in renderer.findall("symbols/symbol"):
        if symbol.get("name") == symbol_name:
            return symbol
    raise RuntimeError(f"no symbol {symbol_name}")


def _put(layer_el, name, value):
    option = layer_el.find("Option")
    for child in option:
        if child.get("name") == name:
            child.set("value", value)
            return
    ET.SubElement(option, "Option", {"name": name, "type": "QString", "value": value})


def _lift_size(marker):
    size_el = marker.find("Option/Option[@name='size']")
    unit_el = marker.find("Option/Option[@name='size_unit']")
    if size_el is None:
        _put(marker, "size", "6")
        _put(marker, "size_unit", "Point")
        return
    try:
        current = float(size_el.get("value") or 0)
    except ValueError:
        current = 0.0
    unit = (unit_el.get("value") if unit_el is not None else "MM") or "MM"
    if unit.upper() in ("POINT", "PT"):
        if current < SIZE_FLOOR_PT:
            size_el.set("value", "6")
        return
    mm_floor = SIZE_FLOOR_PT * POINT_MM
    if current < mm_floor:
        size_el.set("value", f"{mm_floor:.4g}")


def patch_contour_numbers(layer, style=None):
    """Paint contour_number FontMarkers with the index contour ink, upright."""
    style = style or STYLE
    symbol = _rule_symbol(layer, "contour_number")
    marker = symbol.find("layer[@class='FontMarker']")
    if marker is None:
        raise RuntimeError("contour_number has no FontMarker")
    _put(marker, "color", rgba(style["contours"]["index"]["colour"], 255))
    _put(marker, "fontStyle", style["fonts"]["raster_upright_style"])
    _put(marker, "fontFamily", style["fonts"]["raster_family"])
    _put(marker, "fontItalic", "0")
    marker.set("fontItalic", "0")
    _lift_size(marker)
