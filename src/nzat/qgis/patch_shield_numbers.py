import copy
import uuid

from nzat.colour.darken import darken_for_text
from nzat.qgis.defaults import STYLE
from nzat.qgis.format_qgis_colour import format_qgis_colour
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.patch_contour_numbers import _lift_size, _put, _rule_symbol
from nzat.qgis.rgba import _hex_rgb

SYMBOL_LAYER = "nztopo50_carto_symbol"
NUMBER_LAYER = "nztopo50_carto_symbol_label"
SHIELD_RULE = "highway_shield"


def _layer(root, name):
    for layer in root.findall("projectlayers/maplayer"):
        if (layer.findtext("layername") or "") == name:
            return layer
    return None


def patch_shield_numbers(root, style=None):
    """Draw state highway numbers inside a white shield, above the road.

    The stock number layer reads a parquet in a LINZ staff Downloads folder,
    so no number draws (log 0090). It reads the symbol layer's source here.
    The shield draws below the roads in stock, so the number sat on the red
    highway line. A copy of the shield now draws under each number.
    """
    style = style or STYLE
    symbols = _layer(root, SYMBOL_LAYER)
    numbers = _layer(root, NUMBER_LAYER)
    if symbols is None or numbers is None:
        return
    numbers.find("datasource").text = symbols.findtext("datasource")
    number_symbol = _rule_symbol(numbers, SHIELD_RULE)
    marker = number_symbol.find("layer[@class='FontMarker']")
    if marker is None:
        raise RuntimeError(f"{NUMBER_LAYER} has no FontMarker")
    _put(marker, "font", style["fonts"]["raster_family"])
    _put(marker, "font_style", style["fonts"]["raster_upright_style"])
    _lift_size(marker)
    shield = _rule_symbol(symbols, SHIELD_RULE).find("layer[@class='SvgMarker']")
    if shield is None:
        raise RuntimeError(f"{SYMBOL_LAYER} has no {SHIELD_RULE} SvgMarker")
    fill = parse_qgis_colour(shield.find("Option/Option[@name='color']").get("value"))
    contrast = style["label_contrast"]
    ink = darken_for_text(
        _hex_rgb(style["reference_inks"]["project_highway"]),
        fill[:3],
        contrast["min_ratio"],
        contrast["red_light_min"],
    )
    _put(marker, "color", format_qgis_colour(ink, 255))
    for old in number_symbol.findall("layer[@nzat='shield']"):
        number_symbol.remove(old)
    body = copy.deepcopy(shield)
    body.set("nzat", "shield")
    if body.get("id"):
        body.set("id", "{" + str(uuid.uuid4()) + "}")
    number_symbol.insert(list(number_symbol).index(marker), body)
