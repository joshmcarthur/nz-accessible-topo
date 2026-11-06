import copy

from nzat.qgis.defaults import STYLE
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.require_field import require_field
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option

MULTIPLE = "coalesce(\"track_type\", '') = 'multiple'"


def _white_line(symbol):
    for line in symbol.findall("layer[@class='SimpleLine']"):
        colour = line.find("Option/Option[@name='line_color']")
        if colour is not None and (colour.get("value") or "").startswith("255,255,255"):
            return line
    return None


def patch_railway(layer, style=None):
    style = style or STYLE
    require_field(layer, "track_type")
    spec = style["railway"]
    symbol = layer.find("renderer-v2/symbols/symbol")
    if symbol is None:
        raise RuntimeError("railway_line map has no symbol")
    black = None
    for line in symbol.findall("layer[@class='SimpleLine']"):
        colour = line.find("Option/Option[@name='line_color']")
        if colour is None or (colour.get("value") or "").startswith("255,255,255"):
            continue
        black = line
        break
    if black is None:
        raise RuntimeError("railway_line map has no black line")
    props = properties_map(black.find("data_defined_properties"))
    put_expr(
        props,
        "outlineWidth",
        f"CASE WHEN {MULTIPLE} THEN {spec['multiple_width_mm']} "
        f"ELSE {spec['single_width_mm']} END",
    )
    set_option(black, "line_width", str(spec["single_width_mm"]))
    white = _white_line(symbol)
    if white is None:
        white = copy.deepcopy(black)
        symbol.append(white)
    set_option(white, "line_color", rgba("#FFFFFF", 255))
    set_option(white, "line_width", str(spec["dash_width_mm"]))
    set_option(white, "customdash", spec["dash"])
    set_option(white, "use_custom_dash", "1")
    white_props = properties_map(white.find("data_defined_properties"))
    put_expr(white_props, "enabled", MULTIPLE)
    put_expr(white_props, "outlineWidth", str(spec["dash_width_mm"]))
