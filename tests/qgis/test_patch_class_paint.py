import xml.etree.ElementTree as ET

from nzat.qgis.patch_class_paint import patch_class_paint

LANDUSE_XML = """
<maplayer>
  <layername>landuse</layername>
  <renderer-v2 type="categorizedSymbol" attr="feature_type">
    <categories>
      <category label="cemetery" symbol="0" type="string" value="cemetery"/>
      <category label="quarry" symbol="1" type="string" value="quarry"/>
      <category label="" symbol="2" type="NULL" value="NULL"/>
    </categories>
    <symbols>
      <symbol name="0" type="fill"><layer class="SimpleFill">
        <Option type="Map"><Option name="color" type="QString" value="240,179,47,255"/></Option>
      </layer></symbol>
      <symbol name="1" type="fill"><layer class="SimpleFill">
        <Option type="Map"><Option name="color" type="QString" value="191,90,234,255"/></Option>
      </layer></symbol>
      <symbol name="2" type="fill"><layer class="SimpleFill">
        <Option type="Map"><Option name="color" type="QString" value="131,235,235,255"/></Option>
      </layer></symbol>
    </symbols>
  </renderer-v2>
</maplayer>
"""

STYLE = {
    "class_paint": {
        "landuse": {
            "classes": {
                "cemetery": {
                    "pattern": {
                        "shape": "cross",
                        "colour": "#000000",
                        "size_mm": 1.4,
                        "stroke_mm": 0.2,
                        "spacing_mm": [3, 2.4],
                    },
                    "lines": [{"colour": "#000000", "width_mm": 0.2, "dash": "2;1"}],
                },
                "orchard": {"lines": [{"colour": "#008A00", "width_mm": 0.2}]},
            },
            "stock_paint": ["vehicle_track"],
        }
    }
}


def _symbol(layer, value):
    renderer = layer.find("renderer-v2")
    name = next(
        c.get("symbol") for c in renderer.iter("category") if c.get("value") == value
    )
    return next(s for s in renderer.iter("symbol") if s.get("name") == name)


def _colours(symbol):
    return [
        option.get("value")
        for option in symbol.findall("layer/Option/Option[@name='color']")
    ]


def test_layer_reads_type_and_draws_the_owned_class():
    layer = ET.fromstring(LANDUSE_XML)
    patch_class_paint(layer, STYLE)
    assert layer.find("renderer-v2").get("attr") == "type"
    classes = [
        part.get("class") for part in _symbol(layer, "cemetery").findall("layer")
    ]
    assert classes == ["PointPatternFill", "SimpleLine"]
    dash = _symbol(layer, "cemetery").find(
        "layer[@class='SimpleLine']/Option/Option[@name='customdash']"
    )
    assert dash.get("value") == "2;1"


def test_class_we_do_not_own_keeps_the_stock_paint():
    # Catches the QGIS random colours that reading `type` alone paints (log 0114).
    layer = ET.fromstring(LANDUSE_XML)
    patch_class_paint(layer, STYLE)
    assert _colours(_symbol(layer, "quarry")) == ["131,235,235,255"]


def test_type_with_no_stock_category_gets_one():
    # Catches orchards that stop drawing once the layer reads `type`.
    layer = ET.fromstring(LANDUSE_XML)
    patch_class_paint(layer, STYLE)
    assert _symbol(layer, "orchard").find("layer").get("class") == "SimpleLine"
    assert _colours(_symbol(layer, "vehicle_track")) == ["131,235,235,255"]
    names = [s.get("name") for s in layer.iter("symbol") if s.get("type") == "fill"]
    assert len(names) == len(set(names))


def test_other_layers_are_unchanged():
    layer = ET.fromstring(
        LANDUSE_XML.replace("<layername>landuse", "<layername>runway")
    )
    patch_class_paint(layer, STYLE)
    assert layer.find("renderer-v2").get("attr") == "feature_type"
