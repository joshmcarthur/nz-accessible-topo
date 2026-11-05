import xml.etree.ElementTree as ET

from nzat.qgis.apply import apply
from nzat.qgis.defaults import FAMILY


def test_overrides_skip_the_print_layout():
    # Catches a change that restyles the legend or the sheet title.
    # Also catches a stretch-to-fit mode left on a curved name.
    root = ET.fromstring(
        """
        <qgis>
          <layer-tree-group>
            <layer-tree-layer name="vegetation map"/>
            <layer-tree-layer name="contour"/>
            <custom-order enabled="0"/>
          </layer-tree-group>
          <projectlayers>
            <maplayer>
              <layername>nztopo50_carto_text</layername>
              <labeling type="simple"><settings>
                <text-style fontFamily="Nimbus Sans LINZ" fontItalic="1" fontSize="5.5" namedStyle="Narrow Italic"/>
                <dd_properties><Option type="Map">
                  <Option name="properties" type="Map">
                    <Option name="Family" type="Map">
                      <Option name="field" type="QString" value="text_font"/>
                      <Option name="type" type="int" value="2"/>
                    </Option>
                    <Option name="FontStyle" type="Map">
                      <Option name="field" type="QString" value="style"/>
                      <Option name="type" type="int" value="2"/>
                    </Option>
                    <Option name="Size" type="Map">
                      <Option name="field" type="QString" value="size"/>
                      <Option name="type" type="int" value="2"/>
                    </Option>
                    <Option name="CurvedLabelMode" type="Map">
                      <Option name="field" type="QString" value="charplace"/>
                      <Option name="type" type="int" value="2"/>
                    </Option>
                  </Option>
                </Option></dd_properties>
              </settings></labeling>
            </maplayer>
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
              <labeling><settings>
                <text-style fontFamily="Nimbus Sans LINZ" fontItalic="0" fontSize="5" namedStyle="Regular"/>
              </settings></labeling>
            </maplayer>
            <maplayer>
              <layername>track_line map</layername>
              <fieldConfiguration><field name="status"/><field name="track_type"/></fieldConfiguration>
              <renderer-v2 type="categorizedSymbol">
                <categories><category value="foot" symbol="1"/></categories>
                <symbols>
                  <symbol name="1" type="line">
                    <layer class="SimpleLine">
                      <Option type="Map">
                        <Option name="use_custom_dash" type="QString" value="1"/>
                        <Option name="line_width" type="QString" value="0.15"/>
                      </Option>
                      <data_defined_properties><Option type="Map">
                        <Option name="properties"/>
                      </Option></data_defined_properties>
                    </layer>
                  </symbol>
                </symbols>
              </renderer-v2>
            </maplayer>
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
            <maplayer>
              <layername>water_line map</layername>
              <renderer-v2 type="singleSymbol"><symbols>
                <symbol name="0" type="line">
                  <layer class="SimpleLine">
                    <Option type="Map">
                      <Option name="line_color" type="QString" value="0,158,255,255"/>
                      <Option name="line_width" type="QString" value="0.1"/>
                    </Option>
                    <data_defined_properties><Option type="Map">
                      <Option name="properties"/>
                    </Option></data_defined_properties>
                  </layer>
                </symbol>
              </symbols></renderer-v2>
            </maplayer>
          </projectlayers>
          <Layouts>
            <Layout>
              <text-style fontFamily="Nimbus Sans LINZ" fontItalic="1" fontSize="5" namedStyle="Italic"/>
            </Layout>
          </Layouts>
        </qgis>
        """
    )
    apply(root)
    layout = root.find("Layouts/Layout/text-style")
    assert layout.get("fontFamily") == "Nimbus Sans LINZ"
    assert layout.get("namedStyle") == "Italic"
    label = root.find("projectlayers/maplayer/labeling/settings/text-style")
    assert label.get("fontFamily") == FAMILY
    assert label.get("namedStyle") == "Regular"
    assert label.get("fontSize") == "7"
    props = root.find(
        "projectlayers/maplayer/labeling/settings/dd_properties/Option/Option[@name='properties']"
    )
    assert (
        props.find("Option[@name='Family']/Option[@name='expression']").get("value")
        == f"'{FAMILY}'"
    )
    font_style = props.find("Option[@name='FontStyle']/Option[@name='expression']").get(
        "value"
    )
    assert "italic" in font_style
    assert "Bold" in font_style
    assert props.find("Option[@name='Family']/Option[@name='field']") is None
    curved = props.find("Option[@name='CurvedLabelMode']/Option[@name='expression']")
    assert "StretchWordSpacingToFit" in curved.get("value")
    assert "'default'" in curved.get("value")
    contour = root.find("projectlayers/maplayer[layername='contour']")
    assert contour.find(".//text-style").get("fontSize") == "7"
    lines = contour.findall(".//symbol[@name='0']/layer[@class='SimpleLine']")
    assert len(lines) == 2
    casing_color = lines[0].find(
        "data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']"
    )
    assert "122,85,66" in casing_color.get("value")
    assert "176,136,114" not in casing_color.get("value")
    enabled = lines[0].find(
        "data_defined_properties//Option[@name='enabled']/Option[@name='expression']"
    )
    assert "% 100 <> 0" in enabled.get("value")
    fill_color = lines[1].find(
        "data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']"
    )
    assert "122,85,66" in fill_color.get("value")
    assert "176,136,114" in fill_color.get("value")
    water = root.find("projectlayers/maplayer[layername='water_point']/renderer-v2")
    assert water.get("attr") == "type"
    scrub = root.find(
        "projectlayers/maplayer[layername='vegetation map']//symbol[@name='3']"
    )
    fill = scrub.find("layer[@class='SimpleFill']/Option/Option[@name='color']")
    assert fill.get("value").startswith("163,204,144")
    assert scrub.find("layer[@class='LinePatternFill']") is None
    assert scrub.find("layer[@class='PointPatternFill']") is not None
    # Catches drains drawn at river width, which made the plain a blue mesh.
    stream_width = root.find(
        "projectlayers/maplayer[layername='water_line map']"
        "//Option[@name='outlineWidth']/Option[@name='expression']"
    )
    assert stream_width.get("value") == (
        "CASE WHEN \"type\" = 'drain' THEN 0.15 ELSE 0.25 END"
    )
    scattered = root.find(
        "projectlayers/maplayer[layername='vegetation map']//symbol[@name='2']"
    )
    assert scattered.find("layer[@class='PointPatternFill']") is not None
    assert scattered.find("layer[@class='SimpleFill']") is None
    track = root.find(
        "projectlayers/maplayer[layername='track_line map']//symbol[@name='1']"
    )
    assert track.find("layer[@class='MarkerLine']") is not None
    closed = track.find(
        "layer[@class='MarkerLine']/symbol[@name='@closed']/layer[@class='SimpleMarker']/Option/Option[@name='name']"
    )
    assert closed.get("value") == "cross2"
    stream = root.find(
        "projectlayers/maplayer[layername='water_line map']//Option[@name='line_color']"
    )
    assert stream.get("value").startswith("0,76,153")
    painted = ET.tostring(root, encoding="unicode")
    assert "213,180,60" not in painted
    assert "234,99,0" not in painted


