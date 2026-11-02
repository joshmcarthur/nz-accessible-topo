#!/usr/bin/env python3
"""Sanity tests for the measurement and rendering tools. Run: python3 tools/test_tools.py"""
import os
import sys
import xml.etree.ElementTree as ET

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import palette_audit as pa  # noqa: E402
import render_comparison as rc  # noqa: E402
import override_topo50_project as ov  # noqa: E402
import build_style as bs  # noqa: E402
import render_square as rs  # noqa: E402


def test_ciede2000_reference():
    # Sharma, Wu & Dalal (2005) test pairs 1 and 3
    assert round(pa.ciede2000((50, 2.6772, -79.7751), (50, 0, -82.7485)), 4) == 2.0425
    assert round(pa.ciede2000((50, -1.1848, -84.8006), (50, 0, -82.7485)), 4) == 1.0


def test_contrast_black_white():
    assert round(pa.contrast_ratio(pa.rel_luminance((0, 0, 0)), pa.rel_luminance((255, 255, 255))), 2) == 21.0


def test_hillshade_direction():
    # Log 0017: the first renderer lit slopes from the opposite side. Never again.
    y, x = np.mgrid[0:rc.H, 0:rc.W].astype(float)
    z = 1000 * np.exp(-((x - 310) ** 2 + (y - 230) ** 2) / (2 * 60 ** 2))
    for az, lit, dark in [(315, (180, 260), (280, 360)), (0, (170, 310), (290, 310)), (90, (230, 370), (230, 250))]:
        sh = rc.hillshade(z, [az], [1])
        assert sh[lit] > 0.9 and sh[dark] < 0.1, az


def test_upright_style_and_size_floor():
    # Catches a label style that stays italic, or a spot height lifted to 7 pt.
    for name in ("Italic", "Narrow Italic", "Narrow", "Narrow Bold", ""):
        assert ov.upright_style_name(name) == "Regular"
    assert ov.upright_style_name("Regular") == "Regular"
    assert ov.size_floor("contour", "5") == "7"
    assert ov.size_floor("contour", "10") == "10"
    assert ov.size_floor("relief_point map", "5") == "6"
    assert ov.size_floor("relief_point map", "6") == "6"


def test_overrides_skip_the_print_layout():
    # Catches a change that restyles the legend or the sheet title.
    # Also catches a stretch-to-fit mode left on a curved name.
    root = ET.fromstring(
        """
        <qgis>
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
              <fieldConfiguration><field name="status"/></fieldConfiguration>
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
          </projectlayers>
          <Layouts>
            <Layout>
              <text-style fontFamily="Nimbus Sans LINZ" fontItalic="1" fontSize="5" namedStyle="Italic"/>
            </Layout>
          </Layouts>
        </qgis>
        """
    )
    ov.apply(root)
    layout = root.find("Layouts/Layout/text-style")
    assert layout.get("fontFamily") == "Nimbus Sans LINZ"
    assert layout.get("namedStyle") == "Italic"
    label = root.find("projectlayers/maplayer/labeling/settings/text-style")
    assert label.get("fontFamily") == ov.FAMILY
    assert label.get("namedStyle") == "Regular"
    assert label.get("fontSize") == "7"
    props = root.find("projectlayers/maplayer/labeling/settings/dd_properties/Option/Option[@name='properties']")
    assert props.find("Option[@name='Family']/Option[@name='expression']").get("value") == f"'{ov.FAMILY}'"
    assert "italic" in props.find("Option[@name='FontStyle']/Option[@name='expression']").get("value")
    assert props.find("Option[@name='Family']/Option[@name='field']") is None
    curved = props.find("Option[@name='CurvedLabelMode']/Option[@name='expression']")
    assert "StretchWordSpacingToFit" in curved.get("value")
    assert "'default'" in curved.get("value")
    contour = root.find("projectlayers/maplayer[layername='contour']")
    assert contour.find(".//text-style").get("fontSize") == "7"
    color = contour.find(".//layer[@class='SimpleLine']/data_defined_properties//Option[@name='outlineColor']")
    assert "138,79,28" in color.find("Option[@name='expression']").get("value")
    water = root.find("projectlayers/maplayer[layername='water_point']/renderer-v2")
    assert water.get("attr") == "type"
    scrub = root.find("projectlayers/maplayer[layername='vegetation map']//symbol[@name='3']")
    fill = scrub.find("layer[@class='SimpleFill']/Option/Option[@name='color']")
    assert fill.get("value").startswith("163,204,144")
    assert scrub.find("layer[@class='LinePatternFill']") is not None
    scattered = root.find("projectlayers/maplayer[layername='vegetation map']//symbol[@name='2']")
    assert scattered.find("layer[@class='PointPatternFill']") is not None
    assert scattered.find("layer[@class='SimpleFill']") is None
    track = root.find("projectlayers/maplayer[layername='track_line map']//symbol[@name='1']")
    assert track.find("layer[@class='MarkerLine']") is not None
    painted = ET.tostring(root, encoding="unicode")
    assert "213,180,60" not in painted
    assert "234,99,0" not in painted


