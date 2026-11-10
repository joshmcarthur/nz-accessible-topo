from nzat.qgis.defaults import ONE_LANE_CASING_LAYER
from nzat.qgis.is_owned_road_layer import is_owned_road_layer
from nzat.qgis.load_carto_fit import load_carto_fit
from nzat.qgis.load_urban_text import load_urban_text
from nzat.qgis.patch_contour import patch_contour
from nzat.qgis.patch_contour_numbers import patch_contour_numbers
from nzat.qgis.patch_draw_order import patch_draw_order
from nzat.qgis.patch_hillshade import patch_hillshade
from nzat.qgis.patch_labels import patch_labels
from nzat.qgis.patch_landcover import patch_landcover
from nzat.qgis.patch_legend_picture import patch_legend_picture
from nzat.qgis.patch_map_themes import patch_map_themes
from nzat.qgis.patch_owned_lines import patch_owned_lines
from nzat.qgis.patch_railway import patch_railway
from nzat.qgis.patch_relief_point import patch_relief_point
from nzat.qgis.patch_road_fills import patch_road_fills
from nzat.qgis.patch_road_widths import patch_one_lane_casing, patch_road_widths
from nzat.qgis.patch_shield_numbers import patch_shield_numbers
from nzat.qgis.patch_springs import patch_springs
from nzat.qgis.patch_structures import (
    install_owned_symbols,
    patch_building,
    patch_building_point,
    patch_structure_line,
    patch_structure_point,
)
from nzat.qgis.patch_thin_lines import patch_thin_lines
from nzat.qgis.patch_tracks import patch_tracks
from nzat.qgis.patch_vegetation import patch_vegetation
from nzat.qgis.patch_water_line import patch_water_line
from nzat.qgis.project_palette import project_palette


def _mask_contour_casing(root):
    contour = None
    for layer in root.findall("projectlayers/maplayer"):
        if (layer.findtext("layername") or "") == "contour":
            contour = layer
            break
    if contour is None:
        return
    lines = contour.findall("renderer-v2/symbols/symbol/layer[@class='SimpleLine']")
    if len(lines) < 2:
        return
    fill_id = lines[1].get("id")
    casing_id = lines[0].get("id")
    if not fill_id or not casing_id:
        return
    layer_id = contour.findtext("id") or ""
    token = f"{layer_id};{casing_id}" if layer_id else casing_id
    for mask in root.iter("text-mask"):
        current = mask.get("maskedSymbolLayers") or ""
        if fill_id in current and casing_id not in current:
            mask.set("maskedSymbolLayers", current + ";" + token)


def apply(root, project_dir=None):
    """Patch map layers. Return a count of label styles touched."""
    layers = root.find("projectlayers")
    if layers is None:
        raise RuntimeError("project has no projectlayers")
    labels = 0
    seen = set()
    palette = project_palette(root)
    fit = load_carto_fit(project_dir)
    urban = load_urban_text(project_dir)
    for layer in layers.findall("maplayer"):
        name = layer.findtext("layername") or ""
        labels += patch_labels(layer, name, palette=palette, fit=fit, urban=urban)
        if name == "contour":
            patch_contour(layer)
            seen.add(name)
        elif is_owned_road_layer(name):
            patch_road_fills(layer)
            patch_road_widths(layer)
        elif name == ONE_LANE_CASING_LAYER:
            patch_one_lane_casing(layer)
        elif name == "nztopo50_carto_symbol":
            patch_contour_numbers(layer)
        elif name == "track_line map":
            patch_tracks(layer)
            seen.add(name)
        elif name in ("vegetation map", "vegetation_point map"):
            patch_vegetation(layer)
            seen.add(name)
        elif name == "water_point":
            patch_springs(layer)
            seen.add(name)
        elif name == "water_line map":
            patch_water_line(layer)
            seen.add(name)
        elif name == "structure_point map":
            patch_structure_point(layer)
            seen.add(name)
        elif name in ("structure_line", "structure_line map"):
            patch_structure_line(layer)
        elif name == "building_point map":
            patch_building_point(layer)
        elif name == "building map":
            patch_building(layer)
        elif name == "railway_line map":
            patch_railway(layer)
        elif name == "landcover map":
            patch_landcover(layer)
        elif name == "relief_point map":
            patch_relief_point(layer)
        patch_owned_lines(layer)
        patch_thin_lines(layer)
    missing = {
        "contour",
        "track_line map",
        "vegetation map",
        "vegetation_point map",
        "water_point",
        "water_line map",
        "structure_point map",
    } - seen
    if missing:
        raise RuntimeError(f"missing layers: {', '.join(sorted(missing))}")
    _mask_contour_casing(root)
    patch_shield_numbers(root)
    patch_draw_order(root)
    patch_hillshade(root, project_dir)
    patch_legend_picture(root)
    patch_map_themes(root)
    if project_dir:
        install_owned_symbols(project_dir)
    return labels
