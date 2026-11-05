import copy
import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba

POINT_MM = 25.4 / 72
SIZE_FLOOR_PT = 6.0
# QPainter::CompositionMode_SourceOver.
SOURCE_OVER = "0"


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
    marker = next(
        (
            layer
            for layer in symbol.findall("layer[@class='FontMarker']")
            if layer.get("nzat") != "halo"
        ),
        None,
    )
    if marker is None:
        raise RuntimeError("contour_number has no FontMarker")
    _put(marker, "color", rgba(style["contours"]["index"]["colour"], 255))
    # FontMarker reads "font" and "font_style" (log 0082).
    _put(marker, "font_style", style["fonts"]["raster_upright_style"])
    _put(marker, "font", style["fonts"]["raster_family"])
    _put(marker, "fontItalic", "0")
    marker.set("fontItalic", "0")
    _lift_size(marker)
    _halo(symbol, marker, style)
    # Stock draws this layer DestinationOver, which puts each digit behind its
    # halo. Normal blending draws the halo first, then the digit (log 0082).
    blend = layer.find("featureBlendMode")
    if blend is not None:
        blend.text = SOURCE_OVER


def _halo(symbol, marker, style):
    """A paper-coloured copy of the digit, drawn first, with a stroke as the halo."""
    for old in symbol.findall("layer[@class='FontMarker']"):
        if old.get("nzat") == "halo":
            symbol.remove(old)
    halo = copy.deepcopy(marker)
    halo.set("nzat", "halo")
    if halo.get("id"):
        halo.set("id", "{" + str(uuid.uuid4()) + "}")
    paper = rgba(style["contours"]["number_halo"]["colour"], 255)
    _put(halo, "color", paper)
    _put(halo, "outline_color", paper)
    _put(halo, "outline_width", str(style["contours"]["number_halo"]["width_mm"]))
    _put(halo, "outline_width_unit", "MM")
    _put(halo, "joinstyle", "round")
    symbol.insert(list(symbol).index(marker), halo)
