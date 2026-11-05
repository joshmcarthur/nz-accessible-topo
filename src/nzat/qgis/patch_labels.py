from nzat.qgis.curved_label_mode_expression import curved_label_mode_expression
from nzat.qgis.defaults import CARTO_TEXT_LAYER, STYLE
from nzat.qgis.expr import expr
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.patch_carto_point_labels import patch_carto_point_labels
from nzat.qgis.patch_label_contrast import patch_label_contrast
from nzat.qgis.patch_wrap_baseline import patch_wrap_baseline
from nzat.qgis.put_expr import put_expr
from nzat.qgis.rgba import rgb_call
from nzat.qgis.settings_props import settings_props
from nzat.qgis.size_floor import size_floor
from nzat.qgis.upright_style_name import upright_style_name

# Topo50 sets natural-feature and water names in italic. Narrow upright is a
# settlement or area name, so it stays Regular.
NATURAL_TEST = "lower(coalesce(\"style\", '')) LIKE '%italic%'"
# Spot heights stay black, so they do not read as index-brown contour numbers (log 0081).
SPOT_HEIGHT_TEST = (
    "regexp_match(trim(coalesce(\"text_string\", '')), '^[0-9]+(\\\\.[0-9]+)?m?$')"
)


def _style_expr(style=None):
    style = style or STYLE
    regular = style["fonts"]["raster_upright_style"]
    natural = style["fonts"]["raster_natural_style"]
    return (
        f"CASE WHEN {NATURAL_TEST} THEN '{natural}'"
        f" WHEN lower(coalesce(\"style\", '')) LIKE '%bold%' THEN 'Bold'"
        f" WHEN lower(coalesce(\"style\", '')) LIKE '%narrow%' THEN '{regular}'"
        f" WHEN coalesce(\"style\", '') = '' THEN '{regular}'"
        ' ELSE "style" END'
    )


def patch_labels(layer, layer_name, style=None, palette=None, fit=None, urban=None):
    style = style or STYLE
    family = style["fonts"]["raster_family"]
    labels = style["labels"]
    spot = labels["spot_height_layer_contains"]
    floor = int(
        labels["spot_height_floor_pt"]
        if layer_name and spot in layer_name
        else labels["size_floor_pt"]
    )
    count = 0
    for text_style in layer.findall(".//text-style"):
        text_style.set(
            "namedStyle", upright_style_name(text_style.get("namedStyle"), style)
        )
        text_style.set("fontItalic", "0")
        text_style.set("fontFamily", family)
        if text_style.get("fontSize") is not None:
            text_style.set(
                "fontSize", size_floor(layer_name, text_style.get("fontSize"), style)
            )
        count += 1
    size_expr = f'max({floor}, coalesce("size", {floor}))'
    if layer_name == CARTO_TEXT_LAYER:
        # Spot heights are carto_text here. They keep the 6 pt rank below names (G4, log 0084).
        spot_floor = int(labels["spot_height_floor_pt"])
        size_expr = (
            f"CASE WHEN {SPOT_HEIGHT_TEST}"
            f' THEN max({spot_floor}, coalesce("size", {spot_floor}))'
            f" ELSE {size_expr} END"
        )
    for dd in layer.findall(".//dd_properties"):
        option = dd.find("Option")
        if option is None:
            continue
        props = option.find("Option[@name='properties']")
        if props is None or props.get("type") != "Map":
            continue
        present = {child.get("name") for child in props}
        if "Family" in present:
            put_expr(props, "Family", f"'{family}'")
        if "FontStyle" in present:
            put_expr(props, "FontStyle", _style_expr(style))
        if "Size" in present:
            put_expr(props, "Size", size_expr)
        if layer_name == CARTO_TEXT_LAYER and "CurvedLabelMode" in present:
            put_expr(props, "CurvedLabelMode", curved_label_mode_expression(style))
    if layer_name == CARTO_TEXT_LAYER:
        patch_wrap_baseline(layer)
        patch_carto_point_labels(layer, style, fit)
    patch_label_contrast(layer, style, palette)
    if layer_name == CARTO_TEXT_LAYER:
        _paint_natural_names(layer, style)
        if urban:
            _paint_urban_halos(layer, style, urban)
    return count


def _paint_natural_names(layer, style):
    """Black italic names take the natural ink. The face has no Bold file (log 0072)."""
    red, green, blue = (
        int(style["labels"]["natural_colour"][i : i + 2], 16) for i in (1, 3, 5)
    )
    natural = f"color_rgb({red},{green},{blue})"
    for dd in layer.findall(".//dd_properties"):
        props = dd.find("Option/Option[@name='properties']")
        if props is None or props.get("type") != "Map":
            continue
        current = expr(props, "Color")
        if not current:
            continue
        put_expr(
            props,
            "Color",
            f"CASE WHEN \"colour\" = 'black' AND {NATURAL_TEST}"
            f" AND NOT {SPOT_HEIGHT_TEST} THEN {natural}"
            f" ELSE {current} END",
        )


def _paint_urban_halos(layer, style, urban):
    """Black names inside the urban fill take an urban-fill halo, not a white hole (G4, log 0093).

    The ids come from urban_text.json. A layer lookup in a label expression hangs the render (log 0090).
    Coloured names keep the paper halo: brown and blue are under 3.4:1 on the urban fill.
    """
    ids = ", ".join(
        "'" + str(ident).replace("'", "''") + "'" for ident in sorted(urban)
    )
    fill = rgb_call(style["reference_inks"]["urban_fill"])
    for settings in layer.findall(".//settings"):
        buffer_el = settings.find("text-style/text-buffer")
        props = settings_props(settings)
        if buffer_el is None or buffer_el.get("bufferDraw") != "1" or props is None:
            continue
        parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
        if parsed is None:
            continue
        paper = "color_rgb({},{},{})".format(*parsed[:3])
        put_expr(
            props,
            "BufferColor",
            f'CASE WHEN "id" IN ({ids}) AND "colour" = \'black\''
            f" AND NOT ({NATURAL_TEST} AND NOT {SPOT_HEIGHT_TEST})"
            f" THEN {fill} ELSE {paper} END",
        )
