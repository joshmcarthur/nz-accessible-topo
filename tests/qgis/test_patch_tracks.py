import json
import xml.etree.ElementTree as ET

from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.darken import darken_for_text
from nzat.colour.red_light import red_light_reflectance
from nzat.qgis.defaults import STYLE
from nzat.qgis.patch_label_contrast import patch_label_contrast
from nzat.qgis.patch_tracks import patch_tracks
from nzat.qgis.rgb_key import rgb_key
from nzat.style.closed_track_casing import closed_track_casing
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.vector_params import P

RULES = load_rules()


def test_closed_tracks_read_the_style_file():
    # Catches a vector closed-track casing that ignores the JSON, a 1 mm × left in every gap, or a raster warm_red left below 3:1 under red light.
    track = RULES["tracks"]["closed_foot"]
    assert track["casing_colour"] == "#1A1A1A"
    assert track["casing_alpha"] == 0.55
    assert closed_track_casing(RULES) == "rgba(26, 26, 26, 0.55)"
    assert "closed_track_shadow" not in P
    assert lookup_style_path(RULES, "label_contrast.red_light_min") == 3.0
    behind = (250, 250, 250)
    warm = (255, 69, 0)
    dark = darken_for_text(warm, behind, 4.8, 3.0)
    assert (
        contrast_ratio(red_light_reflectance(dark), red_light_reflectance(behind))
        >= 3.0
    )
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
    patch_label_contrast(layer, palette=palette)
    expr = layer.find(".//Option[@name='Color']/Option[@name='expression']").get(
        "value"
    )
    assert "warm_red" in expr
    assert "color_rgb(255,69,0)" not in expr
    assert "WHEN \"colour\" = 'black'" not in expr
    expected = rgb_key(dark)
    assert f"color_rgb({expected[0]},{expected[1]},{expected[2]})" in expr
    track_layer = ET.fromstring(
        """
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
        """
    )
    patch_tracks(track_layer)
    angle = track_layer.find(
        ".//symbol[@name='@closed']/layer[@class='SimpleMarker']/Option/Option[@name='angle']"
    )
    size = track_layer.find(
        ".//symbol[@name='@closed']/layer[@class='SimpleMarker']/Option/Option[@name='size']"
    )
    marker = track_layer.find(
        ".//symbol[@name='@closed']/layer[@class='SimpleMarker']/Option/Option[@name='name']"
    )
    assert angle.get("value") == str(
        STYLE["tracks"]["closed_foot"]["crossbar_angle_deg"]
    )
    assert size.get("value") == str(STYLE["tracks"]["closed_foot"]["crossbar_size_mm"])
    assert marker.get("value") == STYLE["tracks"]["closed_foot"]["marker"]
    assert marker.get("value") == "cross2"
    interval = track_layer.find(
        ".//layer[@class='MarkerLine'][last()]/Option/Option[@name='interval']"
    )
    along = track_layer.find(
        ".//layer[@class='MarkerLine'][last()]/Option/Option[@name='offset_along_line']"
    )
    assert interval.get("value") == str(
        STYLE["tracks"]["closed_foot"]["marker_interval_mm"]
    )
    assert interval.get("value") == "3"
    assert along.get("value") == "1.25"
    width = track_layer.find(
        ".//Option[@name='outlineWidth']/Option[@name='expression']"
    ).get("value")
    assert "0.2" in width
    assert "0.45" not in width
    again = json.loads(json.dumps(STYLE))
    again["tracks"]["closed_foot"]["crossbar_angle_deg"] = 45
    patch_tracks(track_layer, again)
    assert angle.get("value") == "45"
    # Catches the cross drawn on open foot tracks: QGIS reads NULL as enabled.
    enabled = track_layer.find(
        ".//layer[@class='MarkerLine'][last()]//Option[@name='enabled']/Option[@name='expression']"
    ).get("value")
    assert enabled == "coalesce(\"status\", '') = 'closed'"


def _foot_layer():
    return ET.fromstring(
        """
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


def _enabled(layer):
    node = layer.find(
        "data_defined_properties//Option[@name='enabled']/Option[@name='expression']"
    )
    return None if node is None else node.get("value")


def _evaluate(expression, status, track_type):
    """Evaluate the small coalesce() filters the patch writes, NULL as None."""
    if expression is None:
        return True
    fields = {"status": status or "", "track_type": track_type or ""}
    field, rest = expression.removeprefix('coalesce("').split("\", '')", 1)
    value = fields[field]
    rest = rest.strip()
    if rest.startswith("NOT IN"):
        return value not in ("route", "connector")
    return value == rest.removeprefix("= ").strip("'")


def _drawn(symbol, status, track_type):
    drawn = []
    for layer in symbol.findall("layer"):
        if _evaluate(_enabled(layer), status, track_type):
            marker = layer.find("symbol")
            drawn.append(marker.get("name") if marker is not None else "dashes")
    return drawn


def test_poled_routes_draw_dots():
    layer = _foot_layer()
    patch_tracks(layer)
    patch_tracks(layer)
    symbol = layer.find(".//symbol[@name='1']")
    # Catches a second apply that stacks a second set of dot or × markers.
    assert len(symbol.findall("layer[@class='MarkerLine']")) == 3
    # Catches an open poled route drawn with the foot-track dashes, not dots.
    assert _drawn(symbol, None, "route") == ["@route"]
    assert _drawn(symbol, None, "connector") == ["@connector"]
    # Catches a closed poled route that loses the × under its dots.
    assert _drawn(symbol, "closed", "route") == [
        "@route",
        "@closed",
    ]
    # Catches the × on an open foot track (NULL status and NULL track_type).
    assert _drawn(symbol, None, None) == ["dashes"]
    assert _drawn(symbol, "closed", None) == ["dashes", "@closed"]


def test_track_weights_read_the_style_file():
    # Catches a hard-coded weight, dot size or × size that ignores the JSON.
    style = json.loads(json.dumps(STYLE))
    style["tracks"]["closed_foot"]["open_width_mm"] = 0.31
    style["tracks"]["closed_foot"]["crossbar_outline_width_mm"] = 0.17
    style["tracks"]["dotted"]["route_dot_mm"] = 0.61
    style["tracks"]["dotted"]["connector_dot_mm"] = 0.29
    style["tracks"]["dotted"]["interval_mm"] = 1.2
    layer = _foot_layer()
    patch_tracks(layer, style)
    width = layer.find(".//Option[@name='outlineWidth']/Option[@name='expression']")
    assert "0.31" in width.get("value")
    symbols = {s.get("name"): s for s in layer.iter("symbol")}

    def option(name, key):
        return symbols[name].find(f"layer/Option/Option[@name='{key}']").get("value")

    assert option("@route", "size") == "0.61"
    assert option("@connector", "size") == "0.29"
    assert option("@closed", "outline_width") == "0.17"
    dots = layer.find(".//layer[@class='MarkerLine']/Option/Option[@name='interval']")
    assert dots.get("value") == "1.2"
    assert STYLE["tracks"]["closed_foot"]["open_width_mm"] == 0.2
    assert STYLE["tracks"]["closed_foot"]["crossbar_size_mm"] == 0.7
