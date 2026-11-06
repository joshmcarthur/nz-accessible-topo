import xml.etree.ElementTree as ET
from pathlib import Path

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_relief_point import patch_relief_point
from nzat.qgis.patch_structures import SYMBOLS_DIR

RELIEF_XML = """
<maplayer>
  <layername>relief_point map</layername>
  <fieldConfiguration><field name="type"/></fieldConfiguration>
  <renderer-v2 type="singleSymbol"><symbols>
    <symbol name="0" type="marker">
      <layer class="SimpleMarker">
        <Option type="Map">
          <Option name="name" type="QString" value="circle"/>
          <Option name="size" type="QString" value="0.3"/>
          <Option name="color" type="QString" value="0,0,0,255"/>
          <Option name="outline_color" type="QString" value="255,255,255,0"/>
          <Option name="outline_width" type="QString" value="0.4"/>
        </Option>
      </layer>
    </symbol>
  </symbols></renderer-v2>
</maplayer>
"""


def _option(layer, symbol_name, class_name, option_name):
    marker = layer.find(
        f".//symbol[@name='{symbol_name}']/layer[@class='{class_name}']"
    )
    return marker.find(f"Option/Option[@name='{option_name}']")


def test_saddle_is_two_arcs_and_spot_heights_stay_dots():
    # Catches a saddle left as a 0.3 mm spot-height dot, or a spot height enlarged to the saddle.
    layer = ET.fromstring(RELIEF_XML)
    patch_relief_point(layer)
    spec = STYLE["relief"]["saddle"]
    renderer = layer.find("renderer-v2")
    assert renderer.get("type") == "RuleRenderer"
    filters = [rule.get("filter") or "" for rule in renderer.findall("rules/rule")]
    assert any("saddle" in blob and "coalesce" in blob for blob in filters)
    assert any(blob.strip() == "ELSE" for blob in filters)
    name = _option(layer, "1", "SvgMarker", "name")
    size = _option(layer, "1", "SvgMarker", "size")
    svg = SYMBOLS_DIR / Path(spec["marker"]).name
    assert name.get("value") == spec["marker"]
    assert size.get("value") == str(spec["size_mm"])
    assert spec["stroke_mm"] >= 0.2
    assert svg.is_file()
    root = ET.fromstring(svg.read_text(encoding="utf-8"))
    view = [float(part) for part in root.get("viewBox").split()]
    height = view[3] / view[2] * spec["size_mm"]
    assert abs(height - 1.4) < 0.02
    stroke = max(
        float(node.get("stroke-width"))
        for node in root.iter()
        if node.get("stroke-width")
    )
    assert stroke / view[2] * spec["size_mm"] >= spec["stroke_mm"] - 1e-9
    spot = _option(layer, "0", "SimpleMarker", "size")
    assert spot.get("value") == "0.3"
    patch_relief_point(layer)
    assert len(layer.findall(".//symbol[@name='1']/layer[@class='SvgMarker']")) == 1
    assert len(layer.findall(".//symbol[@name='0']/layer[@class='SimpleMarker']")) == 1


def test_saddle_filter_uses_feature_type_when_type_is_absent():
    # Catches a stock .qgs that only lists feature_type, with the parquet column named type.
    xml = RELIEF_XML.replace('<field name="type"/>', '<field name="feature_type"/>')
    layer = ET.fromstring(xml)
    patch_relief_point(layer)
    filters = [rule.get("filter") or "" for rule in layer.findall(".//rule")]
    saddle = [blob for blob in filters if "saddle" in blob][0]
    assert "feature_type" in saddle
    assert '"type"' not in saddle
