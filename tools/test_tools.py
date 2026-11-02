#!/usr/bin/env python3
"""Sanity tests for the measurement and rendering tools. Run: python3 tools/test_tools.py"""
import json
import os
import sys
import tempfile
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
    lines = contour.findall(".//symbol[@name='0']/layer[@class='SimpleLine']")
    assert len(lines) == 2
    casing_color = lines[0].find("data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']")
    assert "138,79,28" in casing_color.get("value")
    assert "196,129,75" not in casing_color.get("value")
    enabled = lines[0].find("data_defined_properties//Option[@name='enabled']/Option[@name='expression']")
    assert "% 100 <> 0" in enabled.get("value")
    fill_color = lines[1].find("data_defined_properties//Option[@name='outlineColor']/Option[@name='expression']")
    assert "138,79,28" in fill_color.get("value")
    assert "196,129,75" in fill_color.get("value")
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
        </qgis>
        """
    )
    ov.apply(root)
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
    assert style["contours"]["index"]["width_mm"] == 0.45
    assert style["contours"]["intermediate"]["colour"] == "#C4814B"
    assert style["contours"]["intermediate"]["casing_colour"] == "#8A4F1C"
    assert style["contours"]["intermediate"]["casing_width_mm"] == 0.2
    assert style["reference_inks"]["project_road"] == "#D5B43C"
    assert style["reference_inks"]["print_legend_highway"] == "#EA6300"
    assert ov.FAMILY == style["fonts"]["raster_family"]
    assert ov.size_floor("contour", "1") == str(int(style["labels"]["size_floor_pt"]))
    assert ov.size_floor("relief_point map", "1") == str(int(style["labels"]["spot_height_floor_pt"]))
    assert style["labels"]["web_floor_px"] == 10
    assert style["labels"]["place_name_floor_px"] == 11
    assert style["labels"]["letter_spacing_em"] == 0.05
    assert style["vegetation"]["scrub"]["colour"] == "#A3CC90"
    assert style["vegetation"]["scattered"]["colour"] == "#E0EDD8"
    assert style["tracks"]["closed_foot"]["casing_colour"] == "#1A1A1A"
    assert style["tracks"]["access"]["reserved_channel"] == "casing_colour"
    assert style["tracks"]["access"]["painted"] is False
    assert style["draw_order"] == [{"name": "vegetation map", "below": "contour"}]
    assert style["label_contrast"]["red_light_min"] == 3.0


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
    assert bs.letter_spacing_em() == 0.05
    assert "letter_spacing_em" not in bs.P


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
    # Catches a water name left at process_blue, or a label buffer left at the stock millimetre size.
    assert bs.text_contrast_min() == bs.RULES["label_contrast"]["min_ratio"] == 4.8
    assert bs.halo_alpha() == 1
    assert bs.RULES["label_contrast"]["halo_max_mm"] == 0.4
    assert ov.format_buffer_mm(ov.capped_buffer_mm("1", 0.4)) == "0.4"
    assert ov.format_buffer_mm(ov.capped_buffer_mm("0.5", 0.4)) == "0.4"
    assert ov.format_buffer_mm(ov.capped_buffer_mm("0.2", 0.4)) == "0.2"
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
    assert buf.get("bufferSize") == "0.4"
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
    assert contour_buf.get("bufferSize") == "0.4"
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


def test_track_access_channel_is_reserved():
    # Catches access painted, a reserved channel other than casing_colour, or an access ink added to the style file.
    access = bs.RULES["tracks"]["access"]
    assert access["reserved_channel"] == "casing_colour"
    assert access["painted"] is False
    assert "colour" not in access
    assert bs.track_access_reserved_channel() == "casing_colour"
    assert bs.track_access_painted() is False


def test_closed_tracks_read_the_style_file():
    # Catches a vector closed-track casing that ignores the JSON, or a raster warm_red left below 3:1 under red light.
    track = bs.RULES["tracks"]["closed_foot"]
    assert track["casing_colour"] == "#1A1A1A"
    assert track["casing_alpha"] == 0.55
    assert bs.closed_track_casing() == "rgba(26, 26, 26, 0.55)"
    assert "closed_track_shadow" not in bs.P
    assert bs.red_light_min() == 3.0
    behind = (250, 250, 250)
    warm = (255, 69, 0)
    dark = bs.darken_for_text(warm, behind, 4.8, 3.0)
    assert pa.contrast_ratio(pa.red_light_reflectance(dark), pa.red_light_reflectance(behind)) >= 3.0
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
    palette = [("warm_red", "255,69,0,255"), ("black", "0,0,0,255")]
    ov.patch_label_contrast(layer, palette=palette)
    expr = layer.find(".//Option[@name='Color']/Option[@name='expression']").get("value")
    assert "warm_red" in expr
    assert "color_rgb(255,69,0)" not in expr
    assert "WHEN \"colour\" = 'black'" not in expr
    expected = ov._rgb_key(dark)
    assert f"color_rgb({expected[0]},{expected[1]},{expected[2]})" in expr
    track_layer = ET.fromstring(
        """
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
        """
    )
    ov.patch_tracks(track_layer)
    assert track_layer.find(".//layer[@class='MarkerLine']") is not None


def test_contour_casing_read_the_style_file():
    # Catches an intermediate contour with no index-ink casing, or a vector casing that ignores the JSON.
    mid = bs.RULES["contours"]["intermediate"]
    assert mid["casing_colour"] == "#8A4F1C"
    assert mid["casing_width_mm"] == 0.2
    assert bs.RULES["contours"]["index"]["width_mm"] == 0.45
    assert bs.contour_colour("index") == "#8A4F1C"
    assert bs.contour_colour("intermediate") == "#C4814B"
    assert bs.intermediate_casing_colour() == "#8A4F1C"
    assert bs.intermediate_casing_width()["stops"] == [[12, 1.0], [16, 1.5]]
    layer = ET.fromstring(
        """
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
        """
    )
    ov.patch_contour(layer)
    lines = layer.findall(".//layer[@class='SimpleLine']")
    assert len(lines) == 2
    enabled = lines[0].find("data_defined_properties//Option[@name='enabled']/Option[@name='expression']")
    assert "% 100 <> 0" in enabled.get("value")
    width = lines[0].find("data_defined_properties//Option[@name='outlineWidth']/Option[@name='expression']")
    assert width.get("value") == "0.2"
    fill_width = lines[1].find("data_defined_properties//Option[@name='outlineWidth']/Option[@name='expression']")
    assert "0.45" in fill_width.get("value")
    assert "0.12" in fill_width.get("value")


def test_springs_and_native_read_the_style_file():
    # Catches a vector native fill that ignores the JSON, or a raster spring that keeps one glyph for hot and cold.
    assert bs.vegetation_fill("native") == "rgba(225, 234, 195, 1)"
    assert bs.RULES["vegetation"]["native"]["colour"] == "#E1EAC3"
    assert bs.spring_colour("hot") == "rgba(20, 20, 20, 1)"
    assert bs.spring_colour("cold") == "rgba(0, 92, 143, 1)"
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
    ov.patch_springs(layer)
    marker = layer.find(".//layer[@class='SimpleMarker']/data_defined_properties/Option/Option[@name='properties']")
    name_expr = marker.find("Option[@name='name']/Option[@name='expression']").get("value")
    assert "cross2" in name_expr
    assert "circle" in name_expr
    colour_expr = marker.find("Option[@name='fillColor']/Option[@name='expression']").get("value")
    assert "20,20,20" in colour_expr.replace(" ", "") or "color_rgb(20,20,20)" in colour_expr.replace(" ", "")
    assert "0,92,143" in colour_expr.replace(" ", "") or "color_rgb(0,92,143)" in colour_expr.replace(" ", "")
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
    ov.patch_vegetation(veg)
    native = veg.find(".//symbol[@name='1']/layer[@class='SimpleFill']/Option/Option[@name='color']")
    assert native.get("value").startswith("225,234,195")


CARTO_TEXT_LAYER_XML = """
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
    root = ET.fromstring(CARTO_TEXT_LAYER_XML)
    ov.patch_labels(root, "nztopo50_carto_text")
    assert root.find("labeling").get("type") == "rule-based"
    line_rule, point_rule = root.findall("./labeling/rules/rule")
    assert line_rule.get("filter") == f"NOT ({ov.CARTO_POINT_FILTER})"
    placement = line_rule.find("settings/placement")
    assert placement.get("geometryGeneratorEnabled") == "1"
    assert placement.get("geometryGeneratorType") == "LineGeometry"
    assert "text_string" in placement.get("geometryGenerator")
    curved = line_rule.find(".//Option[@name='CurvedLabelMode']/Option[@name='expression']")
    assert curved.get("value") == ov.curved_label_mode_expression()
    # Catches a flat one-line name left on its fixed baseline.
    assert point_rule.get("filter") == ov.CARTO_POINT_FILTER
    point = point_rule.find("settings/placement")
    assert point.get("placement") == "2"
    assert point.get("placementFlags") == "14"
    assert point.get("geometryGeneratorType") == "LineGeometry"
    assert point.get("geometryGenerator") == ov.carto_flat_line_expression()
    allowance_m = ov.STYLE["labels"]["carto_point"]["allowance_mm"] * ov.SHEET_SCALE / 1000
    assert f"+ {allowance_m:g})" in point.get("geometryGenerator")
    assert point_rule.find(".//Option[@name='CurvedLabelMode']") is None
    # Catches a dual name left on one line, or a split that drops the slash.
    point_text = point_rule.find("settings/text-style")
    assert point_text.get("fieldName") == ov.CARTO_FLAT_TEXT
    assert point_text.get("isExpression") == "1"
    assert "' /\\n'" in ov.CARTO_FLAT_TEXT
    assert point.get("multipartBehavior") == "LabelLargestPartOnly"
    assert line_rule.find("settings/text-style").get("isExpression") is None
    # Catches a wrap that also breaks dual names, a lone leading "Te", or the line height left at 1.
    wrap = point_rule.find(".//Option[@name='AutoWrapLength']/Option[@name='expression']")
    assert wrap.get("value") == ov.carto_flat_wrap_expression()
    assert "strpos(\"text_string\", ' / ') = 0" in wrap.get("value")
    assert "'Te\u00a0'" in ov.CARTO_FLAT_TEXT
    assert point_text.get("multilineHeight") == str(ov.STYLE["labels"]["carto_point"]["line_height"])
    assert line_rule.find(".//Option[@name='AutoWrapLength']") is None
    assert point_rule.find(".//Option[@name='PositionX']") is None


