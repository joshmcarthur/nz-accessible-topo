import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_railway import patch_railway

RAIL_XML = """
<maplayer>
  <layername>railway_line map</layername>
  <fieldConfiguration><field name="track_type"/></fieldConfiguration>
  <renderer-v2 type="singleSymbol"><symbols>
    <symbol name="0" type="line">
      <layer class="SimpleLine">
        <Option type="Map">
          <Option name="line_color" type="QString" value="0,0,0,255"/>
          <Option name="line_width" type="QString" value="0.25"/>
          <Option name="customdash" type="QString" value="5;2"/>
          <Option name="use_custom_dash" type="QString" value="0"/>
        </Option>
        <data_defined_properties><Option type="Map">
          <Option name="properties"/>
        </Option></data_defined_properties>
      </layer>
    </symbol>
  </symbols></renderer-v2>
</maplayer>
"""


def test_multiple_track_is_a_black_bar_with_white_dashes():
    # Catches double track left at the 0.25 mm single-track width, or white dashes on every railway.
    layer = ET.fromstring(RAIL_XML)
    patch_railway(layer)
    spec = STYLE["railway"]
    black = layer.find(".//symbol[@name='0']/layer[@class='SimpleLine']")
    width = black.find(
        "data_defined_properties//Option[@name='outlineWidth']/Option[@name='expression']"
    )
    assert str(spec["single_width_mm"]) in width.get("value")
    assert str(spec["multiple_width_mm"]) in width.get("value")
    assert "coalesce" in width.get("value")
    assert "multiple" in width.get("value")
    whites = [
        line
        for line in layer.findall(".//symbol[@name='0']/layer[@class='SimpleLine']")
        if (
            line.find("Option/Option[@name='line_color']").get("value") or ""
        ).startswith("255,255,255")
    ]
    assert len(whites) == 1
    white = whites[0]
    assert white.find("Option/Option[@name='line_width']").get("value") == str(
        spec["dash_width_mm"]
    )
    assert white.find("Option/Option[@name='customdash']").get("value") == spec["dash"]
    assert white.find("Option/Option[@name='use_custom_dash']").get("value") == "1"
    enabled = white.find(
        "data_defined_properties//Option[@name='enabled']/Option[@name='expression']"
    )
    assert "coalesce" in enabled.get("value")
    assert "multiple" in enabled.get("value")
    patch_railway(layer)
    whites = [
        line
        for line in layer.findall(".//symbol[@name='0']/layer[@class='SimpleLine']")
        if (
            line.find("Option/Option[@name='line_color']").get("value") or ""
        ).startswith("255,255,255")
    ]
    assert len(whites) == 1
