from nzat.qgis.is_owned_road_layer import is_owned_road_layer
from nzat.qgis.load_carto_fit import load_carto_fit
from nzat.qgis.patch_contour import patch_contour
from nzat.qgis.patch_contour_numbers import patch_contour_numbers
from nzat.qgis.patch_draw_order import patch_draw_order
from nzat.qgis.patch_hillshade import patch_hillshade
from nzat.qgis.patch_labels import patch_labels
from nzat.qgis.patch_legend_picture import patch_legend_picture
from nzat.qgis.patch_owned_lines import patch_owned_lines
from nzat.qgis.patch_road_fills import patch_road_fills
from nzat.qgis.patch_shield_numbers import patch_shield_numbers
from nzat.qgis.patch_springs import patch_springs
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
    for layer in layers.findall("maplayer"):
        name = layer.findtext("layername") or ""
        labels += patch_labels(layer, name, palette=palette, fit=fit)
        if name == "contour":
            patch_contour(layer)
            seen.add(name)
        elif is_owned_road_layer(name):
            patch_road_fills(layer)
        elif name == "nztopo50_carto_symbol":
            patch_contour_numbers(layer)
        elif name == "track_line map":
            patch_tracks(layer)
            seen.add(name)
        elif name == "vegetation map":
            patch_vegetation(layer)
            seen.add(name)
        elif name == "water_point":
            patch_springs(layer)
            seen.add(name)
        elif name == "water_line map":
            patch_water_line(layer)
            seen.add(name)
        patch_owned_lines(layer)
    missing = {
        "contour",
        "track_line map",
        "vegetation map",
        "water_point",
        "water_line map",
    } - seen
    if missing:
        raise RuntimeError(f"missing layers: {', '.join(sorted(missing))}")
    _mask_contour_casing(root)
    patch_shield_numbers(root)
    patch_draw_order(root)
    patch_hillshade(root, project_dir)
    patch_legend_picture(root)
    return labels
