from nzat.qgis.defaults import STYLE
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option

# Map5View paints these RGB triples. Apply replaces them with the owned hex.
STOCK_LINE_RGB = {
    (0, 158, 255): "stream",
    (148, 255, 59): "shelterbelt",
    (41, 160, 211): "grid",
}
COLOUR_OPTIONS = ("line_color", "color", "outline_color")


def _rgb_tuple(text):
    parsed = parse_qgis_colour(text)
    if parsed is None:
        return None
    return tuple(int(round(channel)) for channel in parsed[:3])


def patch_owned_lines(layer, style=None):
    """Replace stock process-blue, shelterbelt, and grid RGB with owned inks."""
    style = style or STYLE
    inks = style["reference_inks"]
    for symbol_layer in layer.findall(".//layer"):
        option = symbol_layer.find("Option")
        if option is None:
            continue
        for name in COLOUR_OPTIONS:
            child = option.find(f"Option[@name='{name}']")
            if child is None:
                continue
            ink_name = STOCK_LINE_RGB.get(_rgb_tuple(child.get("value") or ""))
            if ink_name is None:
                continue
            set_option(symbol_layer, name, rgba(inks[ink_name], 255))