def test_carto_fit_places_listed_names():
    # Catches a fit file that is not read, a fitted row not pinned to its point, or a one-line fit that still breaks.
    with tempfile.TemporaryDirectory() as folder:
        assert ov.load_carto_fit(folder) == {}
        with open(os.path.join(folder, ov.CARTO_FIT_FILE), "w", encoding="utf-8") as handle:
            json.dump({"row-1": {"x": 1569900.5, "y": 5165760.0, "lines": 1}}, handle)
        fit = ov.load_carto_fit(folder)
    root = ET.fromstring(CARTO_TEXT_LAYER_XML)
    ov.patch_labels(root, "nztopo50_carto_text", fit=fit)
    point_rule = root.findall("./labeling/rules/rule")[1]
    props = point_rule.find("settings/dd_properties/Option/Option[@name='properties']")
    assert ov._expr(props, "PositionX") == ov.carto_fit_value(fit, "x")
    assert ov._expr(props, "PositionY") == ov.carto_fit_value(fit, "y")
    assert "1569900.5" in ov._expr(props, "PositionX")
    assert ov._expr(props, "Hali") == "'Center'"
    assert ov._expr(props, "Vali") == "'Bottom'"
    text = point_rule.find("settings/text-style").get("fieldName")
    assert text == ov.carto_fit_text_expression(fit)
    assert text.startswith("CASE WHEN ") and ov.CARTO_FLAT_TEXT in text
    assert ov._expr(props, "AutoWrapLength").startswith("CASE WHEN ")
    assert "O''Brien" in ov.carto_fit_value({"O'Brien": {"x": 1}}, "x")


