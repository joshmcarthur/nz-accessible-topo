import json
import os
import tempfile
import xml.etree.ElementTree as ET

from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.darken import darken_for_text
from nzat.colour.rel_luminance import rel_luminance
from nzat.qgis.capped_buffer_mm import capped_buffer_mm
from nzat.qgis.carto_fit_text_expression import carto_fit_text_expression
from nzat.qgis.carto_fit_value import carto_fit_value
from nzat.qgis.carto_flat_line_expression import carto_flat_line_expression
from nzat.qgis.carto_flat_wrap_expression import carto_flat_wrap_expression
from nzat.qgis.carto_text_width_expression import carto_text_width_expression
from nzat.qgis.curved_label_mode_expression import curved_label_mode_expression
from nzat.qgis.defaults import (
    CARTO_FIT_FILE,
    CARTO_FLAT_TEXT,
    CARTO_POINT_FILTER,
    SHEET_SCALE,
    STYLE,
)
from nzat.qgis.expr import expr
from nzat.qgis.format_buffer_mm import format_buffer_mm
from nzat.qgis.label_behind import label_behind
from nzat.qgis.load_carto_fit import load_carto_fit
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.patch_label_contrast import patch_label_contrast
from nzat.qgis.patch_labels import patch_labels
from nzat.qgis.rgb_key import rgb_key
from nzat.qgis.size_floor import size_floor
from nzat.qgis.split_wrap_baseline import split_wrap_baseline
from nzat.qgis.upright_style_name import upright_style_name
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path

RULES = load_rules()

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


def test_upright_style_and_size_floor():
    # Catches a label style that stays italic, or a spot height lifted to 7 pt.
    for name in ("Italic", "Narrow Italic", "Narrow", "Narrow Bold", ""):
        assert upright_style_name(name) == "Regular"
    assert upright_style_name("Regular") == "Regular"
    assert size_floor("contour", "5") == "7"
    assert size_floor("contour", "10") == "10"
    assert size_floor("relief_point map", "5") == "6"
    assert size_floor("relief_point map", "6") == "6"


def test_label_contrast_darkens_water_and_draws_the_buffer():
    # Catches a water name left at process_blue, or a label buffer left at the stock millimetre size.
    assert (
        lookup_style_path(RULES, "label_contrast.min_ratio")
        == RULES["label_contrast"]["min_ratio"]
        == 4.8
    )
    assert lookup_style_path(RULES, "label_contrast.halo_alpha") == 1
    assert RULES["label_contrast"]["halo_max_mm"] == 0.4
    assert format_buffer_mm(capped_buffer_mm("1", 0.4)) == "0.4"
    assert format_buffer_mm(capped_buffer_mm("0.5", 0.4)) == "0.4"
    assert format_buffer_mm(capped_buffer_mm("0.2", 0.4)) == "0.2"
    white = (255, 255, 255)
    blue = (0, 158, 255)
    dark = darken_for_text(
        blue, white, lookup_style_path(RULES, "label_contrast.min_ratio")
    )
    assert contrast_ratio(rel_luminance(dark), rel_luminance(white)) >= 4.8
    assert rel_luminance(dark) < rel_luminance(blue)
    assert rgb_key(darken_for_text((0, 0, 0), white, 4.8)) == (0, 0, 0)
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
    patch_label_contrast(layer, palette=palette)
    patch_label_contrast(contour, palette=palette)
    buf = layer.find(".//text-buffer")
    assert buf.get("bufferDraw") == "1"
    assert buf.get("bufferOpacity") == "1"
    assert buf.get("bufferSize") == "0.4"
    assert buf.get("bufferColor").startswith("250,250,250,255")
    expr = layer.find(".//Option[@name='Color']/Option[@name='expression']").get(
        "value"
    )
    assert "process_blue" in expr
    assert "WHEN \"colour\" = 'black'" not in expr
    assert "color_rgb(0,158,255)" not in expr
    behind = label_behind(buf)
    expected = rgb_key(darken_for_text((0, 158, 255), behind, 4.8))
    assert f"color_rgb({expected[0]},{expected[1]},{expected[2]})" in expr
    contour_buf = contour.find(".//text-buffer")
    assert contour_buf.get("bufferDraw") == "1"
    assert contour_buf.get("bufferSize") == "0.4"
    contour_ink = parse_qgis_colour(contour.find(".//text-style").get("textColor"))
    assert (
        contrast_ratio(rel_luminance(contour_ink[:3]), rel_luminance((250, 250, 250)))
        >= 4.8
    )
    assert contour_ink[:3] != (255, 180, 29)
    spot = ET.fromstring(
        """
        <maplayer>
          <layername>relief_point map</layername>
          <labeling><settings>
            <text-style textColor="0,0,0,255" fontSize="6">
              <text-buffer bufferDraw="0" bufferOpacity="1" bufferColor="255,255,255,255" bufferSize="0.5"/>
            </text-style>
          </settings></labeling>
        </maplayer>
        """
    )
    patch_label_contrast(spot)
    spot_buf = spot.find(".//text-buffer")
    assert spot_buf.get("bufferColor").startswith("188,186,182")


