import uuid
import xml.etree.ElementTree as ET

from nzat.qgis.category_symbol import category_symbol
from nzat.qgis.closed_bar_placement import _mm, closed_bar_placement
from nzat.qgis.defaults import STYLE
from nzat.qgis.expr import expr
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr
from nzat.qgis.require_field import require_field
from nzat.qgis.rgba import rgba
from nzat.qgis.set_option import set_option

# QGIS reads a NULL "enabled" value as on, so a bare "status" = 'closed'
# drew the cross on every open foot track (status is NULL there, log 0092).
CLOSED_ENABLED = "coalesce(\"status\", '') = 'closed'"
# Poled routes and track connectors draw as dots (LINZ printed legend), so
# the dashed line steps aside for them. coalesce() keeps NULL out of "on".
DOTTED = {
    "route": "coalesce(\"track_type\", '') = 'route'",
    "connector": "coalesce(\"track_type\", '') = 'connector'",
}
DASHED_ENABLED = "coalesce(\"track_type\", '') NOT IN ('route', 'connector')"


def _closed_crossbar(style=None):
    style = style or STYLE
    track = style["tracks"]["closed_foot"]
    ink = rgba(track["crossbar_colour"], 255)
    interval, along = closed_bar_placement(track)
    return _marker_line(
        "@closed",
        CLOSED_ENABLED,
        interval,
        along,
        (
            ("angle", str(track["crossbar_angle_deg"])),
            ("cap_style", "square"),
            ("color", ink),
            ("horizontal_anchor_point", "1"),
            ("joinstyle", "bevel"),
            ("name", track["marker"]),
            ("offset", "0,0"),
            ("offset_unit", "MM"),
            ("outline_color", ink),
            ("outline_style", "solid"),
            ("outline_width", str(track["crossbar_outline_width_mm"])),
            ("outline_width_unit", "MM"),
            ("scale_method", "diameter"),
            ("size", str(track["crossbar_size_mm"])),
            ("size_unit", "MM"),
            ("vertical_anchor_point", "1"),
        ),
    )


def _dot_options(style, kind):
    dotted = style["tracks"]["dotted"]
    ink = rgba(dotted["colour"], 255)
    return (
        ("angle", "0"),
        ("color", ink),
        ("horizontal_anchor_point", "1"),
        ("name", "circle"),
        ("offset", "0,0"),
        ("offset_unit", "MM"),
        ("outline_color", ink),
        ("outline_style", "no"),
        ("outline_width", "0"),
        ("outline_width_unit", "MM"),
        ("scale_method", "diameter"),
        ("size", str(dotted[f"{kind}_dot_mm"])),
        ("size_unit", "MM"),
        ("vertical_anchor_point", "1"),
    )


def _dot_placement(style):
    """Return the dot interval and an offset that centres each closed × between two dots."""
    interval = float(style["tracks"]["dotted"]["interval_mm"])
    _, along = closed_bar_placement(style["tracks"]["closed_foot"])
    return _mm(interval), _mm((float(along) + interval / 2) % interval)


