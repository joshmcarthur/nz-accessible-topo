import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_map_themes import ALL_THEME, PAPER_THEME, patch_map_themes


def test_map_themes_paper_keeps_hidden_layers_and_all_shows_them():
    # Catches Map5View-all leaving water_point off, or -paper turning it on.
    root = ET.fromstring(
        """
        <qgis>
          <projectlayers>
            <maplayer>
              <id>water_point_id</id>
              <layername>water_point</layername>
            </maplayer>
            <maplayer>
              <id>structure_point_id</id>
              <layername>structure_point</layername>
            </maplayer>
            <maplayer>
              <id>structure_point_map_id</id>
              <layername>structure_point map</layername>
            </maplayer>
            <maplayer>
              <id>contour_id</id>
              <layername>contour</layername>
            </maplayer>
            <maplayer>
              <id>relief_line_id</id>
              <layername>relief_line map</layername>
            </maplayer>
          </projectlayers>
          <visibility-presets>
            <visibility-preset name="Map5View">
              <layer expanded="1" id="contour_id" style="default" visible="1"/>
              <layer expanded="1" id="relief_line_id" style="default" visible="1"/>
              <checked-legend-nodes id="relief_line_id"/>
            </visibility-preset>
          </visibility-presets>
        </qgis>
        """
    )
    patch_map_themes(root)
    names = [
        preset.get("name")
        for preset in root.findall("visibility-presets/visibility-preset")
    ]
    assert PAPER_THEME in names
    assert ALL_THEME in names
    assert STYLE["map"]["theme_paper"] == PAPER_THEME
    paper = root.find(f"visibility-presets/visibility-preset[@name='{PAPER_THEME}']")
    all_preset = root.find(f"visibility-presets/visibility-preset[@name='{ALL_THEME}']")
    paper_ids = {
        layer.get("id"): layer.get("visible") for layer in paper.findall("layer")
    }
    all_ids = {
        layer.get("id"): layer.get("visible") for layer in all_preset.findall("layer")
    }
    assert "water_point_id" not in paper_ids
    assert all_ids["water_point_id"] == "1"
    assert "structure_point_id" not in all_ids
    assert "structure_point_map_id" not in all_ids
    assert paper.find("checked-legend-nodes[@id='relief_line_id']") is not None
    assert all_preset.find("checked-legend-nodes[@id='relief_line_id']") is None
