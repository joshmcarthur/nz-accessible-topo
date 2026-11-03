import copy
import uuid

from nzat.qgis.defaults import STYLE
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.require_field import require_field
from nzat.qgis.rgba import alpha_byte, rgba, rgba_call
from nzat.qgis.set_option import set_option


def patch_contour(layer, style=None):
    style = style or STYLE
    index = style["contours"]["index"]
    intermediate = style["contours"]["intermediate"]
    require_field(layer, "elevation")
    symbol = layer.find("renderer-v2/symbols/symbol")
    lines = symbol.findall("layer[@class='SimpleLine']")
    if not lines:
        raise RuntimeError("contour symbol has no SimpleLine")
    if len(lines) == 1:
        casing = copy.deepcopy(lines[0])
        casing.set("id", "{" + str(uuid.uuid4()) + "}")
        symbol.insert(list(symbol).index(lines[0]), casing)
        fill = lines[0]
    else:
        casing = lines[0]
        fill = lines[1]
    # definition is null on the national contour table, so indefinite
    # contours cannot be dashed from that field.
    casing_props = properties_map(casing.find("data_defined_properties"))
    put_expr(
        casing_props,
        "enabled",
        '"elevation" IS NOT NULL AND round("elevation") % 100 <> 0',
    )
    put_expr(
        casing_props,
        "outlineColor",
        rgba_call(intermediate["casing_colour"], intermediate["alpha"]),
    )
    put_expr(casing_props, "outlineWidth", str(intermediate["casing_width_mm"]))
    set_option(
        casing,
        "line_color",
        rgba(intermediate["casing_colour"], alpha_byte(intermediate["alpha"])),
    )
    set_option(casing, "line_width", str(intermediate["casing_width_mm"]))
    fill_props = properties_map(fill.find("data_defined_properties"))
    put_expr(
        fill_props,
        "outlineColor",
        'CASE WHEN "elevation" IS NOT NULL AND round("elevation") % 100 = 0'
        f" THEN {rgba_call(index['colour'], index['alpha'])}"
        f" ELSE {rgba_call(intermediate['colour'], intermediate['alpha'])} END",
    )
    put_expr(
        fill_props,
        "outlineWidth",
        'CASE WHEN "elevation" IS NOT NULL AND round("elevation") % 100 = 0'
        f" THEN {index['width_mm']} ELSE {intermediate['width_mm']} END",
    )
