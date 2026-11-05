import xml.etree.ElementTree as ET

from nzat.qgis.patch_owned_lines import patch_owned_lines


def test_owned_lines_rewrite_stock_rgb():
    # Catches a process-blue stream, lime shelterbelt, or grid line left at Map5View RGB.
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>water_line map</layername>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="0,158,255,255"/>
                </Option>
              </layer>
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="148,255,59,255"/>
                </Option>
              </layer>
              <layer class="SimpleMarker">
                <Option type="Map">
                  <Option name="color" type="QString" value="41,160,211,255"/>
                  <Option name="outline_color" type="QString" value="35,35,35,255"/>
                </Option>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_owned_lines(layer)
    colours = [
        opt.get("value") for opt in layer.findall(".//Option[@name='line_color']")
    ]
    assert colours[0].startswith("0,76,153")
    assert colours[1].startswith("29,157,0")
    marker = layer.find(".//Option[@name='color']").get("value")
    outline = layer.find(".//Option[@name='outline_color']").get("value")
    assert marker.startswith("38,159,210")
    assert outline.startswith("35,35,35")
