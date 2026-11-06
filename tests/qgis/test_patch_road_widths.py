import xml.etree.ElementTree as ET

from nzat.qgis.patch_road_fills import patch_road_fills
from nzat.qgis.patch_road_widths import patch_road_widths


def test_road_fills_rise_to_the_navigation_floor():
    # Catches a metalled one-lane fill left at 0.26 mm or an expression below 0.35 mm.
    road = ET.fromstring(
        """
        <maplayer>
          <layername>road_line 1 lane metalled map</layername>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,127,0,255"/>
                  <Option name="line_width" type="QString" value="0.26"/>
                </Option>
              </layer>
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,255,255,255"/>
                  <Option name="line_width" type="QString" value="0.25"/>
                </Option>
              </layer>
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,127,0,255"/>
                  <Option name="line_width" type="QString" value="0.25"/>
                  <Option name="use_custom_dash" type="QString" value="0"/>
                </Option>
                <data_defined_properties><Option type="Map">
                  <Option name="properties" type="Map">
                    <Option name="outlineWidth" type="Map">
                      <Option name="expression" type="QString" value="0.35764*(&quot;lane_count&quot;)"/>
                    </Option>
                  </Option>
                </Option></data_defined_properties>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_road_fills(road)
    patch_road_widths(road)
    widths = [
        layer.find("Option/Option[@name='line_width']").get("value")
        for layer in road.findall(".//layer[@class='SimpleLine']")
    ]
    assert widths[0] == "0.35"
    assert widths[1] == "0.35"
    expr = road.find(".//Option[@name='outlineWidth']/Option[@name='expression']").get(
        "value"
    )
    assert expr == 'max(0.35, 0.35764*("lane_count"))'
    patch_road_widths(road)
    assert expr == 'max(0.35, 0.35764*("lane_count"))'
