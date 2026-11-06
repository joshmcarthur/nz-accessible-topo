import xml.etree.ElementTree as ET

from nzat.qgis.patch_vegetation import patch_vegetation
from nzat.style.load_rules import load_rules
from nzat.style.vector_params import P
from nzat.style.vegetation_fill import vegetation_fill

RULES = load_rules()


def test_vegetation_reads_the_style_file():
    # Catches a vector scrub fill that ignores the JSON, or a 45° hatch left on raster scrub.
    veg = RULES["vegetation"]
    assert vegetation_fill("scrub", RULES) == "rgba(163, 204, 144, 1)"
    assert vegetation_fill("scattered", RULES) == "rgba(224, 237, 216, 1)"
    assert veg["scrub"]["colour"] == "#A3CC90"
    assert veg["scattered"]["colour"] == "#E0EDD8"
    assert "scrub" not in P
    assert "scattered_scrub" not in P
    layer = ET.fromstring(
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
                  <symbol name="1" type="fill">
                    <layer class="SimpleFill"><Option type="Map">
                      <Option name="color" type="QString" value="164,214,94,102"/>
                      <Option name="outline_color" type="QString" value="167,192,94,255"/>
                    </Option></layer>
                    <layer class="PointPatternFill">
                      <Option type="Map">
                        <Option name="distance_x" type="QString" value="5"/>
                      </Option>
                      <symbol type="marker">
                        <layer class="SimpleMarker">
                          <Option type="Map">
                            <Option name="color" type="QString" value="0,128,0,255"/>
                            <Option name="size" type="QString" value="1.5"/>
                          </Option>
                        </layer>
                      </symbol>
                    </layer>
                  </symbol>
              <symbol name="2" type="fill"><layer class="PointPatternFill"><Option type="Map">
                <Option name="distance_x" type="QString" value="5"/>
                <Option name="distance_y" type="QString" value="5"/>
                <Option name="clip_mode" type="QString" value="completely_within"/>
              </Option>
              <symbol type="marker">
                <layer class="SimpleMarker">
                  <Option type="Map">
                    <Option name="name" type="QString" value="third_arc"/>
                    <Option name="size" type="QString" value="1.2"/>
                    <Option name="color" type="QString" value="178,223,138,255"/>
                    <Option name="outline_color" type="QString" value="178,223,138,255"/>
                    <Option name="outline_width" type="QString" value="0"/>
                  </Option>
                </layer>
              </symbol>
              </layer></symbol>
              <symbol name="3" type="fill">
                <layer class="LinePatternFill"><Option type="Map">
                  <Option name="angle" type="QString" value="45"/>
                </Option></layer>
                <layer class="SimpleFill"><Option type="Map">
                <Option name="color" type="QString" value="164,214,94,51"/>
                <Option name="outline_color" type="QString" value="167,192,94,255"/>
              </Option></layer></symbol>
            </symbols>
          </renderer-v2>
        </maplayer>
        """
    )
    patch_vegetation(layer)
    scrub = layer.find(".//symbol[@name='3']")
    fill = scrub.find("layer[@class='SimpleFill']/Option/Option[@name='color']")
    assert fill.get("value").startswith("163,204,144")
    assert fill.get("value").endswith(",26")
    assert scrub.find("layer[@class='LinePatternFill']") is None
    dots = scrub.find("layer[@class='PointPatternFill']")
    assert dots is not None
    assert dots.find("Option/Option[@name='distance_x']").get("value") == "3"
    marker = dots.find(
        "symbol/layer[@class='SimpleMarker']/Option/Option[@name='name']"
    )
    assert marker.get("value") == "third_arc"
    # Catches a hairline arc (stroke 0) or clipped half-marks, which hid scrub.
    stroke = dots.find(
        "symbol/layer[@class='SimpleMarker']/Option/Option[@name='outline_width']"
    )
    assert float(stroke.get("value")) > 0
    clip = dots.find("Option/Option[@name='clip_mode']")
    assert clip.get("value") == "centroid_within"
    native = layer.find(".//symbol[@name='1']")
    tree = native.find("layer[@class='PointPatternFill']//Option[@name='color']")
    assert tree.get("value").startswith("63,107,50")
    scattered = layer.find(".//symbol[@name='2']")
    assert scattered.find("layer[@class='SimpleFill']") is None
    scattered_dots = scattered.find("layer[@class='PointPatternFill']")
    assert scattered_dots.find("Option/Option[@name='distance_x']").get("value") == "5"
    assert scattered_dots.find("Option/Option[@name='distance_y']").get("value") == "5"
    assert (
        scattered_dots.find("Option/Option[@name='clip_mode']").get("value")
        == "completely_within"
    )
    scattered_mark = scattered_dots.find("symbol/layer[@class='SimpleMarker']")
    assert (
        scattered_mark.find("Option/Option[@name='name']").get("value") == "third_arc"
    )
    assert scattered_mark.find("Option/Option[@name='size']").get("value") == "1.4"
    assert (
        float(scattered_mark.find("Option/Option[@name='outline_width']").get("value"))
        == 0.18
    )
    assert (
        scattered_mark.find("Option/Option[@name='color']")
        .get("value")
        .startswith("106,154,80")
    )
    native_outline = native.find(
        "layer[@class='SimpleFill']/Option/Option[@name='outline_color']"
    )
    assert native_outline.get("value").startswith("133,158,62")
    scrub_outline = scrub.find(
        "layer[@class='SimpleFill']/Option/Option[@name='outline_color']"
    )
    assert scrub_outline.get("value").startswith("133,158,62")
    patch_vegetation(layer)
    assert len(scrub.findall("layer[@class='PointPatternFill']")) == 1
    assert scrub.find("layer[@class='LinePatternFill']") is None
    assert len(scattered.findall("layer[@class='PointPatternFill']")) == 1


def test_trees_use_owned_stroke_svg():
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>vegetation_point map</layername>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="marker">
              <layer class="SimpleMarker">
                <Option type="Map">
                  <Option name="name" type="QString" value="circle"/>
                  <Option name="size" type="QString" value="0.05"/>
                  <Option name="color" type="QString" value="148,255,59,255"/>
                  <Option name="outline_color" type="QString" value="35,35,35,0"/>
                </Option>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_vegetation(layer)
    marker = layer.find("renderer-v2/symbols/symbol/layer[@class='SvgMarker']")
    assert marker is not None
    assert layer.find("renderer-v2/symbols/symbol/layer[@class='SimpleMarker']") is None
    assert (
        marker.find("Option/Option[@name='name']").get("value")
        == "./symbol/nztopo50_tree_stroke.svg"
    )
    assert marker.find("Option/Option[@name='size']").get("value") == "0.2"
    assert (
        marker.find("Option/Option[@name='color']").get("value").startswith("0,138,0")
    )
    patch_vegetation(layer)
    assert (
        len(layer.findall("renderer-v2/symbols/symbol/layer[@class='SvgMarker']")) == 1
    )


def test_exotic_marks_use_scrub_ink_and_split_on_subtype():
    # Catches fixed #9DCE69 conifers on both exotic classes, or a split with no subtype field.
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>vegetation map</layername>
          <fieldConfiguration>
            <field name="type"/>
            <field name="subtype"/>
          </fieldConfiguration>
          <renderer-v2 type="categorizedSymbol">
            <categories>
              <category value="native" symbol="1"/>
              <category value="scattered_scrub" symbol="2"/>
              <category value="scrub" symbol="3"/>
              <category value="exotic" symbol="0"/>
            </categories>
            <symbols>
              <symbol name="0" type="fill">
                <layer class="SimpleFill"><Option type="Map">
                  <Option name="color" type="QString" value="164,214,94,51"/>
                  <Option name="outline_color" type="QString" value="167,192,94,255"/>
                </Option></layer>
                <layer class="SVGFill">
                  <Option type="Map">
                    <Option name="svgFile" type="QString" value="./symbol/nztopo50_exotic_con.svg"/>
                    <Option name="width" type="QString" value="3"/>
                    <Option name="color" type="QString" value="231,72,162,255"/>
                    <Option name="outline_color" type="QString" value="35,35,35,255"/>
                    <Option name="outline_width" type="QString" value="0.26"/>
                  </Option>
                  <data_defined_properties><Option type="Map">
                    <Option name="properties"/>
                  </Option></data_defined_properties>
                </layer>
              </symbol>
              <symbol name="1" type="fill"><layer class="SimpleFill"><Option type="Map">
                <Option name="color" type="QString" value="164,214,94,102"/>
                <Option name="outline_color" type="QString" value="167,192,94,255"/>
              </Option></layer></symbol>
              <symbol name="2" type="fill"><layer class="PointPatternFill"><Option type="Map">
                <Option name="distance_x" type="QString" value="5"/>
                <Option name="distance_y" type="QString" value="5"/>
                <Option name="clip_mode" type="QString" value="completely_within"/>
              </Option>
              <symbol type="marker">
                <layer class="SimpleMarker">
                  <Option type="Map">
                    <Option name="name" type="QString" value="third_arc"/>
                    <Option name="size" type="QString" value="1.2"/>
                    <Option name="color" type="QString" value="178,223,138,255"/>
                    <Option name="outline_color" type="QString" value="178,223,138,255"/>
                    <Option name="outline_width" type="QString" value="0"/>
                  </Option>
                </layer>
              </symbol>
              </layer></symbol>
              <symbol name="3" type="fill"><layer class="SimpleFill"><Option type="Map">
                <Option name="color" type="QString" value="164,214,94,51"/>
                <Option name="outline_color" type="QString" value="167,192,94,255"/>
              </Option></layer></symbol>
            </symbols>
          </renderer-v2>
        </maplayer>
        """
    )
    patch_vegetation(layer)
    spec = RULES["vegetation"]["exotic"]
    fill = layer.find(".//symbol[@name='0']/layer[@class='SVGFill']")
    svg = fill.find("Option/Option[@name='svgFile']")
    colour = fill.find("Option/Option[@name='color']")
    expr = fill.find(
        "data_defined_properties//Option[@name='name']/Option[@name='expression']"
    )
    if expr is None:
        expr = fill.find(
            "data_defined_properties//Option[@name='svgFile']/Option[@name='expression']"
        )
    assert colour.get("value").startswith("106,154,80")
    assert spec["coniferous_marker"] in svg.get("value")
    assert expr is not None
    assert "non-coniferous" in expr.get("value")
    assert spec["non_coniferous_marker"] in expr.get("value")
    assert "coalesce" in expr.get("value")
    native_fill = layer.find(
        ".//symbol[@name='1']/layer[@class='SimpleFill']/Option/Option[@name='color']"
    )
    assert native_fill.get("value").startswith("225,234,195")
