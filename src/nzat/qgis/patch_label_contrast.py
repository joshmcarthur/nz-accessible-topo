from nzat.colour.composite import composite
from nzat.colour.darken import darken_for_text
from nzat.qgis.colour_expression import colour_expression
from nzat.qgis.defaults import STYLE
from nzat.qgis.draw_configured_buffer import draw_configured_buffer
from nzat.qgis.expr import expr
from nzat.qgis.format_qgis_colour import format_qgis_colour
from nzat.qgis.label_behind import label_behind
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.put_expr import put_expr
from nzat.qgis.rgb_key import rgb_key
from nzat.qgis.rgba import rgba
from nzat.qgis.settings_props import settings_props


def _is_named_project_colour(expression):
    if not expression:
        return False
    compact = "".join(expression.split())
    return compact in (
        'project_color_object("colour")',
        "project_color_object('colour')",
    )


def _darken_text_color(text_style, behind, min_ratio, red_min=None):
    parsed = parse_qgis_colour(text_style.get("textColor"))
    if parsed is None:
        return
    red, green, blue, alpha = parsed
    fg = composite((red, green, blue, alpha / 255.0), behind)
    new = darken_for_text(fg, behind, min_ratio, red_min)
    if rgb_key(new) == rgb_key(fg):
        return
    text_style.set("textColor", format_qgis_colour(new, 255))


def patch_label_contrast(layer, style=None, palette=None):
    """Draw each configured label buffer. Darken ink that misses the contrast floor."""
    style = style or STYLE
    min_ratio = style["label_contrast"]["min_ratio"]
    red_min = style["label_contrast"]["red_light_min"]
    max_mm = style["label_contrast"]["halo_max_mm"]
    named = palette or []
    layer_name = layer.findtext("layername") or ""
    spot = style["labels"]["spot_height_layer_contains"]
    urban = style["reference_inks"]["urban_fill"]
    for settings in layer.findall(".//settings"):
        text_style = settings.find("text-style")
        if text_style is None:
            continue
        buffer_el = text_style.find("text-buffer")
        draw_configured_buffer(buffer_el, max_mm)
        if spot in layer_name and buffer_el is not None:
            parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
            if parsed is not None:
                buffer_el.set("bufferColor", rgba(urban, 255))
        behind = label_behind(buffer_el)
        props = settings_props(settings)
        expression = expr(props, "Color") if props is not None else None
        if _is_named_project_colour(expression):
            updated = colour_expression(named, behind, min_ratio, red_min)
            if updated:
                put_expr(props, "Color", updated)
            continue
        _darken_text_color(text_style, behind, min_ratio, red_min)
