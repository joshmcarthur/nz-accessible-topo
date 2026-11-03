import xml.etree.ElementTree as ET

from nzat.qgis.patch_springs import patch_springs
from nzat.qgis.patch_vegetation import patch_vegetation
from nzat.style.load_rules import load_rules
from nzat.style.spring_colour import spring_colour
from nzat.style.vegetation_fill import vegetation_fill

RULES = load_rules()


def test_springs_and_native_read_the_style_file():
    # Catches a vector native fill that ignores the JSON, or a raster spring that keeps one glyph for hot and cold.
    assert vegetation_fill("native", RULES) == "rgba(225, 234, 195, 1)"
    assert RULES["vegetation"]["native"]["colour"] == "#E1EAC3"
    assert spring_colour("hot", RULES) == "rgba(20, 20, 20, 1)"
    assert spring_colour("cold", RULES) == "rgba(0, 92, 143, 1)"
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>water_point</layername>
          <fieldConfiguration>
            <field name="type"/>
            <field name="temperature_indicator"/>
          </fieldConfiguration>
          <renderer-v2 type="categorizedSymbol" attr="feature_type">
            <categories><category value="spring" symbol="2"/></categories>
            <symbols>
              <symbol name="2" type="marker">
                <layer class="SimpleMarker">
                  <Option type="Map">
                    <Option name="name" type="QString" value="circle"/>
                  </Option>
                  <data_defined_properties><Option type="Map">
                    <Option name="properties"/>
                  </Option></data_defined_properties>
                </layer>
              </symbol>
            </symbols>
          </renderer-v2>
        </maplayer>
        """
    )
    patch_springs(layer)
    marker = layer.find(
        ".//layer[@class='SimpleMarker']/data_defined_properties/Option/Option[@name='properties']"
    )
    name_expr = marker.find("Option[@name='name']/Option[@name='expression']").get(
        "value"
    )
    assert "cross2" in name_expr
    assert "circle" in name_expr
    colour_expr = marker.find(
        "Option[@name='fillColor']/Option[@name='expression']"
    ).get("value")
    assert "20,20,20" in colour_expr.replace(
        " ", ""
    ) or "color_rgb(20,20,20)" in colour_expr.replace(" ", "")
    assert "0,92,143" in colour_expr.replace(
        " ", ""
    ) or "color_rgb(0,92,143)" in colour_expr.replace(" ", "")
    veg = ET.fromstring(
        """
        <maplayer>
          <layername>vegetation map</layername>
          <renderer-v2 type="categorizedSymbol">
            <categories>
              <category value="native" symbol="1"/>
              <category value="scattered_scrub" symbol="2"/>
              <category value="scrub" symbol="3"/>
            </categories>
            <symbols>
              <symbol name="1" type="fill"><layer class="SimpleFill"><Option type="Map">
                <Option name="color" type="QString" value="164,214,94,102"/>
              </Option></layer></symbol>
              <symbol name="2" type="fill"><layer class="PointPatternFill"><Option type="Map">
                <Option name="distance_x" type="QString" value="5"/>
              </Option></layer></symbol>
              <symbol name="3" type="fill"><layer class="SimpleFill"><Option type="Map">
                <Option name="color" type="QString" value="164,214,94,51"/>
              </Option></layer></symbol>
            </symbols>
          </renderer-v2>
        </maplayer>
        """
    )
    patch_vegetation(veg)
    native = veg.find(
        ".//symbol[@name='1']/layer[@class='SimpleFill']/Option/Option[@name='color']"
    )
    assert native.get("value").startswith("225,234,195")