def test_vegetation_map_draws_below_contour():
    # Catches vegetation map left above contour in the layer tree.
    root = ET.fromstring(
        """
        <qgis>
          <layer-tree-group>
            <layer-tree-layer name="vegetation_line map"/>
            <layer-tree-layer name="vegetation map"/>
            <layer-tree-layer name="nztopo50_carto_symbol"/>
            <layer-tree-layer name="contour"/>
            <layer-tree-layer name="landcover map"/>
            <custom-order enabled="0"/>
          </layer-tree-group>
          <projectlayers>
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
            <maplayer>
              <layername>track_line map</layername>
              <fieldConfiguration><field name="status"/><field name="track_type"/></fieldConfiguration>
              <renderer-v2 type="categorizedSymbol">
                <categories><category value="foot" symbol="1"/></categories>
                <symbols>
                  <symbol name="1" type="line">
                    <layer class="SimpleLine">
                      <Option type="Map">
                        <Option name="use_custom_dash" type="QString" value="1"/>
                        <Option name="line_width" type="QString" value="0.15"/>
                      </Option>
                      <data_defined_properties><Option type="Map">
                        <Option name="properties"/>
                      </Option></data_defined_properties>
                    </layer>
                  </symbol>
                </symbols>
              </renderer-v2>
            </maplayer>
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
            <maplayer>
              <layername>water_line map</layername>
              <renderer-v2 type="singleSymbol"><symbols>
                <symbol name="0" type="line">
                  <layer class="SimpleLine">
                    <Option type="Map">
                      <Option name="line_color" type="QString" value="0,158,255,255"/>
                      <Option name="line_width" type="QString" value="0.1"/>
                    </Option>
                  </layer>
                </symbol>
              </symbols></renderer-v2>
            </maplayer>
          </projectlayers>
        </qgis>
        """
    )
    apply(root)
    names = [
        child.get("name")
        for child in list(root.find("layer-tree-group"))
        if child.tag == "layer-tree-layer"
    ]
    assert names.index("contour") < names.index("vegetation map")
    assert names.index("vegetation_line map") < names.index("contour")
    assert names.index("nztopo50_carto_symbol") < names.index("contour")
    assert names.index("vegetation map") < names.index("landcover map")
    assert root.find("layer-tree-group/custom-order").get("enabled") == "0"