def test_multiline_baseline_splits_at_a_fold():
    # Catches the estuary name left on one folded line, so the words still stack.
    estuary = [
        (1577379.6, 5178302.3),
        (1578853.9, 5178302.3),
        (1577379.6, 5178107.5),
        (1578853.9, 5178107.5),
    ]
    passes = split_wrap_baseline(estuary, 2)
    assert len(passes) == 2
    assert passes[0] == estuary[:2]
    assert passes[1] == estuary[2:]
    reverse = [(0.0, 0.0), (400.0, 0.0), (0.0, -80.0)]
    assert len(split_wrap_baseline(reverse, 2)) == 2
    assert split_wrap_baseline(estuary, 1) == [estuary]
    root = ET.fromstring(CARTO_TEXT_LAYER_XML)
    patch_labels(root, "nztopo50_carto_text")
    assert root.find("labeling").get("type") == "rule-based"
    line_rule, point_rule = root.findall("./labeling/rules/rule")
    assert line_rule.get("filter") == f"NOT ({CARTO_POINT_FILTER})"
    placement = line_rule.find("settings/placement")
    assert placement.get("geometryGeneratorEnabled") == "1"
    assert placement.get("geometryGeneratorType") == "LineGeometry"
    assert "text_string" in placement.get("geometryGenerator")
    curved = line_rule.find(
        ".//Option[@name='CurvedLabelMode']/Option[@name='expression']"
    )
    assert curved.get("value") == curved_label_mode_expression()
    # Catches a stretch that squeezes a name onto a short baseline, or that drops the stock spread on a long one.
    assert "length($geometry) <= " + carto_text_width_expression(
        'length("text_string")'
    ) in curved.get("value")
    assert "THEN 'default' ELSE \"charplace\" END" in curved.get("value")
    # Catches a flat one-line name left on its fixed baseline.
    assert point_rule.get("filter") == CARTO_POINT_FILTER
    # Catches a curved area name, such as Banks Peninsula, pulled off its long baseline.
    assert "num_points($geometry) <= 2" in CARTO_POINT_FILTER
    point = point_rule.find("settings/placement")
    assert point.get("placement") == "2"
    assert point.get("placementFlags") == "14"
    assert point.get("geometryGeneratorType") == "LineGeometry"
    assert point.get("geometryGenerator") == carto_flat_line_expression()
    allowance_m = STYLE["labels"]["carto_point"]["allowance_mm"] * SHEET_SCALE / 1000
    assert f"+ {allowance_m:g})" in point.get("geometryGenerator")
    assert point_rule.find(".//Option[@name='CurvedLabelMode']") is None
    # Catches a dual name left on one line, or a split that drops the slash.
    point_text = point_rule.find("settings/text-style")
    assert point_text.get("fieldName") == CARTO_FLAT_TEXT
    assert point_text.get("isExpression") == "1"
    assert "' /\\n'" in CARTO_FLAT_TEXT
    assert point.get("multipartBehavior") == "LabelLargestPartOnly"
    assert line_rule.find("settings/text-style").get("isExpression") is None
    # Catches a wrap that also breaks dual names, a lone leading "Te", or the line height left at 1.
    wrap = point_rule.find(
        ".//Option[@name='AutoWrapLength']/Option[@name='expression']"
    )
    assert wrap.get("value") == carto_flat_wrap_expression()
    assert "strpos(\"text_string\", ' / ') = 0" in wrap.get("value")
    assert "'Te\u00a0'" in CARTO_FLAT_TEXT
    assert point_text.get("multilineHeight") == str(
        STYLE["labels"]["carto_point"]["line_height"]
    )
    assert line_rule.find(".//Option[@name='AutoWrapLength']") is None
    assert point_rule.find(".//Option[@name='PositionX']") is None