def test_hillshade_is_an_optional_overlay():
    # Catches azimuth other than 337.5, a missing painted flag, a raster file other than dem.tif, or hillshade_direction left in P.
    shade = bs.RULES["hillshade"]
    assert shade["painted"] is True
    assert shade["raster_file"] == "dem.tif"
    assert shade["azimuth_deg"] == 337.5
    assert shade["altitude_deg"] == 45
    assert shade["multidirectional"] is True
    assert shade["fill_azimuths_deg"] == [292.5, 22.5]
    assert "hillshade_direction" not in bs.P
    assert bs.hillshade_azimuth() == 337.5
    assert bs.hillshade_fill_azimuths() == [292.5, 22.5]
    assert bs.hillshade_painted() is True
    assert ov.DEM_LAYER_NAME == "dem"
    assert ov.hillshade_should_paint(None) is False
    assert rs.with_dem_layer(["a", "b"], None) == ["a", "b"]
    assert rs.with_dem_layer(["a", "b"], "dem") == ["dem", "a", "b"]
    assert rs.with_dem_layer(["dem", "a"], "dem") == ["dem", "a"]


def test_hillshade_stays_off_without_a_dem():
    # Catches the shader left on, or the light left at 315, when dem.tif is missing.
    root = ET.fromstring(
        """
        <qgis>
          <projectCrs><spatialrefsys><srid>2193</srid></spatialrefsys></projectCrs>
          <elevation-shading-renderer hillshading-is-active="1" hillshading-is-multidirectional="0" hillshading-z-factor="1" is-active="1" light-altitude="45" light-azimuth="315"/>
          <layer-tree-group/>
          <projectlayers/>
          <ElevationProperties>
            <terrainProvider type="flat"><TerrainProvider offset="0" scale="1"/></terrainProvider>
          </ElevationProperties>
        </qgis>
        """
    )
    ov.patch_hillshade(root, project_dir="/tmp/missing-nzat-dem")
    renderer = root.find("elevation-shading-renderer")
    assert renderer.get("light-azimuth") == "337.5"
    assert renderer.get("light-altitude") == "45"
    assert renderer.get("hillshading-is-multidirectional") == "1"
    assert renderer.get("is-active") == "0"
    assert renderer.get("hillshading-is-active") == "0"
    assert root.find("projectlayers/maplayer[layername='dem']") is None