def test_style_file_has_no_sheet_code():
    # Catches a sheet code in the style file, or a settled ink the apply step no longer reads.
    with open(ov.STYLE_PATH, encoding="utf-8") as handle:
        raw = handle.read()
    for token in ("BX24", "1577000", "5178000", "5172000", "1569000", "5165000", "1584000", "5173000"):
        assert token not in raw, token
    style = ov.STYLE
    assert style["fonts"]["raster_family"] == "NZAT Legible Test"
    assert style["fonts"]["vector_family"] == "Open Sans"
    assert style["fonts"]["stock_family"] == "Nimbus Sans LINZ"
    assert style["contours"]["index"]["colour"] == "#8A4F1C"
    assert style["contours"]["intermediate"]["colour"] == "#C4814B"
    assert style["reference_inks"]["project_road"] == "#D5B43C"
    assert style["reference_inks"]["print_legend_highway"] == "#EA6300"
    assert ov.FAMILY == style["fonts"]["raster_family"]
    assert ov.size_floor("contour", "1") == str(int(style["labels"]["size_floor_pt"]))
    assert ov.size_floor("relief_point map", "1") == str(int(style["labels"]["spot_height_floor_pt"]))
    assert style["labels"]["web_floor_px"] == 10
    assert style["labels"]["place_name_floor_px"] == 11
    assert style["vegetation"]["scrub"]["colour"] == "#A3CC90"
    assert style["vegetation"]["scattered"]["colour"] == "#E0EDD8"


def test_vector_size_floor_reads_the_style_file():
    # Catches a place name left under 11 px, or a web floor that ignores the style file.
    labels = bs.RULES["labels"]
    assert bs.label_floor_px("Place-Label-Suburb", "{label}") == labels["place_name_floor_px"]
    assert bs.label_floor_px("All-Road-Labels", "{name}") == labels["web_floor_px"]
    assert bs.label_floor_px("Place-Symbol-Peak-12", "") == labels["web_floor_px"]
    assert bs.floor_text_size(10, labels["place_name_floor_px"]) == 11
    assert bs.floor_text_size(12, labels["place_name_floor_px"]) == 12
    assert bs.floor_text_size(8, labels["web_floor_px"]) == 10
    assert bs.is_place_name("Place-Label-Suburb", "{label}") is True
    assert bs.is_place_name("Place-Symbol-Peak-12", "") is False


