import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_water_line import patch_water_line, water_line_width_expression


def test_stream_width_reads_the_navigation_floor():
    # Catches a stream width below sizes.navigation_line_mm or a drain raised with it.
    assert STYLE["sizes"]["navigation_line_mm"] == 0.35
    assert STYLE["water"]["stream_width_mm"] == STYLE["sizes"]["navigation_line_mm"]
    assert STYLE["water"]["drain_width_mm"] == 0.15
    expression = water_line_width_expression(STYLE["water"])
    assert "0.35" in expression
    assert "0.15" in expression
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>water_line map</layername>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <data_defined_properties><Option type="Map">
                  <Option name="properties"/>
                </Option></data_defined_properties>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_water_line(layer)
    expr = layer.find(".//Option[@name='outlineWidth']/Option[@name='expression']").get(
        "value"
    )
    assert expr == expression
