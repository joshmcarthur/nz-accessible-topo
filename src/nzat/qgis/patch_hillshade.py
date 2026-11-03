import copy
import xml.etree.ElementTree as ET

from nzat.qgis.defaults import DEM_LAYER_ID, DEM_LAYER_NAME
from nzat.qgis.hillshade_rules import hillshade_rules
from nzat.qgis.hillshade_should_paint import hillshade_should_paint


def _copy_project_srs(root):
    source = root.find("projectCrs/spatialrefsys")
    if source is None:
        raise RuntimeError("project has no projectCrs")
    return copy.deepcopy(source)


def _ensure_dem_layer(root, style=None):
    layers = root.find("projectlayers")
    if layers is None:
        raise RuntimeError("project has no projectlayers")
    rules = hillshade_rules(style)
    existing = None
    for layer in layers.findall("maplayer"):
        if layer.findtext("layername") == DEM_LAYER_NAME:
            existing = layer
            break
    if existing is None:
        layer = ET.SubElement(layers, "maplayer")
        layer.set("type", "raster")
        layer.set("styleCategories", "AllStyleCategories")
        ident = ET.SubElement(layer, "id")
        ident.text = DEM_LAYER_ID
        name = ET.SubElement(layer, "layername")
        name.text = DEM_LAYER_NAME
        provider = ET.SubElement(layer, "provider")
        provider.text = "gdal"
        srs = ET.SubElement(layer, "srs")
        srs.append(_copy_project_srs(root))
        pipe = ET.SubElement(layer, "pipe")
        renderer = ET.SubElement(pipe, "rasterrenderer")
        renderer.set("type", "singlebandgray")
        renderer.set("opacity", "0")
        renderer.set("grayBand", "1")
        elevation = ET.SubElement(layer, "elevation")
        elevation.set("enabled", "1")
        elevation.set("mode", "RepresentsElevationSurface")
        elevation.set("band", "1")
        tree = root.find("layer-tree-group")
        if tree is not None:
            node = ET.SubElement(tree, "layer-tree-layer")
            node.set("checked", "Qt::Unchecked")
            node.set("expanded", "0")
            node.set("id", DEM_LAYER_ID)
            node.set("name", DEM_LAYER_NAME)
            node.set("providerKey", "gdal")
            node.set("source", f"./{rules['raster_file']}")
        existing = layer
    datasource = existing.find("datasource")
    if datasource is None:
        datasource = ET.SubElement(existing, "datasource")
    datasource.text = f"./{rules['raster_file']}"


def _set_raster_terrain(root):
    props = root.find("ElevationProperties")
    if props is None:
        props = ET.SubElement(root, "ElevationProperties")
    provider = props.find("terrainProvider")
    if provider is None:
        provider = ET.SubElement(props, "terrainProvider")
    provider.set("type", "raster")
    inner = provider.find("TerrainProvider")
    if inner is None:
        inner = ET.SubElement(provider, "TerrainProvider")
        inner.set("offset", "0")
        inner.set("scale", "1")
    inner.set("layer", DEM_LAYER_ID)


def patch_hillshade(root, project_dir=None, style=None):
    """Write R-03 lights onto the project shader. Turn it on only when dem.tif is present."""
    renderer = root.find("elevation-shading-renderer")
    if renderer is None:
        return
    rules = hillshade_rules(style)
    renderer.set("light-azimuth", str(rules["azimuth_deg"]))
    renderer.set("light-altitude", str(rules["altitude_deg"]))
    renderer.set(
        "hillshading-is-multidirectional", "1" if rules["multidirectional"] else "0"
    )
    renderer.set("hillshading-z-factor", str(rules["z_factor"]))
    on = hillshade_should_paint(project_dir, style)
    renderer.set("is-active", "1" if on else "0")
    renderer.set("hillshading-is-active", "1" if on else "0")
    if on:
        _ensure_dem_layer(root, style)
        _set_raster_terrain(root)
