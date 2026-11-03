import xml.etree.ElementTree as ET

from nzat.qgis.is_owned_road_layer import is_owned_road_layer
from nzat.qgis.patch_contour_numbers import patch_contour_numbers
from nzat.qgis.patch_road_fills import patch_road_fills


def test_road_fills_and_contour_numbers_read_the_style_file():
    # Catches a PMS151 road fill left unpainted, or a contour number left in road orange.
    assert is_owned_road_layer("road_line 2 lane map") is True
    assert is_owned_road_layer("road_line 1 lane sealed map") is True
    assert is_owned_road_layer("road_line 2 lane highway map") is False
    assert is_owned_road_layer("road_line 2 lane background map") is False
    road = ET.fromstring(
        """
        <maplayer>
          <layername>road_line 2 lane map</layername>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,127,0,255"/>
                </Option>
              </layer>
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="35,35,35,255"/>
                </Option>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_road_fills(road)
    colours = [
        opt.get("value") for opt in road.findall(".//Option[@name='line_color']")
    ]
    assert colours[0].startswith("236,112,0")
    assert colours[1].startswith("35,35,35")
    carto = ET.fromstring(
        """
        <maplayer>
          <layername>nztopo50_carto_symbol</layername>
          <renderer-v2 type="RuleRenderer">
            <rules>
              <rule filter="&quot;type&quot; = 'contour_number'" symbol="3"/>
            </rules>
            <symbols>
              <symbol name="3" type="marker">
                <layer class="FontMarker">
                  <Option type="Map">
                    <Option name="chr" type="QString" value="A"/>
                    <Option name="color" type="QString" value="255,127,0,255"/>
                  </Option>
                </layer>
              </symbol>
            </symbols>
          </renderer-v2>
        </maplayer>
        """
    )
    patch_contour_numbers(carto)
    color = carto.find(".//Option[@name='color']").get("value")
    assert color.startswith("122,85,66")
