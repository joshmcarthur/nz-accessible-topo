import xml.etree.ElementTree as ET
from pathlib import Path
from xml.etree.ElementTree import ParseError

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_landcover import patch_landcover
from nzat.qgis.patch_structures import SYMBOLS_DIR
from nzat.qgis.rgba import rgba

LANDCOVER_XML = """
<maplayer>
  <layername>landcover map</layername>
  <renderer-v2 type="RuleRenderer">
    <rules>
      <rule filter=" &quot;type&quot;  =  'moraine' " label="moraine" symbol="1"/>
      <rule filter=" &quot;type&quot;  =  'moraine_wall' " label="moraine_wall" symbol="2"/>
      <rule filter=" &quot;type&quot;  =  'scree' " label="scree" symbol="6"/>
      <rule filter=" &quot;type&quot;  =  'shingle' " label="shingle" symbol="7"/>
      <rule filter=" &quot;type&quot;  =  'swamp' " label="swamp" symbol="8"/>
      <rule filter=" &quot;type&quot;  =  'sand' " label="sand" symbol="5"/>
    </rules>
    <symbols>
      <symbol name="1" type="fill">
        <layer class="SVGFill">
          <Option type="Map">
            <Option name="svgFile" type="QString" value="./symbol/nztopo50_shingle.svg"/>
            <Option name="width" type="QString" value="10"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
            <Option name="outline_width" type="QString" value="0.26"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="2" type="fill">
        <layer class="LinePatternFill">
          <Option type="Map">
            <Option name="color" type="QString" value="240,0,236,255"/>
            <Option name="angle" type="QString" value="135"/>
          </Option>
          <symbol type="line">
            <layer class="SimpleLine">
              <Option type="Map">
                <Option name="customdash" type="QString" value="1;2"/>
                <Option name="line_color" type="QString" value="240,0,236,255"/>
                <Option name="line_width" type="QString" value="0.5"/>
                <Option name="use_custom_dash" type="QString" value="1"/>
              </Option>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="5" type="fill">
        <layer class="SVGFill">
          <Option type="Map">
            <Option name="svgFile" type="QString" value="./symbol/nztopo50_sand.svg"/>
            <Option name="width" type="QString" value="10"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
            <Option name="outline_width" type="QString" value="0.26"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="6" type="fill">
        <layer class="SVGFill">
          <Option type="Map">
            <Option name="svgFile" type="QString" value="./symbol/nztopo50_shingle.svg"/>
            <Option name="width" type="QString" value="10"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
            <Option name="outline_width" type="QString" value="0.26"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="7" type="fill">
        <layer class="SVGFill">
          <Option type="Map">
            <Option name="svgFile" type="QString" value="./symbol/nztopo50_shingle.svg"/>
            <Option name="width" type="QString" value="10"/>
            <Option name="color" type="QString" value="0,0,0,255"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
            <Option name="outline_width" type="QString" value="0.26"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="8" type="fill">
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="customdash" type="QString" value="1;0.5"/>
            <Option name="line_color" type="QString" value="0,158,255,255"/>
            <Option name="line_width" type="QString" value="0.1"/>
            <Option name="use_custom_dash" type="QString" value="1"/>
          </Option>
        </layer>
        <layer class="SVGFill">
          <Option type="Map">
            <Option name="svgFile" type="QString" value="./symbol/nztopo50_swamp.svg"/>
            <Option name="width" type="QString" value="4.5"/>
            <Option name="color" type="QString" value="0,0,255,255"/>
            <Option name="outline_color" type="QString" value="0,158,255,255"/>
            <Option name="outline_width" type="QString" value="0.26"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""


def _svgfile(layer, symbol_name):
    return layer.find(
        f".//symbol[@name='{symbol_name}']/layer[@class='SVGFill']/Option/Option[@name='svgFile']"
    )


def _sheet_stroke_mm(path, pattern_mm):
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    view = [float(part) for part in root.get("viewBox").split()]
    width = view[2]
    stroke = max(
        float(node.get("stroke-width"))
        for node in root.iter()
        if node.get("stroke-width")
    )
    return stroke / width * pattern_mm


def test_moraine_scree_and_shingle_use_distinct_owned_textures():
    # Catches moraine, scree and shingle all left on shingle.svg, or a hairline texture stroke.
    layer = ET.fromstring(LANDCOVER_XML)
    patch_landcover(layer)
    cover = STYLE["landcover"]
    files = {
        "1": cover["moraine"]["marker"],
        "6": cover["scree"]["marker"],
        "7": cover["shingle"]["marker"],
        "8": cover["swamp"]["marker"],
    }
    assert len(set(files.values())) == 4
    for symbol_name, marker in files.items():
        assert _svgfile(layer, symbol_name).get("value") == marker
        svg = SYMBOLS_DIR / Path(marker).name
        assert svg.is_file()
        try:
            ET.parse(svg)
        except ParseError as error:
            raise AssertionError(f"owned {marker} is not well formed") from error
        width = float(
            layer.find(
                f".//symbol[@name='{symbol_name}']/layer[@class='SVGFill']"
                "/Option/Option[@name='width']"
            ).get("value")
        )
        key = next(k for k, spec in cover.items() if spec.get("marker") == marker)
        assert _sheet_stroke_mm(svg, width) >= cover[key]["stroke_mm"] - 1e-9
    sand = _svgfile(layer, "5")
    assert sand.get("value") == "./symbol/nztopo50_sand.svg"


def test_moraine_wall_is_black_dotted_rows():
    # Catches magenta #F000EC left on moraine wall rows.
    layer = ET.fromstring(LANDCOVER_XML)
    patch_landcover(layer)
    ink = rgba("#000000", 255)
    colour = layer.find(
        ".//symbol[@name='2']//layer[@class='SimpleLine']/Option/Option[@name='line_color']"
    )
    width = layer.find(
        ".//symbol[@name='2']//layer[@class='SimpleLine']/Option/Option[@name='line_width']"
    )
    dash = layer.find(
        ".//symbol[@name='2']//layer[@class='SimpleLine']/Option/Option[@name='use_custom_dash']"
    )
    assert colour.get("value") == ink
    assert width.get("value") == "0.5"
    assert dash.get("value") == "1"
    assert "240,0,236" not in ET.tostring(layer, encoding="unicode")
    swamp_ink = layer.find(
        ".//symbol[@name='8']/layer[@class='SVGFill']/Option/Option[@name='color']"
    )
    assert swamp_ink.get("value") == rgba(STYLE["reference_inks"]["stream"], 255)
