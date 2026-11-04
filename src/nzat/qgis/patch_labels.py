from nzat.qgis.curved_label_mode_expression import curved_label_mode_expression
from nzat.qgis.defaults import CARTO_TEXT_LAYER, STYLE
from nzat.qgis.expr import expr
from nzat.qgis.patch_carto_point_labels import patch_carto_point_labels
from nzat.qgis.patch_label_contrast import patch_label_contrast
from nzat.qgis.patch_wrap_baseline import patch_wrap_baseline
from nzat.qgis.put_expr import put_expr
from nzat.qgis.size_floor import size_floor
from nzat.qgis.upright_style_name import upright_style_name

# Topo50 sets natural-feature and water names in italic. Narrow upright is a
# settlement or area name, so it stays Regular.
NATURAL_TEST = "lower(coalesce(\"style\", '')) LIKE '%italic%'"


def _style_expr(style=None):
    style = style or STYLE
    regular = style["fonts"]["raster_upright_style"]
    natural = style["fonts"]["raster_natural_style"]
    return (
        f"CASE WHEN {NATURAL_TEST} THEN '{natural}'"
        f" WHEN lower(coalesce(\"style\", '')) LIKE '%narrow%' THEN '{regular}'"
        f" WHEN coalesce(\"style\", '') = '' THEN '{regular}'"
        ' ELSE "style" END'
    )


def patch_labels(layer, layer_name, style=None, palette=None, fit=None):
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
            f"CASE WHEN \"colour\" = 'black' AND {NATURAL_TEST} THEN {natural}"
            f" ELSE {current} END",
        )
