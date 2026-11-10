from nzat.qgis.defaults import STYLE
from nzat.qgis.set_option import set_option


def _line_width_mm(line):
    option = line.find("Option/Option[@name='line_width']")
    if option is None or not option.get("value"):
        return None
    return float(option.get("value"))


def _raise_simple_lines(parent, floor):
    for line in parent.findall("layer[@class='SimpleLine']"):
        width = _line_width_mm(line)
        if width is None or width >= floor:
            continue
        set_option(line, "line_width", str(floor))


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


def _raise_embankments(layer, spec):
    """Embankment and stopbank ticks are 0.1 mm in stock. Reduced acuity loses them."""
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return
    names = {
        rule.get("symbol")
        for rule in renderer.iter("rule")
        if "embankment" in (rule.get("label") or "").lower()
    }
    for symbol in renderer.findall("symbols/symbol"):
        if symbol.get("name") not in names:
            continue
        _raise_simple_lines(symbol, float(spec["line_mm"]))
        for marker in symbol.findall(
            "layer[@class='MarkerLine']/symbol/layer[@class='SimpleMarker']"
        ):
            option = marker.find("Option/Option[@name='outline_width']")
            if (
                option is not None
                and float(option.get("value")) < spec["tick_stroke_mm"]
            ):
                set_option(marker, "outline_width", str(spec["tick_stroke_mm"]))


def patch_thin_lines(layer, style=None):
    """Raise thin fence, embankment, ice contour and bridge strokes to the style."""
    style = style or STYLE
    name = layer.findtext("layername") or ""
    sizes = style["sizes"]
    if name == "fence_line map":
        symbol = layer.find("renderer-v2/symbols/symbol")
        if symbol is not None:
            _raise_simple_lines(symbol, float(sizes["fence_line_mm"]))
        return
    if name == "nztopo50_ice_contour":
        symbol = layer.find("renderer-v2/symbols/symbol")
        if symbol is not None:
            _raise_simple_lines(symbol, float(sizes["ice_contour_mm"]))
        return
    if name == "relief_line map":
        _raise_embankments(layer, style["relief"]["embankment"])
        return
    if name != "bridge_line copy copy":
        return
    symbol = _find_rule_symbol(layer, "vehicle-2")
    if symbol is None:
        return
    spec = style["bridges"]["two_lane"]
    casing = str(spec["casing_width_mm"])
    for line in symbol.findall("layer[@class='SimpleLine']"):
        set_option(line, "line_width", casing)
    tick = spec["tick_mm"]
    for marker in symbol.findall(
        "layer[@class='MarkerLine']/symbol/layer[@class='SimpleMarker']"
    ):
        set_option(marker, "size", str(tick))
