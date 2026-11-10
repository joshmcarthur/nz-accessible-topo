import xml.etree.ElementTree as ET

from nzat.qgis.patch_road_fills import patch_road_fills
from nzat.qgis.patch_road_widths import patch_one_lane_casing, patch_road_widths


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
                      <Option name="active" type="bool" value="true"/>
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
    # The white centre keeps the stock width, so the dark edges stay (log 0113).
    assert widths[1] == "0.25"
    expr = road.find(".//Option[@name='outlineWidth']/Option[@name='expression']").get(
        "value"
    )
    assert expr == 'max(0.35, 0.35764*("lane_count"))'
    patch_road_widths(road)
    assert expr == 'max(0.35, 0.35764*("lane_count"))'


def _line(width, extra=""):
    return ET.fromstring(
        f"""
        <maplayer><renderer-v2 type="singleSymbol"><symbols><symbol name="0" type="line">
          <layer class="SimpleLine">
            <Option type="Map">
              <Option name="line_color" type="QString" value="255,127,0,255"/>
              <Option name="line_width" type="QString" value="{width}"/>
            </Option>
            {extra}
          </layer>
        </symbol></symbols></renderer-v2></maplayer>
        """
    )


def test_inactive_stock_width_expression_stays_off():
    # Catches the fill growing to the casing width: roads lost their dark edge (log 0111).
    road = _line(
        "0.45",
        """<data_defined_properties><Option type="Map"><Option name="properties" type="Map">
          <Option name="outlineWidth" type="Map">
            <Option name="active" type="bool" value="false"/>
            <Option name="expression" type="QString" value="0.35764*(&quot;lane_count&quot;)"/>
          </Option>
        </Option></Option></data_defined_properties>""",
    )
    patch_road_widths(road)
    node = road.find(".//Option[@name='outlineWidth']")
    assert node.find("Option[@name='active']").get("value") == "false"
    assert node.find("Option[@name='expression']").get("value").startswith("0.35764")


def test_one_lane_casing_widens_with_the_raised_fill():
    casing = _line("0.5")
    patch_one_lane_casing(casing)
    assert casing.find(".//Option[@name='line_width']").get("value") == "0.6"
