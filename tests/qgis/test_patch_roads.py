import xml.etree.ElementTree as ET

from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.red_light import red_light_reflectance
from nzat.colour.rel_luminance import rel_luminance
from nzat.qgis.is_owned_road_layer import is_owned_road_layer
from nzat.qgis.patch_contour_numbers import patch_contour_numbers
from nzat.qgis.patch_road_fills import patch_road_fills
from nzat.qgis.patch_shield_numbers import patch_shield_numbers


def test_road_fills_and_contour_numbers_read_the_style_file():
    # Catches a PMS151 road fill left unpainted, or a contour number left in road orange.
    assert is_owned_road_layer("road_line 2 lane map") is True
    assert is_owned_road_layer("road_line 1 lane sealed map") is True
    assert is_owned_road_layer("road_line 2 lane highway map") is False
    assert is_owned_road_layer("road_line 2 lane background map") is False
    road = ET.fromstring(
        """
        <maplayer>
          <layername>road_line 2 lane map</layername>
          <renderer-v2 type="singleSymbol"><symbols>
            <symbol name="0" type="line">
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="255,127,0,255"/>
                </Option>
              </layer>
              <layer class="SimpleLine">
                <Option type="Map">
                  <Option name="line_color" type="QString" value="35,35,35,255"/>
                </Option>
              </layer>
            </symbol>
          </symbols></renderer-v2>
        </maplayer>
        """
    )
    patch_road_fills(road)
    colours = [
        opt.get("value") for opt in road.findall(".//Option[@name='line_color']")
    ]
    assert colours[0].startswith("236,112,0")
    assert colours[1].startswith("35,35,35")
    carto = ET.fromstring(
        """
        <maplayer>
          <layername>nztopo50_carto_symbol</layername>
          <featureBlendMode>1</featureBlendMode>
          <renderer-v2 type="RuleRenderer">
            <rules>
              <rule filter="&quot;type&quot; = 'contour_number'" symbol="3"/>
            </rules>
            <symbols>
              <symbol name="3" type="marker">
                <layer class="FontMarker">
                  <Option type="Map">
                    <Option name="chr" type="QString" value="A"/>
                    <Option name="color" type="QString" value="255,127,0,255"/>
                    <Option name="font" type="QString" value="Nimbus Sans LINZ"/>
                    <Option name="font_style" type="QString" value="Narrow Italic"/>
                    <Option name="fontItalic" type="QString" value="1"/>
                    <Option name="size" type="QString" value="4"/>
                    <Option name="size_unit" type="QString" value="Point"/>
                  </Option>
                </layer>
              </symbol>
            </symbols>
          </renderer-v2>
        </maplayer>
        """
    )
    patch_contour_numbers(carto)
    patch_contour_numbers(carto)
    # Catches a DestinationOver layer, which hid each digit behind its halo (log 0082).
    assert carto.findtext("featureBlendMode") == "0"
    halo, digit = carto.findall(".//layer[@class='FontMarker']")
    # Catches the face left as Nimbus Narrow Italic: FontMarker reads font and font_style (log 0082).
    assert digit.find("Option/Option[@name='font']").get("value") == "Atkinson Hyperlegible Next Macron"
    assert digit.find("Option/Option[@name='font_style']").get("value") == "Regular"
    assert digit.find("Option/Option[@name='color']").get("value").startswith("122,85,66")
    assert digit.find("Option/Option[@name='fontItalic']").get("value") == "0"
    assert digit.get("fontItalic") == "0"
    assert float(digit.find("Option/Option[@name='size']").get("value")) >= 6
    # Catches a missing halo, a halo drawn over the digit, or a second halo on re-apply.
    assert halo.get("nzat") == "halo"
    assert halo.find("Option/Option[@name='color']").get("value").startswith("255,255,255")
    assert float(halo.find("Option/Option[@name='outline_width']").get("value")) > 0


SHIELD_PROJECT = """
<qgis><projectlayers>
  <maplayer>
    <layername>nztopo50_carto_symbol</layername>
    <datasource>./nztopo50_carto_symbol.parquet|layername=nztopo50_carto_symbol</datasource>
    <renderer-v2 type="RuleRenderer">
      <rules><rule filter="&quot;type&quot; = 'highway_shield'" symbol="0"/></rules>
      <symbols><symbol name="0" type="marker">
        <layer class="SvgMarker" id="{a}"><Option type="Map">
          <Option name="color" type="QString" value="255,255,255,255"/>
          <Option name="name" type="QString" value="./symbol/nztopo50_highway_shield.svg"/>
        </Option></layer>
      </symbol></symbols>
    </renderer-v2>
  </maplayer>
  <maplayer>
    <layername>nztopo50_carto_symbol_label</layername>
    <datasource>../../../../../Users/KBaker/Downloads/nztopo50_carto_symbol.parquet|layername=nztopo50_carto_symbol</datasource>
    <renderer-v2 type="RuleRenderer">
      <rules><rule filter=" &quot;type&quot;  =  'highway_shield' " symbol="0"/></rules>
      <symbols><symbol name="0" type="marker">
        <layer class="FontMarker"><Option type="Map">
          <Option name="color" type="QString" value="255,0,0,255"/>
          <Option name="font" type="QString" value="Nimbus Sans LINZ"/>
          <Option name="font_style" type="QString" value="Narrow"/>
          <Option name="size" type="QString" value="2.2"/>
          <Option name="size_unit" type="QString" value="MM"/>
        </Option></layer>
      </symbol></symbols>
    </renderer-v2>
  </maplayer>
</projectlayers></qgis>
"""


def test_highway_numbers_draw_in_a_shield_in_the_raster_face():
    # Catches the stock number layer left on a LINZ staff Downloads path (no
    # number draws), a number left in Nimbus or pure red, or a number with no
    # shield under it, so it sits on the red highway line (log 0090).
    root = ET.fromstring(SHIELD_PROJECT)
    patch_shield_numbers(root)
    patch_shield_numbers(root)
    symbols, numbers = root.findall("projectlayers/maplayer")
    assert numbers.findtext("datasource") == symbols.findtext("datasource")
    shield, digit = numbers.findall(".//symbol/layer")
    assert shield.get("class") == "SvgMarker" and shield.get("nzat") == "shield"
    assert shield.get("id") != "{a}"
    assert digit.find("Option/Option[@name='font']").get("value") == "Atkinson Hyperlegible Next Macron"
    assert digit.find("Option/Option[@name='font_style']").get("value") == "Regular"
    ink = tuple(int(v) for v in digit.find("Option/Option[@name='color']").get("value").split(",")[:3])
    white = (255, 255, 255)
    assert contrast_ratio(rel_luminance(ink), rel_luminance(white)) >= 4.8
    assert contrast_ratio(red_light_reflectance(ink), red_light_reflectance(white)) >= 3.0
