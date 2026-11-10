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
    assert lookup_style_path(RULES, "contours.index.alpha") == 1.0
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
    assert "color_rgba(122,85,66,255)" in fill_color.get("value")
    assert "color_rgba(176,136,114,128)" in fill_color.get("value")
    assert (
        lines[0].find("Option/Option[@name='line_color']").get("value")
        == "122,85,66,128"
    )
    assert layer.find(".//layer[@class='MarkerLine']") is None
    assert (
        lines[1].find(
            "data_defined_properties//Option[@name='customDash']/Option[@name='expression']"
        )
        is None
    )


CONTOUR_CLASS_XML = """
        <maplayer>
          <layername>contour</layername>
          <fieldConfiguration>
            <field name="elevation"/>
            <field name="designation"/>
            <field name="formation"/>
          </fieldConfiguration>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,127,0,255"/>
                  <Option name="line_width" type="QString" value="0.12"/>
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


def test_supplementary_contours_dash_and_depressions_gain_ticks():
    # Catches a solid supplementary contour, orange depression ticks, or lost elevation colour.
    layer = ET.fromstring(CONTOUR_CLASS_XML)
    patch_contour(layer)
    lines = layer.findall(".//layer[@class='SimpleLine']")
    assert len(lines) == 2
    fill_width = lines[1].find(
        "data_defined_properties//Option[@name='outlineWidth']/Option[@name='expression']"
    )
    fill_color = lines[1].find(
        "data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']"
    )
    assert "0.35" in fill_width.get("value")
    assert "elevation" in fill_width.get("value")
    assert "color_rgba(122,85,66,255)" in fill_color.get("value")
    # Catches a depression contour left in the pale intermediate ink (log 0114).
    assert "'depression'" in fill_color.get("value").split("THEN")[0]
    dash = lines[1].find(
        "data_defined_properties//Option[@name='customDash']/Option[@name='expression']"
    )
    use_dash = lines[1].find(
        "data_defined_properties//Option[@name='useCustomDash']/Option[@name='expression']"
    )
    assert "3;1" in dash.get("value")
    # A normal contour must not take the stock 5;2 dash (log 0110).
    assert "'5;2'" not in dash.get("value")
    assert "'10000;0'" in dash.get("value")
    assert "coalesce" in dash.get("value")
    assert "supplementary" in dash.get("value")
    assert "coalesce" in use_dash.get("value")
    casing_dash = lines[0].find(
        "data_defined_properties//Option[@name='customDash']/Option[@name='expression']"
    )
    assert "3;1" in casing_dash.get("value")
    ticks = layer.findall(".//layer[@class='MarkerLine']")
    assert len(ticks) == 1
    enabled = ticks[0].find(
        "data_defined_properties//Option[@name='enabled']/Option[@name='expression']"
    )
    assert "coalesce" in enabled.get("value")
    assert "depression" in enabled.get("value")
    size = ticks[0].find(
        "symbol/layer[@class='SimpleMarker']/Option/Option[@name='size']"
    )
    colour = ticks[0].find(
        "symbol/layer[@class='SimpleMarker']/Option/Option[@name='outline_color']"
    )
    assert size.get("value") == "0.6"
    assert colour.get("value").startswith("122,85,66")
    painted = ET.tostring(layer, encoding="unicode")
    assert "255,127,0" not in painted or "FF7F00" not in painted.upper()
    patch_contour(layer)
    assert len(layer.findall(".//layer[@class='MarkerLine']")) == 1