def _marker_line(name, enabled, interval, along, marker_options):
    layer = ET.Element(
        "layer",
        {
            "class": "MarkerLine",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    for option_name, value, kind in (
        ("interval", interval, "QString"),
        ("interval_unit", "MM", "QString"),
        ("offset", "0", "QString"),
        ("offset_along_line", along, "QString"),
        ("offset_along_line_unit", "MM", "QString"),
        ("offset_unit", "MM", "QString"),
        ("place_on_every_part", "true", "bool"),
        ("placements", "Interval", "QString"),
        ("rotate", "1", "QString"),
        ("ring_filter", "0", "QString"),
    ):
        ET.SubElement(
            options, "Option", {"name": option_name, "type": kind, "value": value}
        )
    dd = ET.SubElement(layer, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    props = ET.SubElement(root, "Option", {"name": "properties", "type": "Map"})
    ET.SubElement(
        root, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )
    put_expr(props, "enabled", enabled)
    symbol = ET.SubElement(
        layer,
        "symbol",
        {
            "alpha": "1",
            "clip_to_extent": "1",
            "force_rhr": "0",
            "frame_rate": "10",
            "is_animated": "0",
            "name": name,
            "type": "marker",
        },
    )
    symbol_dd = ET.SubElement(symbol, "data_defined_properties")
    symbol_opt = ET.SubElement(symbol_dd, "Option", {"type": "Map"})
    ET.SubElement(
        symbol_opt, "Option", {"name": "name", "type": "QString", "value": ""}
    )
    ET.SubElement(symbol_opt, "Option", {"name": "properties"})
    ET.SubElement(
        symbol_opt, "Option", {"name": "type", "type": "QString", "value": "collection"}
    )
    marker = ET.SubElement(
        symbol,
        "layer",
        {
            "class": "SimpleMarker",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    marker_opt = ET.SubElement(marker, "Option", {"type": "Map"})
    for option_name, value in marker_options:
        ET.SubElement(
            marker_opt,
            "Option",
            {"name": option_name, "type": "QString", "value": value},
        )
    marker_dd = ET.SubElement(marker, "data_defined_properties")
    marker_root = ET.SubElement(marker_dd, "Option", {"type": "Map"})
    ET.SubElement(
        marker_root, "Option", {"name": "name", "type": "QString", "value": ""}
    )
    ET.SubElement(marker_root, "Option", {"name": "properties"})
    ET.SubElement(
        marker_root,
        "Option",
        {"name": "type", "type": "QString", "value": "collection"},
    )
    return layer


def _marker_with(symbol, needle):
    for marker in symbol.findall("layer[@class='MarkerLine']"):
        dd = marker.find("data_defined_properties")
        if dd is None:
            continue
        props = dd.find("Option/Option[@name='properties']")
        if (
            props is not None
            and expr(props, "enabled")
            and needle in expr(props, "enabled")
        ):
            return marker
    return None


def _sync_closed_crossbar(marker, style):
    track = style["tracks"]["closed_foot"]
    ink = rgba(track["crossbar_colour"], 255)
    interval, along = closed_bar_placement(track)
    props = marker.find("data_defined_properties/Option/Option[@name='properties']")
    put_expr(props, "enabled", CLOSED_ENABLED)
    set_option(marker, "interval", interval)
    set_option(marker, "offset_along_line", along)
    simple = marker.find("symbol/layer[@class='SimpleMarker']")
    if simple is None:
        raise RuntimeError("closed cross-bar has no marker")
    for name, value in (
        ("angle", str(track["crossbar_angle_deg"])),
        ("color", ink),
        ("name", track["marker"]),
        ("outline_color", ink),
        ("outline_width", str(track["crossbar_outline_width_mm"])),
        ("size", str(track["crossbar_size_mm"])),
    ):
        set_option(simple, name, value)


def patch_tracks(layer, style=None):
    style = style or STYLE
    if style["tracks"]["access"]["painted"]:
        raise RuntimeError("track access is reserved and must not be painted")
    track = style["tracks"]["closed_foot"]
    require_field(layer, "status")
    require_field(layer, "track_type")
    symbol = category_symbol(layer, "foot")
    line = None
    for candidate in symbol.findall("layer[@class='SimpleLine']"):
        option = candidate.find("Option")
        use_dash = option.find("Option[@name='use_custom_dash']")
        if use_dash is not None and use_dash.get("value") == "1":
            line = candidate
            break
    if line is None:
        raise RuntimeError("foot track has no dashed line")
    props = properties_map(line.find("data_defined_properties"))
    put_expr(
        props,
        "outlineWidth",
        f"if(\"status\" = 'closed', {track['width_mm']}, {track['open_width_mm']})",
    )
    put_expr(
        props,
        "customDash",
        f"if(\"status\" = 'closed', '{track['closed_dash']}', '{track['open_dash']}')",
    )
    put_expr(props, "enabled", DASHED_ENABLED)
    interval, along = _dot_placement(style)
    for kind, enabled in DOTTED.items():
        existing = _marker_with(symbol, f"'{kind}'")
        if existing is not None:
            symbol.remove(existing)
        symbol.append(
            _marker_line(
                f"@{kind}", enabled, interval, along, _dot_options(style, kind)
            )
        )
    # The × goes last so it draws over the dots of a closed poled route.
    existing = _marker_with(symbol, "'closed'")
    if existing is None:
        symbol.append(_closed_crossbar(style))
    else:
        symbol.remove(existing)
        symbol.append(existing)
        _sync_closed_crossbar(existing, style)