def test_hillshade_turns_on_when_dem_is_present():
    # Catches a present dem.tif that does not turn the shader on, or a painted false that still shades.
    root = ET.fromstring(
        """
        <qgis>
          <projectCrs><spatialrefsys><srid>2193</srid></spatialrefsys></projectCrs>
          <elevation-shading-renderer hillshading-is-active="0" hillshading-is-multidirectional="0" hillshading-z-factor="1" is-active="0" light-altitude="45" light-azimuth="315"/>
          <layer-tree-group/>
          <projectlayers/>
          <ElevationProperties>
            <terrainProvider type="flat"><TerrainProvider offset="0" scale="1"/></terrainProvider>
          </ElevationProperties>
        </qgis>
        """
    )
    with tempfile.TemporaryDirectory() as folder:
        open(os.path.join(folder, "dem.tif"), "wb").close()
        ov.patch_hillshade(root, project_dir=folder)
        off = {"hillshade": {**ov.hillshade_rules(), "painted": False}}
        assert ov.hillshade_should_paint(folder, off) is False
    renderer = root.find("elevation-shading-renderer")
    assert renderer.get("is-active") == "1"
    assert renderer.get("hillshading-is-active") == "1"
    assert root.find("projectlayers/maplayer[layername='dem']/datasource").text == "./dem.tif"
    assert root.find("ElevationProperties/terrainProvider").get("type") == "raster"
    assert root.find("ElevationProperties/terrainProvider/TerrainProvider").get("layer") == ov.DEM_LAYER_ID


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
