import xml.etree.ElementTree as ET

from nzat.qgis.patch_contour import patch_contour
from nzat.style.index_line_width import index_line_width
from nzat.style.intermediate_casing_width import intermediate_casing_width
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path

RULES = load_rules()


def test_contour_casing_read_the_style_file():
    # Catches an intermediate contour with no index-ink casing, or a vector casing that ignores the JSON.
    mid = RULES["contours"]["intermediate"]
    assert mid["casing_colour"] == "#7A5542"
    assert mid["casing_width_mm"] == 0.2
    assert RULES["contours"]["index"]["width_mm"] == 0.35
    assert lookup_style_path(RULES, "contours.index.colour") == "#7A5542"
    assert lookup_style_path(RULES, "contours.intermediate.colour") == "#B08872"
    assert lookup_style_path(RULES, "contours.index.alpha") == 0.85
    assert lookup_style_path(RULES, "contours.intermediate.alpha") == 0.5
    assert lookup_style_path(RULES, "contours.intermediate.casing_colour") == "#7A5542"
    assert intermediate_casing_width(RULES)["stops"] == [[12, 1.0], [16, 1.5]]
    assert index_line_width(RULES)["stops"] == [[10, 1.01], [12, 1.48], [15, 2.26]]
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>contour</layername>
          <fieldConfiguration><field name="elevation"/></fieldConfiguration>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,127,0,255"/>
                  <Option name="line_width" type="QString" value="0.12"/>
                </Option>
                <data_defined_properties><Option type="Map">
                  <Option name="properties"/>
                </Option></data_defined_properties>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_contour(layer)
    lines = layer.findall(".//layer[@class='SimpleLine']")
    assert len(lines) == 2
    enabled = lines[0].find(
        "data_defined_properties//Option[@name='enabled']/Option[@name='expression']"
    )
    assert "% 100 <> 0" in enabled.get("value")
    width = lines[0].find(
        "data_defined_properties//Option[@name='outlineWidth']/Option[@name='expression']"
    )
    assert width.get("value") == "0.2"
    fill_width = lines[1].find(
        "data_defined_properties//Option[@name='outlineWidth']/Option[@name='expression']"
    )
    assert "0.35" in fill_width.get("value")
    assert "0.12" in fill_width.get("value")
    casing_color = lines[0].find(
        "data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']"
    )
    fill_color = lines[1].find(
        "data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']"
    )
    assert casing_color.get("value") == "color_rgba(122,85,66,128)"
    assert "color_rgba(122,85,66,217)" in fill_color.get("value")
    assert "color_rgba(176,136,114,128)" in fill_color.get("value")
    assert (
        lines[0].find("Option/Option[@name='line_color']").get("value")
        == "122,85,66,128"
    )
