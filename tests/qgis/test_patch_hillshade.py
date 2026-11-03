import os
import tempfile
import xml.etree.ElementTree as ET

from nzat.qgis.defaults import DEM_LAYER_ID, DEM_LAYER_NAME
from nzat.qgis.hillshade_rules import hillshade_rules
from nzat.qgis.hillshade_should_paint import hillshade_should_paint
from nzat.qgis.patch_hillshade import patch_hillshade
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.vector_params import P

RULES = load_rules()


def test_hillshade_is_an_optional_overlay():
    # Catches azimuth other than 337.5, a missing painted flag, a raster file other than dem.tif, or hillshade_direction left in P.
    shade = RULES["hillshade"]
    assert shade["painted"] is True
    assert shade["raster_file"] == "dem.tif"
    assert shade["azimuth_deg"] == 337.5
    assert shade["altitude_deg"] == 45
    assert shade["multidirectional"] is True
    assert shade["fill_azimuths_deg"] == [292.5, 22.5]
    assert "hillshade_direction" not in P
    assert lookup_style_path(RULES, "hillshade.azimuth_deg") == 337.5
    assert lookup_style_path(RULES, "hillshade.fill_azimuths_deg") == [292.5, 22.5]
    assert lookup_style_path(RULES, "hillshade.painted") is True
    assert DEM_LAYER_NAME == "dem"
    assert hillshade_should_paint(None) is False


def test_hillshade_stays_off_without_a_dem():
    # Catches the shader left on, or the light left at 315, when dem.tif is missing.
    root = ET.fromstring(
        """
        <qgis>
          <projectCrs><spatialrefsys><srid>2193</srid></spatialrefsys></projectCrs>
          <elevation-shading-renderer hillshading-is-active="1" hillshading-is-multidirectional="0" hillshading-z-factor="1" is-active="1" light-altitude="45" light-azimuth="315"/>
          <layer-tree-group/>
          <projectlayers/>
          <ElevationProperties>
            <terrainProvider type="flat"><TerrainProvider offset="0" scale="1"/></terrainProvider>
          </ElevationProperties>
        </qgis>
        """
    )
    patch_hillshade(root, project_dir="/tmp/missing-nzat-dem")
    renderer = root.find("elevation-shading-renderer")
    assert renderer.get("light-azimuth") == "337.5"
    assert renderer.get("light-altitude") == "45"
    assert renderer.get("hillshading-is-multidirectional") == "1"
    assert renderer.get("is-active") == "0"
    assert renderer.get("hillshading-is-active") == "0"
    assert root.find("projectlayers/maplayer[layername='dem']") is None


def test_hillshade_turns_on_when_dem_is_present():
    # Catches a present dem.tif that does not turn the shader on, or a painted false that still shades.
    root = ET.fromstring(
        """
        <qgis>
          <projectCrs><spatialrefsys><srid>2193</srid></spatialrefsys></projectCrs>
          <elevation-shading-renderer hillshading-is-active="0" hillshading-is-multidirectional="0" hillshading-z-factor="1" is-active="0" light-altitude="45" light-azimuth="315"/>
          <layer-tree-group/>
          <projectlayers/>
          <ElevationProperties>
            <terrainProvider type="flat"><TerrainProvider offset="0" scale="1"/></terrainProvider>
          </ElevationProperties>
        </qgis>
        """
    )
    with tempfile.TemporaryDirectory() as folder:
        open(os.path.join(folder, "dem.tif"), "wb").close()
        patch_hillshade(root, project_dir=folder)
        off = {"hillshade": {**hillshade_rules(), "painted": False}}
        assert hillshade_should_paint(folder, off) is False
    renderer = root.find("elevation-shading-renderer")
    assert renderer.get("is-active") == "1"
    assert renderer.get("hillshading-is-active") == "1"
    assert (
        root.find("projectlayers/maplayer[layername='dem']/datasource").text
        == "./dem.tif"
    )
    assert root.find("ElevationProperties/terrainProvider").get("type") == "raster"
    assert (
        root.find("ElevationProperties/terrainProvider/TerrainProvider").get("layer")
        == DEM_LAYER_ID
    )
