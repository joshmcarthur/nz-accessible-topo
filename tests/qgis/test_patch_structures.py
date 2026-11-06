import xml.etree.ElementTree as ET
from pathlib import Path
from xml.etree.ElementTree import ParseError

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_structures import (
    BIVOUAC_SVG,
    OWNED_POINT_SVGS,
    SYMBOLS_DIR,
    install_owned_symbols,
    patch_building,
    patch_building_point,
    patch_structure_line,
    patch_structure_point,
)
from nzat.qgis.rgba import rgba

POINT_XML = """
<maplayer>
  <layername>structure_point map</layername>
  <renderer-v2 type="RuleRenderer">
    <rules>
      <rule filter=" &quot;type&quot;  =  'bivouac' " label="bivouac" symbol="0"/>
      <rule filter=" &quot;type&quot; =  'beacon' " label="marine beacon" symbol="11"/>
      <rule filter=" &quot;type&quot;  =  'mast' " label="mast" symbol="12"/>
      <rule filter=" &quot;type&quot;  =  'redoubt' " label="redoubt" symbol="13"/>
      <rule filter=" &quot;type&quot;  =  'tower' " label="tower" symbol="20"/>
      <rule filter="  &quot;wreck_of&quot; =  'ship' " label="ship" symbol="28"/>
      <rule filter=" &quot;type&quot; =  'lighthouse' " label="lighthouse" symbol="10"/>
      <rule filter=" &quot;type&quot;  =  'shaft' " label="shaft" symbol="14"/>
      <rule filter=" &quot;type&quot;  =  'stockyard' " label="stockyard" symbol="16"/>
      <rule filter=" &quot;type&quot; =  'tank' " label="tank" symbol="17"/>
      <rule filter="  &quot;stored_item&quot; =   'water' " label="water" symbol="19"/>
      <rule filter=" &quot;type&quot;  =  'floodgate' " label="floodgate" symbol="5"/>
      <rule filter=" &quot;type&quot;  =  'gate' " label="gate" symbol="6">
        <rule filter="ELSE" symbol="7"/>
        <rule filter=" &quot;restrictions&quot; = 'locked'" symbol="8"/>
      </rule>
    </rules>
    <symbols>
      <symbol name="0" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_cave.svg"/>
            <Option name="size" type="QString" value="1.6"/>
            <Option name="outline_width" type="QString" value="0"/>
            <Option name="color" type="QString" value="213,180,60,255"/>
            <Option name="outline_color" type="QString" value="35,35,35,255"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="11" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_marine_beacon.svg"/>
            <Option name="size" type="QString" value="2"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="12" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_mast.svg"/>
            <Option name="size" type="QString" value="1.0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="13" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_redoubt.svg"/>
            <Option name="size" type="QString" value="2.5"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="20" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_tower.svg"/>
            <Option name="size" type="QString" value="1.6"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="28" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_wreck_ship.svg"/>
            <Option name="size" type="QString" value="3"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="10" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_lighthouse.svg"/>
            <Option name="size" type="QString" value="1.8"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="14" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_shaft.svg"/>
            <Option name="size" type="QString" value="1.2"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="16" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_stockyard.svg"/>
            <Option name="size" type="QString" value="1.6"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="17" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_tank_water.svg"/>
            <Option name="size" type="QString" value="3"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="19" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_tank_water.svg"/>
            <Option name="size" type="QString" value="1"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="5" type="marker">
        <layer class="SimpleMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="line"/>
            <Option name="size" type="QString" value="1"/>
            <Option name="outline_width" type="QString" value="0.2"/>
            <Option name="outline_color" type="QString" value="0,0,0,255"/>
            <Option name="color" type="QString" value="0,0,255,255"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="8" type="marker">
        <layer class="SimpleMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="line"/>
            <Option name="outline_color" type="QString" value="255,69,0,255"/>
            <Option name="size" type="QString" value="1.4"/>
            <Option name="outline_width" type="QString" value="0.2"/>
            <Option name="color" type="QString" value="0,0,255,255"/>
          </Option>
          <data_defined_properties><Option type="Map">
            <Option name="properties" type="Map">
              <Option name="angle" type="Map">
                <Option name="active" type="bool" value="true"/>
                <Option name="expression" type="QString" value="360-( &quot;orientation&quot; /3.142)*180"/>
                <Option name="type" type="int" value="3"/>
              </Option>
            </Option>
          </Option></data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""

BUILDING_XML = """
<maplayer>
  <layername>building_point map</layername>
  <renderer-v2 type="RuleRenderer">
    <rules>
      <rule filter=" &quot;subtype&quot;  =  'hut' " label="hut" symbol="1"/>
      <rule filter=" &quot;subtype&quot;  =  'church' " label="church" symbol="2"/>
    </rules>
    <symbols>
      <symbol name="1" type="marker">
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_hut.svg"/>
            <Option name="size" type="QString" value="0.8"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="2" type="marker">
        <layer class="SimpleMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="square"/>
            <Option name="size" type="QString" value="0.5"/>
            <Option name="outline_width" type="QString" value="0"/>
          </Option>
        </layer>
        <layer class="SimpleMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="line"/>
            <Option name="size" type="QString" value="0.6"/>
            <Option name="outline_width" type="QString" value="0.08"/>
          </Option>
        </layer>
        <layer class="SvgMarker">
          <Option type="Map">
            <Option name="name" type="QString" value="./symbol/nztopo50_church.svg"/>
            <Option name="size" type="QString" value="0.5"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""

