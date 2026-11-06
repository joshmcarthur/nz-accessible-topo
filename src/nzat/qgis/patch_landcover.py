from nzat.qgis.defaults import STYLE
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option


def _rule_symbol(layer, needle):
    renderer = layer.find("renderer-v2")
    if renderer is None:
        return None
    for rule in renderer.iter("rule"):
        blob = f"{rule.get('filter') or ''} {rule.get('label') or ''}".lower()
        if needle not in blob.split() and f"'{needle}'" not in blob:
            continue
        if needle == "moraine" and "moraine_wall" in blob:
            continue
        name = rule.get("symbol")
        for symbol in renderer.findall("symbols/symbol"):
            if symbol.get("name") == name:
                return symbol
    return None


def _set_svg_fill(symbol, spec):
    fill = symbol.find("layer[@class='SVGFill']")
    if fill is None:
        raise RuntimeError("landcover symbol has no SVGFill")
    set_option(fill, "svgFile", spec["marker"])
    set_option(fill, "color", rgba(spec["colour"], 255))


def patch_landcover(layer, style=None):
    style = style or STYLE
    cover = style["landcover"]
    swamp = dict(cover["swamp"])
    swamp["colour"] = style["reference_inks"]["stream"]
    paints = {
        "moraine": cover["moraine"],
        "scree": cover["scree"],
        "shingle": cover["shingle"],
        "swamp": swamp,
    }
    for key, spec in paints.items():
        symbol = _rule_symbol(layer, key)
        if symbol is None:
            continue
        _set_svg_fill(symbol, spec)
    wall = _rule_symbol(layer, "moraine_wall")
    if wall is None:
        return
    ink = rgba(cover["moraine_wall"]["colour"], 255)
    width = str(cover["moraine_wall"]["width_mm"])
    pattern = wall.find("layer[@class='LinePatternFill']")
    if pattern is not None:
        set_option(pattern, "color", ink)
    line = wall.find(".//layer[@class='SimpleLine']")
    if line is None:
        raise RuntimeError("moraine wall has no dotted line")
    set_option(line, "line_color", ink)
    set_option(line, "line_width", width)
    set_option(line, "use_custom_dash", "1")
