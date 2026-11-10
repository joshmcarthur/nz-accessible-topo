import xml.etree.ElementTree as ET

from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_thin_lines import patch_thin_lines

FENCE_XML = """
<maplayer>
  <layername>fence_line map</layername>
  <renderer-v2 type="singleSymbol"><symbols>
    <symbol name="0" type="line">
      <layer class="SimpleLine">
        <Option type="Map">
          <Option name="line_color" type="QString" value="14,4,6,255"/>
          <Option name="line_width" type="QString" value="0.05"/>
        </Option>
      </layer>
    </symbol>
  </symbols></renderer-v2>
</maplayer>
"""

BRIDGE_XML = """
<maplayer>
  <layername>bridge_line copy copy</layername>
  <renderer-v2 type="RuleRenderer">
    <rules>
      <rule filter=" &quot;bridge_use&quot; = 'vehicle' and &quot;lanes&quot; = '2'" label="vehicle-2" symbol="0"/>
      <rule filter=" &quot;bridge_use&quot; = 'vehicle' and &quot;lanes&quot; = '1'" label="vehicle-1" symbol="1"/>
    </rules>
    <symbols>
      <symbol name="0" type="line">
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="line_color" type="QString" value="0,0,0,255"/>
            <Option name="line_width" type="QString" value="0.1"/>
            <Option name="offset" type="QString" value="0.38"/>
          </Option>
        </layer>
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="line_color" type="QString" value="35,35,35,255"/>
            <Option name="line_width" type="QString" value="0.1"/>
            <Option name="offset" type="QString" value="-0.38"/>
          </Option>
        </layer>
        <layer class="MarkerLine">
          <Option type="Map">
            <Option name="offset" type="QString" value="0"/>
          </Option>
          <symbol name="@ticks" type="marker">
            <layer class="SimpleMarker">
              <Option type="Map">
                <Option name="name" type="QString" value="line"/>
                <Option name="size" type="QString" value="1"/>
                <Option name="outline_width" type="QString" value="0.2"/>
              </Option>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="1" type="line">
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="line_color" type="QString" value="255,255,255,255"/>
            <Option name="line_width" type="QString" value="0.51"/>
          </Option>
        </layer>
        <layer class="SimpleLine">
          <Option type="Map">
            <Option name="line_color" type="QString" value="35,35,35,255"/>
            <Option name="line_width" type="QString" value="0.2"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""


def _widths(layer, symbol_name):
    return [
        line.find("Option/Option[@name='line_width']").get("value")
        for line in layer.findall(
            f".//symbol[@name='{symbol_name}']/layer[@class='SimpleLine']"
        )
    ]


def test_fence_rises_to_the_fence_width():
    # Catches a 0.05 mm fence left on the sheet.
    layer = ET.fromstring(FENCE_XML)
    patch_thin_lines(layer)
    floor = str(STYLE["sizes"]["fence_line_mm"])
    assert _widths(layer, "0") == [floor]
    patch_thin_lines(layer)
    assert _widths(layer, "0") == [floor]


def test_two_lane_bridge_casings_rise_to_the_line_floor():
    # Catches 0.1 mm two-lane casings, 1.0 mm end ticks, or a one-lane casing pulled down.
    layer = ET.fromstring(BRIDGE_XML)
    patch_thin_lines(layer)
    spec = STYLE["bridges"]["two_lane"]
    casing = str(spec["casing_width_mm"])
    assert _widths(layer, "0") == [casing, casing]
    assert _widths(layer, "1") == ["0.51", "0.2"]
    tick = layer.find(
        ".//symbol[@name='0']/layer[@class='MarkerLine']"
        "/symbol/layer[@class='SimpleMarker']/Option/Option[@name='size']"
    )
    assert tick.get("value") == str(spec["tick_mm"])
    assert spec["casing_width_mm"] >= 0.2
    assert spec["tick_mm"] >= 1.4


def test_other_layers_are_unchanged():
    # Catches a line-floor bump on a layer this patch does not own.
    layer = ET.fromstring(FENCE_XML)
    layer.find("layername").text = "track_line map"
    before = ET.tostring(layer, encoding="unicode")
    patch_thin_lines(layer)
    assert ET.tostring(layer, encoding="unicode") == before


EMBANKMENT_XML = """
<maplayer>
  <layername>relief_line map</layername>
  <renderer-v2 type="RuleRenderer">
    <rules>
      <rule filter="&quot;type&quot; = 'cliff_edge'" label="cliff_edge" symbol="0"/>
      <rule filter="&quot;type&quot; = 'embankment'" label="embankment_stopbank" symbol="1"/>
    </rules>
    <symbols>
      <symbol name="0" type="line">
        <layer class="SimpleLine"><Option type="Map">
          <Option name="line_width" type="QString" value="0.054"/>
        </Option></layer>
      </symbol>
      <symbol name="1" type="line">
        <layer class="SimpleLine"><Option type="Map">
          <Option name="line_width" type="QString" value="0.06"/>
        </Option></layer>
        <layer class="MarkerLine"><symbol name="@1@1" type="marker">
          <layer class="SimpleMarker"><Option type="Map">
            <Option name="outline_width" type="QString" value="0.1"/>
          </Option></layer>
        </symbol></layer>
      </symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""


def test_embankment_ticks_rise_and_cliffs_keep_the_stock_line():
    # Catches 0.1 mm stopbank ticks, which reduced acuity loses (log 0113).
    layer = ET.fromstring(EMBANKMENT_XML)
    patch_thin_lines(layer)
    spec = STYLE["relief"]["embankment"]
    assert _widths(layer, "1") == [str(spec["line_mm"])]
    tick = layer.find(".//layer[@class='SimpleMarker']/Option/Option")
    assert tick.get("value") == str(spec["tick_stroke_mm"])
    assert _widths(layer, "0") == ["0.054"]
