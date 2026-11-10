import copy
import uuid

from nzat.qgis.closed_bar_placement import _mm
from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_tracks import _marker_line, _marker_with
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.require_field import require_field
from nzat.qgis.rgba import alpha_byte, rgba, rgba_call
from nzat.qgis.set_option import set_option

SUPPLEMENTARY = "coalesce(\"designation\", '') = 'supplementary'"
DEPRESSION = "coalesce(\"formation\", '') = 'depression'"
# QGIS applies a data-defined dash even when useCustomDash is false, and a
# NULL dash falls back to the stock 5;2. One very long dash draws solid.
SOLID_DASH = "10000;0"


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
    names = [field.get("name") for field in layer.findall("fieldConfiguration/field")]
    if "designation" in names:
        dash = style["contours"]["supplementary"]["dash"]
        dash_expr = f"if({SUPPLEMENTARY}, '{dash}', '{SOLID_DASH}')"
        put_expr(casing_props, "customDash", dash_expr)
        put_expr(fill_props, "customDash", dash_expr)
        put_expr(casing_props, "useCustomDash", SUPPLEMENTARY)
        put_expr(fill_props, "useCustomDash", SUPPLEMENTARY)
    if "formation" in names:
        ticks = style["contours"]["depression"]
        ink = rgba(index["colour"], 255)
        existing = _marker_with(symbol, "depression")
        if existing is not None:
            symbol.remove(existing)
        symbol.append(
            _marker_line(
                "@depression",
                DEPRESSION,
                _mm(ticks["interval_mm"]),
                "0",
                (
                    ("angle", "0"),
                    ("cap_style", "square"),
                    ("color", ink),
                    ("horizontal_anchor_point", "1"),
                    ("joinstyle", "bevel"),
                    ("name", "line"),
                    ("offset", "0,0"),
                    ("offset_unit", "MM"),
                    ("outline_color", ink),
                    ("outline_style", "solid"),
                    ("outline_width", str(ticks["stroke_mm"])),
                    ("outline_width_unit", "MM"),
                    ("scale_method", "diameter"),
                    ("size", str(ticks["tick_mm"])),
                    ("size_unit", "MM"),
                    ("vertical_anchor_point", "1"),
                ),
            )
        )
