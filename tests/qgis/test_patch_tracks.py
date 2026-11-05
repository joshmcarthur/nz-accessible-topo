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
    patch_tracks(track_layer)
    angle = track_layer.find(
        ".//layer[@class='SimpleMarker']/Option/Option[@name='angle']"
    )
    size = track_layer.find(
        ".//layer[@class='SimpleMarker']/Option/Option[@name='size']"
    )
    marker = track_layer.find(
        ".//layer[@class='SimpleMarker']/Option/Option[@name='name']"
    )
    assert angle.get("value") == str(
        STYLE["tracks"]["closed_foot"]["crossbar_angle_deg"]
    )
    assert size.get("value") == str(STYLE["tracks"]["closed_foot"]["crossbar_size_mm"])
    assert marker.get("value") == STYLE["tracks"]["closed_foot"]["marker"]
    assert marker.get("value") == "cross2"
    interval = track_layer.find(
        ".//layer[@class='MarkerLine']/Option/Option[@name='interval']"
    )
    along = track_layer.find(
        ".//layer[@class='MarkerLine']/Option/Option[@name='offset_along_line']"
    )
    assert interval.get("value") == str(
        STYLE["tracks"]["closed_foot"]["marker_interval_mm"]
    )
    assert interval.get("value") == "3"
    assert along.get("value") == "1.25"
    width = track_layer.find(
        ".//Option[@name='outlineWidth']/Option[@name='expression']"
    ).get("value")
    assert "0.15" in width
    assert "0.45" not in width
    again = json.loads(json.dumps(STYLE))
    again["tracks"]["closed_foot"]["crossbar_angle_deg"] = 45
    patch_tracks(track_layer, again)
    assert angle.get("value") == "45"
    # Catches the cross drawn on open foot tracks: QGIS reads NULL as enabled.
    enabled = track_layer.find(
        ".//layer[@class='MarkerLine']//Option[@name='enabled']/Option[@name='expression']"
    ).get("value")
    assert enabled == "coalesce(\"status\", '') = 'closed'"