def test_place_ranks_differ_by_at_least_20_percent():
    # Catches a town size under 20% above suburb, or an island layer pulled into the place ladder.
    ranks = bs.RULES["labels"]["place_hierarchy"]
    assert [rank["rank"] for rank in ranks] == ["suburb-locality", "town", "city"]
    assert all(ratio >= 1.2 for ratio in bs.hierarchy_ratios(ranks))
    assert bs.place_rank_size("Place-Label-Suburb") == bs.place_rank_size("Place-Label-Locality")
    assert bs.place_rank_size("Place-Label-City-14") == bs.place_rank_size("Place-Label-City-7")
    assert bs.place_rank_size("Place-Label-Town") / bs.place_rank_size("Place-Label-Suburb") >= 1.2
    assert bs.place_rank_size("Place-Label-Island-12") is None
    assert bs.resolved_text_size(12, 11, 14) == 14
    assert bs.resolved_text_size(10, 11, None) == 11


def test_label_contrast_darkens_water_and_draws_the_buffer():
    # Catches a water name left at process_blue, or a label buffer left undrawn.
    assert bs.text_contrast_min() == bs.RULES["label_contrast"]["min_ratio"] == 4.8
    assert bs.halo_alpha() == 1
    white = (255, 255, 255)
    blue = (0, 158, 255)
    dark = bs.darken_for_text(blue, white, bs.text_contrast_min())
    assert pa.contrast_ratio(pa.rel_luminance(dark), pa.rel_luminance(white)) >= 4.8
    assert pa.rel_luminance(dark) < pa.rel_luminance(blue)
    assert ov._rgb_key(bs.darken_for_text((0, 0, 0), white, 4.8)) == (0, 0, 0)
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>nztopo50_carto_text</layername>
          <labeling type="simple"><settings>
            <text-style textColor="251,73,245,255" fontSize="7">
              <text-buffer bufferDraw="0" bufferOpacity="0.5" bufferColor="250,250,250,128" bufferSize="1"/>
            </text-style>
            <dd_properties><Option type="Map">
              <Option name="properties" type="Map">
                <Option name="Color" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="project_color_object( &quot;colour&quot; )"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
            </Option></dd_properties>
          </settings></labeling>
        </maplayer>
        """
    )
    contour = ET.fromstring(
        """
        <maplayer>
          <layername>contour</layername>
          <labeling><settings>
            <text-style textColor="255,180,29,255" fontSize="7">
              <text-buffer bufferDraw="0" bufferOpacity="1" bufferColor="250,250,250,255" bufferSize="0.5"/>
            </text-style>
          </settings></labeling>
        </maplayer>
        """
    )
    palette = [("black", "0,0,0,255"), ("process_blue", "0,158,255,255")]
    ov.patch_label_contrast(layer, palette=palette)
    ov.patch_label_contrast(contour, palette=palette)
    buf = layer.find(".//text-buffer")
    assert buf.get("bufferDraw") == "1"
    assert buf.get("bufferOpacity") == "1"
    assert buf.get("bufferSize") == "1"
    assert buf.get("bufferColor").startswith("250,250,250,255")
    expr = layer.find(".//Option[@name='Color']/Option[@name='expression']").get("value")
    assert "process_blue" in expr
    assert "WHEN \"colour\" = 'black'" not in expr
    assert "color_rgb(0,158,255)" not in expr
    behind = ov.label_behind(buf)
    expected = ov._rgb_key(bs.darken_for_text((0, 158, 255), behind, 4.8))
    assert f"color_rgb({expected[0]},{expected[1]},{expected[2]})" in expr
    contour_buf = contour.find(".//text-buffer")
    assert contour_buf.get("bufferDraw") == "1"
    assert contour_buf.get("bufferSize") == "0.5"
    contour_ink = ov.parse_qgis_colour(contour.find(".//text-style").get("textColor"))
    assert pa.contrast_ratio(pa.rel_luminance(contour_ink[:3]), pa.rel_luminance((250, 250, 250))) >= 4.8
    assert contour_ink[:3] != (255, 180, 29)


def test_vegetation_reads_the_style_file():
    # Catches a vector scrub fill that ignores the JSON, or a missing hatch on raster scrub.
    veg = bs.RULES["vegetation"]
    assert bs.vegetation_fill("scrub") == "rgba(163, 204, 144, 1)"
    assert bs.vegetation_fill("scattered") == "rgba(224, 237, 216, 1)"
    assert veg["scrub"]["colour"] == "#A3CC90"
    assert veg["scattered"]["colour"] == "#E0EDD8"
    assert "scrub" not in bs.P
    assert "scattered_scrub" not in bs.P
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
    ov.patch_vegetation(layer)
    scrub = layer.find(".//symbol[@name='3']")
    fill = scrub.find("layer[@class='SimpleFill']/Option/Option[@name='color']")
    assert fill.get("value").startswith("163,204,144")
    assert scrub.find("layer[@class='LinePatternFill']") is not None
    scattered = layer.find(".//symbol[@name='2']")
    assert scattered.find("layer[@class='PointPatternFill']") is not None
    assert scattered.find("layer[@class='SimpleFill']") is None


def test_multiline_baseline_splits_at_a_fold():
    # Catches the estuary name left on one folded line, so the words still stack.
    estuary = [
        (1577379.6, 5178302.3),
        (1578853.9, 5178302.3),
        (1577379.6, 5178107.5),
        (1578853.9, 5178107.5),
    ]
    passes = ov.split_wrap_baseline(estuary, 2)
    assert len(passes) == 2
    assert passes[0] == estuary[:2]
    assert passes[1] == estuary[2:]
    reverse = [(0.0, 0.0), (400.0, 0.0), (0.0, -80.0)]
    assert len(ov.split_wrap_baseline(reverse, 2)) == 2
    assert ov.split_wrap_baseline(estuary, 1) == [estuary]
    root = ET.fromstring(
        """
        <maplayer>
          <layername>nztopo50_carto_text</layername>
          <labeling type="simple"><settings>
            <text-style fontFamily="Nimbus Sans LINZ" fontItalic="0" fontSize="7" namedStyle="Regular"/>
            <placement geometryGenerator="" geometryGeneratorEnabled="0" geometryGeneratorType="PointGeometry"/>
            <dd_properties><Option type="Map">
              <Option name="properties" type="Map">
                <Option name="CurvedLabelMode" type="Map">
                  <Option name="field" type="QString" value="charplace"/>
                  <Option name="type" type="int" value="2"/>
                </Option>
              </Option>
            </Option></dd_properties>
          </settings></labeling>
        </maplayer>
        """
    )
    ov.patch_labels(root, "nztopo50_carto_text")
    placement = root.find("./labeling/settings/placement")
    assert placement.get("geometryGeneratorEnabled") == "1"
    assert placement.get("geometryGeneratorType") == "LineGeometry"
    assert "text_string" in placement.get("geometryGenerator")
    curved = root.find(".//Option[@name='CurvedLabelMode']/Option[@name='expression']")
    assert curved.get("value") == ov.curved_label_mode_expression()


def test_qgis_prefix_uses_the_environment():
    # Catches a Mac run that still points QGIS at /usr.
    assert rs.qgis_prefix(None) == "/usr"
    assert rs.qgis_prefix("") == "/usr"
    assert rs.qgis_prefix("  ") == "/usr"
    assert rs.qgis_prefix("/Applications/QGIS.app/Contents/MacOS") == "/Applications/QGIS.app/Contents/MacOS"


def test_square_uses_the_sheet_layer_set():
    # Catches a square that draws landcover_line. The sheet map hides that layer.
    ordered = ["contour_id", "landcover_line_id", "building_point_id", "building_point_map_id"]
    visible = ["contour_id", "building_point_map_id"]
    assert rs.SHEET_PRESET == "Map5View"
    assert rs.sheet_layer_ids(ordered, visible) == ["contour_id", "building_point_map_id"]


def test_square_extent_is_one_kilometre():
    # Catches a square that is not 1000 m on a side, or a pixel size other than the 600 dpi sheet size.
    assert rs.METRES == 1000
    assert rs.DPI == 600
    assert rs.PX == 472
    assert rs.square_extent(1577000, 5178000) == (1577000, 5178000, 1578000, 5179000)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
