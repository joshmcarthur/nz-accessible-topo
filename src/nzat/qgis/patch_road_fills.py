from nzat.qgis.defaults import PMS151_RGB, STYLE
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option


def _rgb_tuple(text):
    parsed = parse_qgis_colour(text)
    if parsed is None:
        return None
    return tuple(int(round(channel)) for channel in parsed[:3])


def patch_road_fills(layer, style=None):
    """Replace painted PMS151 road fills with the owned road ink."""
    style = style or STYLE
    ink = rgba(style["reference_inks"]["project_road"], 255)
    for line in layer.findall(".//layer[@class='SimpleLine']"):
        option = line.find("Option/Option[@name='line_color']")
        if option is None:
            continue
        if _rgb_tuple(option.get("value") or "") != PMS151_RGB:
            continue
        set_option(line, "line_color", ink)