LINE_XML = """
<maplayer>
  <layername>structure_line</layername>
  <renderer-v2 type="categorizedSymbol">
    <categories>
      <category label="buried gas pipeline" symbol="1" value="gas"/>
      <category label="cableway" symbol="2" value="cableway_people"/>
    </categories>
    <symbols>
      <symbol name="1" type="line">
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="line_color" type="QString" value="234,99,0,255"/>
            <Option name="line_width" type="QString" value="0.21"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
          </Option>
        </layer>
      </symbol>
      <symbol name="2" type="line">
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="line_color" type="QString" value="0,0,0,255"/>
            <Option name="line_width" type="QString" value="0.17"/>
            <Option name="customdash" type="QString" value="5;2"/>
            <Option name="use_custom_dash" type="QString" value="0"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""


def _option(layer, symbol_name, class_name, option_name, marker_name=None):
    for marker in layer.findall(
        f".//symbol[@name='{symbol_name}']/layer[@class='{class_name}']"
    ):
        if marker_name is None:
            return marker.find(f"Option/Option[@name='{option_name}']")
        name = marker.find("Option/Option[@name='name']")
        if name is not None and name.get("value") == marker_name:
            return marker.find(f"Option/Option[@name='{option_name}']")
    return None


def test_locked_gate_is_a_black_bar_with_a_square():
    # Catches the orange bar left in place, or a second bar that would read as a cattlestop.
    layer = ET.fromstring(POINT_XML)
    patch_structure_point(layer)
    ink = rgba(STYLE["structures"]["locked_gate"]["bar_colour"], 255)
    colour = _option(layer, "8", "SimpleMarker", "outline_color", "line")
    size = _option(layer, "8", "SimpleMarker", "size", "line")
    stroke = _option(layer, "8", "SimpleMarker", "outline_width", "line")
    lock_size = _option(layer, "8", "SimpleMarker", "size", "square")
    lock_fill = _option(layer, "8", "SimpleMarker", "color", "square")
    bars = [
        marker
        for marker in layer.findall(".//symbol[@name='8']/layer[@class='SimpleMarker']")
        if marker.find("Option/Option[@name='name']").get("value") == "line"
    ]
    squares = [
        marker
        for marker in layer.findall(".//symbol[@name='8']/layer[@class='SimpleMarker']")
        if marker.find("Option/Option[@name='name']").get("value") == "square"
    ]
    assert colour.get("value") == ink
    assert size.get("value") == "1.4"
    assert stroke.get("value") == "0.2"
    assert lock_size.get("value") == "0.6"
    assert lock_fill.get("value") == ink
    assert len(bars) == 1
    assert len(squares) == 1
    angle = squares[0].find(
        "data_defined_properties/Option/Option[@name='properties']"
        "/Option[@name='angle']/Option[@name='expression']"
    )
    assert "orientation" in angle.get("value")
    patch_structure_point(layer)
    assert (
        len(
            [
                marker
                for marker in layer.findall(
                    ".//symbol[@name='8']/layer[@class='SimpleMarker']"
                )
                if marker.find("Option/Option[@name='name']").get("value") == "square"
            ]
        )
        == 1
    )


def test_bivouac_uses_the_owned_tent_svg():
    # Catches a bivouac left on the cave SVG, or a mark under 1.4 mm / 0.15 mm.
    layer = ET.fromstring(POINT_XML)
    patch_structure_point(layer)
    spec = STYLE["structures"]["bivouac"]
    name = _option(layer, "0", "SvgMarker", "name")
    size = _option(layer, "0", "SvgMarker", "size")
    caves = [
        marker
        for marker in layer.findall(".//symbol[@name='0']/layer[@class='SvgMarker']")
        if "cave" in (marker.find("Option/Option[@name='name']").get("value") or "")
    ]
    assert name.get("value") == spec["marker"]
    assert size.get("value") == str(spec["size_mm"])
    assert spec["size_mm"] >= 1.4
    assert spec["stroke_mm"] >= 0.15
    assert caves == []
    assert BIVOUAC_SVG.is_file()
    svg = BIVOUAC_SVG.read_text(encoding="utf-8")
    root = ET.fromstring(svg)
    view = [float(part) for part in root.get("viewBox").split()]
    width, height = view[2], view[3]
    assert width > height
    stroke = max(
        float(node.get("stroke-width"))
        for node in root.iter()
        if node.get("stroke-width")
    )
    assert stroke / width * spec["size_mm"] >= spec["stroke_mm"] - 1e-9
    assert "nztopo50_cave" not in svg


def test_buried_gas_pipeline_is_dark_and_dashed():
    # Catches the legend orange left on a gas line, or a solid line with no dash.
    layer = ET.fromstring(LINE_XML)
    patch_structure_line(layer)
    spec = STYLE["structures"]["buried_gas_pipeline"]
    colour = _option(layer, "1", "SimpleLine", "line_color")
    width = _option(layer, "1", "SimpleLine", "line_width")
    dash = _option(layer, "1", "SimpleLine", "customdash")
    use_dash = _option(layer, "1", "SimpleLine", "use_custom_dash")
    other = _option(layer, "2", "SimpleLine", "line_color")
    assert colour.get("value") == rgba(spec["colour"], 255)
    assert width.get("value") == str(spec["width_mm"])
    assert dash.get("value") == spec["dash"]
    assert use_dash.get("value") == "1"
    assert other.get("value").startswith("0,0,0")


def test_structure_line_without_gas_is_unchanged():
    # Catches apply failing on the stock project, which has no gas category.
    layer = ET.fromstring(LINE_XML)
    for category in layer.findall("renderer-v2/categories/category"):
        if "gas" in f"{category.get('value')} {category.get('label')}".lower():
            layer.find("renderer-v2/categories").remove(category)
    before = ET.tostring(layer, encoding="unicode")
    patch_structure_line(layer)
    assert ET.tostring(layer, encoding="unicode") == before


def _sheet_stroke_mm(path, size_mm):
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    view = [float(part) for part in root.get("viewBox").split()]
    width = view[2]
    stroke = max(
        float(node.get("stroke-width"))
        for node in root.iter()
        if node.get("stroke-width")
    )
    return stroke / width * size_mm


def test_owned_point_svgs_keep_the_linz_shape_at_the_stroke_floor():
    # Catches a thin LINZ stroke left in place, or a marker that never points at the owned copy.
    layer = ET.fromstring(POINT_XML)
    patch_structure_point(layer)
    names = {
        "beacon": "11",
        "mast": "12",
        "redoubt": "13",
        "tower": "20",
        "shipwreck": "28",
        "lighthouse": "10",
        "shaft": "14",
        "stockyard": "16",
        "tank_water": "19",
    }
    assert {key for key, _needles in OWNED_POINT_SVGS} == set(names)
    for key, symbol_name in names.items():
        spec = STYLE["structures"][key]
        marker = _option(layer, symbol_name, "SvgMarker", "name")
        size = _option(layer, symbol_name, "SvgMarker", "size")
        svg_name = Path(spec["marker"]).name
        svg = SYMBOLS_DIR / svg_name
        assert marker.get("value") == spec["marker"]
        assert size.get("value") == str(spec["size_mm"])
        assert spec["stroke_mm"] >= 0.15
        assert svg.is_file()
        assert _sheet_stroke_mm(svg, spec["size_mm"]) >= spec["stroke_mm"] - 1e-9
        try:
            ET.parse(svg)
        except ParseError as error:
            raise AssertionError(f"owned {key} SVG is not well formed") from error


def test_church_uses_the_owned_svg_and_a_thicker_bar():
    # Catches the 0.08 mm QGIS bar, a 1.0 mm-tall church, or the 0.04 mm LINZ church stroke.
    layer = ET.fromstring(BUILDING_XML)
    patch_building_point(layer)
    spec = STYLE["structures"]["church"]
    name = _option(layer, "2", "SvgMarker", "name")
    size = _option(layer, "2", "SvgMarker", "size")
    bar = _option(layer, "2", "SimpleMarker", "outline_width", "line")
    svg = SYMBOLS_DIR / Path(spec["marker"]).name
    assert name.get("value") == spec["marker"]
    assert size.get("value") == str(spec["size_mm"])
    assert bar.get("value") == str(spec["bar_stroke_mm"])
    assert spec["bar_stroke_mm"] >= 0.15
    root = ET.fromstring(svg.read_text(encoding="utf-8"))
    view = [float(part) for part in root.get("viewBox").split()]
    assert abs(view[3] / view[2] * spec["size_mm"] - 1.4) < 0.02
    assert _sheet_stroke_mm(svg, spec["size_mm"]) >= spec["stroke_mm"] - 1e-9


def test_hut_uses_the_linz_glyph_at_the_mark_floor():
    # Catches a hut left at 0.8 mm.
    layer = ET.fromstring(BUILDING_XML)
    patch_building_point(layer)
    spec = STYLE["structures"]["hut"]
    name = _option(layer, "1", "SvgMarker", "name")
    size = _option(layer, "1", "SvgMarker", "size")
    assert name.get("value") == spec["marker"]
    assert size.get("value") == str(spec["size_mm"])
    assert spec["size_mm"] >= 1.4


def test_parent_tank_stays_large():
    # Catches the 3 mm parent tank rule shrunk with the water-tank marker.
    layer = ET.fromstring(POINT_XML)
    patch_structure_point(layer)
    size = _option(layer, "17", "SvgMarker", "size")
    assert size.get("value") == "3"


def test_floodgate_bar_matches_a_gate():
    # Catches a floodgate bar left at 1.0 mm.
    layer = ET.fromstring(POINT_XML)
    patch_structure_point(layer)
    spec = STYLE["structures"]["floodgate"]
    size = _option(layer, "5", "SimpleMarker", "size", "line")
    stroke = _option(layer, "5", "SimpleMarker", "outline_width", "line")
    assert size.get("value") == str(spec["bar_size_mm"])
    assert stroke.get("value") == str(spec["bar_stroke_mm"])
    assert spec["bar_size_mm"] >= 1.4


BUILDING_MAP_XML = """
<maplayer>
  <layername>building map</layername>
  <fieldConfiguration><field name="subtype"/></fieldConfiguration>
  <renderer-v2 type="singleSymbol"><symbols>
    <symbol name="0" type="fill">
      <layer class="SimpleFill">
        <Option type="Map">
          <Option name="color" type="QString" value="0,0,0,255"/>
          <Option name="outline_color" type="QString" value="255,255,255,0"/>
          <Option name="outline_style" type="QString" value="solid"/>
          <Option name="outline_width" type="QString" value="0"/>
          <Option name="style" type="QString" value="solid"/>
        </Option>
        <data_defined_properties><Option type="Map">
          <Option name="properties"/>
        </Option></data_defined_properties>
      </layer>
    </symbol>
  </symbols></renderer-v2>
