from nzat.colour.composite import composite
from nzat.qgis.defaults import WHITE
from nzat.qgis.parse_qgis_colour import parse_qgis_colour


def label_behind(buffer_el):
    """Return the colour behind the ink. A drawn buffer is that colour. Else paper."""
    if buffer_el is None or buffer_el.get("bufferDraw") != "1":
        return WHITE
    parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
    if parsed is None:
        return WHITE
    red, green, blue, alpha = parsed
    return composite((red, green, blue, alpha / 255.0), WHITE)
