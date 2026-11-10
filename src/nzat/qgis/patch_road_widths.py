from nzat.qgis.defaults import PMS151_RGB, STYLE
from nzat.qgis.expr import expr
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option
from nzat.style.navigation_line_mm import navigation_line_mm

WHITE_RGB = (255, 255, 255)


def _rgb_tuple(text):
    parsed = parse_qgis_colour(text)
    if parsed is None:
        return None
    return tuple(int(round(channel)) for channel in parsed[:3])


def _road_fill_rgbs(style):
    road = _rgb_tuple(rgba(style["reference_inks"]["project_road"], 255))
    return {PMS151_RGB, road}


def _line_width_mm(line):
    option = line.find("Option/Option[@name='line_width']")
    if option is None or not option.get("value"):
        return None
    return float(option.get("value"))


def _bump_static_width(line, floor):
    width = _line_width_mm(line)
    if width is None or width >= floor:
        return
    set_option(line, "line_width", str(floor))


def _bump_expression_width(line, floor):
    dd = line.find("data_defined_properties")
    if dd is None:
        return
    props = properties_map(dd)
    if props is None:
        return
    current = expr(props, "outlineWidth")
    if not current:
        return
    # Stock keeps the lane_count width off and draws the static width. An
    # active copy made the fill as wide as its casing (log 0111).
    active = props.find("Option[@name='outlineWidth']/Option[@name='active']")
    if active is None or active.get("value") != "true":
        return
    prefix = f"max({floor}, "
    if current.startswith(prefix):
        return
    put_expr(props, "outlineWidth", f"max({floor}, {current})")


def patch_road_widths(layer, style=None):
    """Raise painted road fills and unmetalled centre lines to the navigation floor."""
    style = style or STYLE
    floor = navigation_line_mm(style)
    fills = _road_fill_rgbs(style)
    for line in layer.findall(".//layer[@class='SimpleLine']"):
        option = line.find("Option/Option[@name='line_color']")
        if option is None:
            continue
        rgb = _rgb_tuple(option.get("value") or "")
        if rgb in fills or (rgb == WHITE_RGB and (_line_width_mm(line) or 0) < floor):
            _bump_expression_width(line, floor)
            _bump_static_width(line, floor)


def patch_one_lane_casing(layer, style=None):
    """Widen the one-lane casing so the raised fill keeps the stock dark edge."""
    style = style or STYLE
    floor = float(style["sizes"]["one_lane_road_casing_mm"])
    for line in layer.findall(".//layer[@class='SimpleLine']"):
        _bump_static_width(line, floor)