</maplayer>
"""


def test_glasshouse_is_an_outline_not_a_solid_fill():
    # Catches a greenhouse polygon left solid black like every other building.
    layer = ET.fromstring(BUILDING_MAP_XML)
    patch_building(layer)
    renderer = layer.find("renderer-v2")
    assert renderer.get("type") == "RuleRenderer"
    filters = [rule.get("filter") or "" for rule in renderer.findall("rules/rule")]
    assert any("greenhouse" in blob and "coalesce" in blob for blob in filters)
    fill = layer.find(".//symbol[@name='1']/layer[@class='SimpleFill']")
    assert fill.find("Option/Option[@name='style']").get("value") == "no"
    assert fill.find("Option/Option[@name='outline_width']").get("value") == "0.2"
    assert (
        fill.find("Option/Option[@name='outline_color']")
        .get("value")
        .startswith("0,0,0")
    )
    other = layer.find(".//symbol[@name='0']/layer[@class='SimpleFill']")
    assert other.find("Option/Option[@name='style']").get("value") == "solid"
    assert other.find("Option/Option[@name='color']").get("value").startswith("0,0,0")
    patch_building(layer)
    assert len(layer.findall("renderer-v2/rules/rule")) == 2


def test_building_point_without_church_is_unchanged():
    # Catches apply failing on a project with no church rule.
    layer = ET.fromstring(BUILDING_XML)
    for rule in list(layer.findall("renderer-v2/rules/rule")):
        layer.find("renderer-v2/rules").remove(rule)
    before = ET.tostring(layer, encoding="unicode")
    patch_building_point(layer)
    assert ET.tostring(layer, encoding="unicode") == before


def test_install_owned_symbols_copies_the_tent(tmp_path):
    install_owned_symbols(tmp_path)
    copied = tmp_path / "symbol" / "nztopo50_bivouac.svg"
    assert copied.is_file()
    assert copied.read_bytes() == BIVOUAC_SVG.read_bytes()
    owned = {path.name: path.read_bytes() for path in SYMBOLS_DIR.glob("*.svg")}
    assert owned
    for name, body in owned.items():
        dest = tmp_path / "symbol" / name
        assert dest.is_file()
        assert dest.read_bytes() == body
        try:
            ET.parse(dest)
        except ParseError as error:
            raise AssertionError(f"owned {name} is not well formed") from error
