import copy
import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE

SOURCE_THEME = "Map5View"
PAPER_THEME = "Map5View-paper"
ALL_THEME = "Map5View-all"
ALL_LAYER_NAMES = (
    "water_point",
    "structure_line",
    "structure",
    "tunnel_line",
    "landcover_point",
    "landuse",
    "marine",
    "structure_point",
)


def _source_preset(root, name):
    presets = root.find("visibility-presets")
    if presets is None:
        return None, None
    for preset in presets.findall("visibility-preset"):
        if preset.get("name") == name:
            return presets, preset
    return presets, None


def _put_preset(presets, name, source):
    for existing in list(presets.findall("visibility-preset")):
        if existing.get("name") == name:
            presets.remove(existing)
    clone = copy.deepcopy(source)
    clone.set("name", name)
    presets.append(clone)
    return clone


def _layer_ids(root):
    out = {}
    layers = root.find("projectlayers")
    if layers is None:
        return out
    for layer in layers.findall("maplayer"):
        name = layer.findtext("layername") or ""
        layer_id = layer.findtext("id")
        if layer_id:
            out[name] = layer_id
    return out


def _ensure_visible(preset, layer_id):
    for layer in preset.findall("layer"):
        if layer.get("id") == layer_id:
            layer.set("visible", "1")
            return
    ET.SubElement(
        preset,
        "layer",
        {
            "expanded": "1",
            "id": layer_id,
            "style": "default",
            "visible": "1",
        },
    )
    ET.SubElement(preset, "expanded-legend-nodes", {"id": layer_id})


def _enable_all_rules(preset, layer_id):
    for checked in list(preset.findall("checked-legend-nodes")):
        if checked.get("id") == layer_id and len(list(checked)) == 0:
            preset.remove(checked)


def patch_map_themes(root, style=None):
    """Copy Map5View to Map5View-paper and Map5View-all. Turn extra layers on in -all."""
    style = style or STYLE
    themes = style.get("map", {})
    source_name = themes.get("theme_source", SOURCE_THEME)
    paper_name = themes.get("theme_paper", PAPER_THEME)
    all_name = themes.get("theme_all", ALL_THEME)
    presets, source = _source_preset(root, source_name)
    if source is None:
        return
    _put_preset(presets, paper_name, source)
    all_preset = _put_preset(presets, all_name, source)
    ids = _layer_ids(root)
    for name in themes.get("all_layers", ALL_LAYER_NAMES):
        layer_id = ids.get(name)
        if layer_id:
            _ensure_visible(all_preset, layer_id)
    relief_id = ids.get("relief_line map")
    if relief_id:
        _ensure_visible(all_preset, relief_id)
        _enable_all_rules(all_preset, relief_id)
