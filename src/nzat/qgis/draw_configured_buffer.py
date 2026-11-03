from nzat.qgis.capped_buffer_mm import capped_buffer_mm
from nzat.qgis.format_buffer_mm import format_buffer_mm
from nzat.qgis.format_qgis_colour import format_qgis_colour
from nzat.qgis.parse_qgis_colour import parse_qgis_colour


def draw_configured_buffer(buffer_el, max_mm):
    """Draw the buffer the text style already has. Cap its size. Keep its colour."""
    if buffer_el is None:
        return
    buffer_el.set("bufferDraw", "1")
    buffer_el.set("bufferOpacity", "1")
    units = (buffer_el.get("bufferSizeUnits") or "MM").upper()
    if units == "MM":
        capped = capped_buffer_mm(buffer_el.get("bufferSize"), max_mm)
        if capped is not None:
            buffer_el.set("bufferSize", format_buffer_mm(capped))
    parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
    if parsed is None:
        return
    red, green, blue, _alpha = parsed
    buffer_el.set("bufferColor", format_qgis_colour((red, green, blue), 255))
