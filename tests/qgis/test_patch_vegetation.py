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
              </Option></layer></symbol>
              <symbol name="3" type="fill">
                <layer class="LinePatternFill"><Option type="Map">
                  <Option name="angle" type="QString" value="45"/>
                </Option></layer>
                <layer class="SimpleFill"><Option type="Map">
                <Option name="color" type="QString" value="164,214,94,51"/>
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
    assert scattered.find("layer[@class='PointPatternFill']") is not None
    assert scattered.find("layer[@class='SimpleFill']") is None
    patch_vegetation(layer)
    assert len(scrub.findall("layer[@class='PointPatternFill']")) == 1
    assert scrub.find("layer[@class='LinePatternFill']") is None