def test_carto_fit_places_listed_names():
    # Catches a fit file that is not read, a fitted row not pinned to its point, or a one-line fit that still breaks.
    with tempfile.TemporaryDirectory() as folder:
        assert load_carto_fit(folder) == {}
        with open(
            os.path.join(folder, CARTO_FIT_FILE), "w", encoding="utf-8"
        ) as handle:
            json.dump({"row-1": {"x": 1569900.5, "y": 5165760.0, "lines": 1}}, handle)
        fit = load_carto_fit(folder)
    root = ET.fromstring(CARTO_TEXT_LAYER_XML)
    patch_labels(root, "nztopo50_carto_text", fit=fit)
    point_rule = root.findall("./labeling/rules/rule")[1]
    props = point_rule.find("settings/dd_properties/Option/Option[@name='properties']")
    assert expr(props, "PositionX") == carto_fit_value(fit, "x")
    assert expr(props, "PositionY") == carto_fit_value(fit, "y")
    assert "1569900.5" in expr(props, "PositionX")
    assert expr(props, "Hali") == "'Center'"
    assert expr(props, "Vali") == "'Bottom'"
    text = point_rule.find("settings/text-style").get("fieldName")
    assert text == carto_fit_text_expression(fit)
    assert text.startswith("CASE WHEN ") and CARTO_FLAT_TEXT in text
    assert expr(props, "AutoWrapLength").startswith("CASE WHEN ")
    assert "O''Brien" in carto_fit_value({"O'Brien": {"x": 1}}, "x")


def test_natural_names_take_the_natural_ink_and_narrow_stays_regular():
    # Catches Narrow settlement names sent to the natural style, or italic
    # natural names left black (the face has no Bold file, log 0072).
    layer = ET.fromstring(
        """
        <maplayer>
          <layername>nztopo50_carto_text</layername>
          <labeling type="simple"><settings>
            <text-style textColor="0,0,0,255" fontSize="7" namedStyle="Italic">
              <text-buffer bufferDraw="1" bufferOpacity="1" bufferColor="255,255,255,255" bufferSize="0.4"/>
            </text-style>
            <dd_properties><Option type="Map">
              <Option name="properties" type="Map">
                <Option name="FontStyle" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="&quot;style&quot;"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
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
    patch_labels(layer, "nztopo50_carto_text", palette=[("black", "0,0,0,255")])
    props = layer.find(".//dd_properties/Option/Option[@name='properties']")
    style = expr(props, "FontStyle")
    assert "LIKE '%narrow%' THEN 'Regular'" in style
    assert "OR lower" not in style
    colour = expr(props, "Color")
    assert colour.startswith(
        "CASE WHEN \"colour\" = 'black' AND lower(coalesce(\"style\", '')) LIKE '%italic%'"
        " THEN color_rgb(122,85,66)"
    )
