from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option


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


def patch_contour_numbers(layer, style=None):
    """Paint contour_number FontMarkers with the index contour ink."""
    style = style or STYLE
    symbol = _rule_symbol(layer, "contour_number")
    marker = symbol.find("layer[@class='FontMarker']")
    if marker is None:
        raise RuntimeError("contour_number has no FontMarker")
    set_option(marker, "color", rgba(style["contours"]["index"]["colour"], 255))
