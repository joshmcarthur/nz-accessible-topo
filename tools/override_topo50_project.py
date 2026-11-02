#!/usr/bin/env python3
"""Apply the research-frame overrides to a Topo50 QGIS project.

The print layout (legend, sheet index, scale, title) is left alone.
Changes are on the map layers the research names:

- labels: upright NZAT Legible Test, size floor (R-05, R-06, R-09)
- labels: draw the buffer already on the text style, and darken ink below the contrast floor (R-07)
- labels: a multiline carto_text name is split onto the forward passes of a folded baseline
- contour: index vs intermediate ink and width (R-04)
- track_line map: closed tracks get a heavier line and cross-bars (R-11)
- water_point: hot and cold springs get different glyphs (R-17)
- vegetation map: native forest and scrub use a larger lightness step (R-10, R-17)

Usage: python3 tools/override_topo50_project.py IN.qgs OUT.qgs

Colour, type size, font family, and symbol rules come from
tools/style-topo50.json. This script does not paint reference_inks.
"""

import json
import math
import os
import sys
import uuid
import xml.etree.ElementTree as ET

import build_style as bs
import palette_audit as pa

STYLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style-topo50.json")
WHITE = (255, 255, 255)


def load_style(path=None):
    with open(path or STYLE_PATH, encoding="utf-8") as handle:
        return json.load(handle)


STYLE = load_style()
FAMILY = STYLE["fonts"]["raster_family"]
CARTO_TEXT_LAYER = "nztopo50_carto_text"
WRAP_TURN_DEG = 90
WRAP_HEADING_DEG = 45


def _hex_rgb(colour):
    text = colour.lstrip("#")
    return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))


def _rgb_call(colour):
    red, green, blue = _hex_rgb(colour)
    return f"color_rgb({red},{green},{blue})"


def _rgba(colour, alpha):
    red, green, blue = _hex_rgb(colour)
    return f"{red},{green},{blue},{alpha}"


def _style_expr(style=None):
    name = (style or STYLE)["fonts"]["raster_upright_style"]
    return (
        "CASE WHEN lower(coalesce(\"style\", '')) LIKE '%italic%'"
        " OR lower(coalesce(\"style\", '')) LIKE '%narrow%'"
        f" OR coalesce(\"style\", '') = '' THEN '{name}' ELSE \"style\" END"
    )


def upright_style_name(style, style_file=None):
    """Map a named font style onto the upright face we can ship."""
    fallback = (style_file or STYLE)["fonts"]["raster_upright_style"]
    text = (style or "").strip().lower()
    if not text or "italic" in text or "narrow" in text:
        return fallback
    return style


def size_floor(layer_name, size_text, style=None):
    """Return the label size in points after the R-09 floor.

    Spot-height layers may stay at 6 pt. Every other map label is at least 7 pt.
    """
    labels = (style or STYLE)["labels"]
    spot = labels["spot_height_layer_contains"]
    floor = (
        float(labels["spot_height_floor_pt"])
        if layer_name and spot in layer_name
        else float(labels["size_floor_pt"])
    )
    try:
        size = float(size_text)
    except (TypeError, ValueError):
        return size_text
    if size < floor:
        return str(int(floor))
    return size_text


def _properties_map(dd_parent):
    option = dd_parent.find("Option")
    if option is None:
        return None
    props = None
    for child in list(option):
        if child.get("name") == "properties":
            props = child
            break
    if props is not None and props.get("type") == "Map":
        return props
    new = ET.Element("Option", {"name": "properties", "type": "Map"})
    if props is not None:
        index = list(option).index(props)
        option.remove(props)
        option.insert(index, new)
    else:
        option.insert(0, new)
    return new


def put_expr(props, name, expression):
    for child in list(props):
        if child.get("name") == name:
            props.remove(child)
    node = ET.Element("Option", {"name": name, "type": "Map"})
    ET.SubElement(node, "Option", {"name": "active", "type": "bool", "value": "true"})
    ET.SubElement(node, "Option", {"name": "expression", "type": "QString", "value": expression})
    ET.SubElement(node, "Option", {"name": "type", "type": "int", "value": "3"})
    props.append(node)


def _expr(props, name):
    node = props.find(f"Option[@name='{name}']")
    if node is None:
        return None
    expr = node.find("Option[@name='expression']")
    return None if expr is None else expr.get("value")


def _set_option(layer_el, name, value):
    option = layer_el.find("Option")
    for child in option:
        if child.get("name") == name:
            child.set("value", value)
            return
    raise RuntimeError(f"missing option {name}")


def _category_symbol(layer, value):
    renderer = layer.find("renderer-v2")
    symbol_name = None
    for category in renderer.findall("categories/category"):
        if category.get("value") == value:
            symbol_name = category.get("symbol")
            break
    if symbol_name is None:
        raise RuntimeError(f"no category {value!r} on {layer.findtext('layername')}")
    for symbol in renderer.findall("symbols/symbol"):
        if symbol.get("name") == symbol_name:
            return symbol
    raise RuntimeError(f"no symbol {symbol_name}")


def _require_field(layer, field_name):
    names = [field.get("name") for field in layer.findall("fieldConfiguration/field")]
    if field_name not in names:
        raise RuntimeError(f"{layer.findtext('layername')} has no field {field_name}")


def parse_qgis_colour(text):
    """Return (r, g, b, a) with alpha 0–255. Return None when text is not a colour."""
    if not text:
        return None
    parts = text.split(",")
    if len(parts) < 3:
        return None
    try:
        red, green, blue = (int(float(parts[0])), int(float(parts[1])), int(float(parts[2])))
        alpha = int(float(parts[3])) if len(parts) >= 4 else 255
    except ValueError:
        return None
    return (red, green, blue, alpha)


def format_qgis_colour(rgb, alpha=255):
    red, green, blue = (int(round(channel)) for channel in rgb[:3])
    return f"{red},{green},{blue},{int(alpha)}"


def _rgb_key(rgb):
    return tuple(int(round(channel)) for channel in rgb[:3])


def project_palette(root):
    """Return (name, colour text) pairs from the project palette."""
    for props in root.iter("properties"):
        if props.get("name") != "Palette":
            continue
        labels = colors = None
        for child in props:
            if child.get("name") == "Labels":
                labels = [value.text or "" for value in child.findall("value")]
            elif child.get("name") == "Colors":
                colors = [value.text or "" for value in child.findall("value")]
        if labels and colors and len(labels) == len(colors):
            return list(zip(labels, colors))
    return []


def _is_named_project_colour(expression):
    if not expression:
        return False
    compact = "".join(expression.split())
    return compact in ('project_color_object("colour")', "project_color_object('colour')")


def _settings_props(settings):
    dd = settings.find("dd_properties")
    if dd is None:
        return None
    option = dd.find("Option")
    if option is None:
        return None
    props = option.find("Option[@name='properties']")
    if props is None or props.get("type") != "Map":
        return None
    return props


def draw_configured_buffer(buffer_el):
    """Draw the buffer the text style already has. Keep its size and its colour."""
    if buffer_el is None:
        return
    buffer_el.set("bufferDraw", "1")
    buffer_el.set("bufferOpacity", "1")
    parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
    if parsed is None:
        return
    red, green, blue, _alpha = parsed
    buffer_el.set("bufferColor", format_qgis_colour((red, green, blue), 255))


def label_behind(buffer_el):
    """Return the colour behind the ink. A drawn buffer is that colour. Else paper."""
    if buffer_el is None or buffer_el.get("bufferDraw") != "1":
        return WHITE
    parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
    if parsed is None:
        return WHITE
    red, green, blue, alpha = parsed
    return pa.composite((red, green, blue, alpha / 255.0), WHITE)


def colour_expression(palette, behind, min_ratio):
    """Map a named project colour that fails the floor to a darker ink."""
    clauses = []
    for name, colour_text in palette:
        if not name:
            continue
        parsed = parse_qgis_colour(colour_text)
        if parsed is None:
            continue
        red, green, blue, alpha = parsed
        fg = pa.composite((red, green, blue, alpha / 255.0), behind)
        new = bs.darken_for_text(fg, behind, min_ratio)
        if _rgb_key(new) == _rgb_key(fg):
            continue
        nr, ng, nb = _rgb_key(new)
        clauses.append(f"WHEN \"colour\" = '{name}' THEN color_rgb({nr},{ng},{nb})")
    if not clauses:
        return None
    return "CASE " + " ".join(clauses) + " ELSE project_color_object(\"colour\") END"


def _darken_text_color(text_style, behind, min_ratio):
    parsed = parse_qgis_colour(text_style.get("textColor"))
    if parsed is None:
        return
    red, green, blue, alpha = parsed
    fg = pa.composite((red, green, blue, alpha / 255.0), behind)
    new = bs.darken_for_text(fg, behind, min_ratio)
    if _rgb_key(new) == _rgb_key(fg):
        return
    text_style.set("textColor", format_qgis_colour(new, 255))


def patch_label_contrast(layer, style=None, palette=None):
    """Draw each configured label buffer. Darken ink that misses the contrast floor."""
    style = style or STYLE
    min_ratio = style["label_contrast"]["min_ratio"]
    named = palette or []
    for settings in layer.findall(".//settings"):
        text_style = settings.find("text-style")
        if text_style is None:
            continue
        buffer_el = text_style.find("text-buffer")
        draw_configured_buffer(buffer_el)
        behind = label_behind(buffer_el)
        props = _settings_props(settings)
        expression = _expr(props, "Color") if props is not None else None
        if _is_named_project_colour(expression):
            updated = colour_expression(named, behind, min_ratio)
            if updated:
                put_expr(props, "Color", updated)
            continue
        _darken_text_color(text_style, behind, min_ratio)


def _heading(start, end):
    return math.degrees(math.atan2(end[0] - start[0], end[1] - start[1]))


def _heading_delta(left, right):
    delta = abs(left - right) % 360
    return min(delta, 360 - delta)


def _turn_deg(before, corner, after):
    ax = corner[0] - before[0]
    ay = corner[1] - before[1]
    bx = after[0] - corner[0]
    by = after[1] - corner[1]
    if math.hypot(ax, ay) < 1 or math.hypot(bx, by) < 1:
        return 0.0
    return abs(math.degrees(math.atan2(ax * by - ay * bx, ax * bx + ay * by)))


def split_wrap_baseline(points, line_count):
    """Return one polyline per text line for a folded multiline baseline.

    A turn sharper than 90 degrees starts a new pass. Passes within 45
    degrees of the first pass are the forward baselines. When there are
    at least line_count of those, the first line_count are returned.
    Otherwise every pass is returned. A one-line label is not split.
    """
    if line_count <= 1 or len(points) < 3:
        return [list(points)]
    cuts = [0]
    for index in range(1, len(points) - 1):
        if _turn_deg(points[index - 1], points[index], points[index + 1]) > WRAP_TURN_DEG:
            cuts.append(index)
    cuts.append(len(points) - 1)
    parts = [points[cuts[index] : cuts[index + 1] + 1] for index in range(len(cuts) - 1)]
    parts = [part for part in parts if len(part) >= 2]
    if not parts:
        return [list(points)]
    heading = _heading(parts[0][0], parts[0][-1])
    forward = [
        part
        for part in parts
        if _heading_delta(_heading(part[0], part[-1]), heading) <= WRAP_HEADING_DEG
    ]
    if len(forward) >= line_count:
        return forward[:line_count]
    return parts


def wrap_baseline_expression():
    """Label geometry expression. The thresholds match split_wrap_baseline."""
    return (
        "CASE WHEN strpos(coalesce(\"text_string\", ''), '\\n') = 0 THEN @geometry ELSE "
        "with_variable('line', if(geometry_type(@geometry) = 'MultiLine', geometry_n(@geometry, 1), @geometry), "
        "with_variable('n', num_points(@line), "
        "if(@n < 3, @geometry, "
        "with_variable('cuts', array_append(array_prepend(array_filter("
        "generate_series(1, @n - 2), "
        "with_variable('a', azimuth(point_n(@line, @element), point_n(@line, @element + 1)), "
        "with_variable('b', azimuth(point_n(@line, @element + 1), point_n(@line, @element + 2)), "
        "degrees(abs(atan2(sin(@b - @a), cos(@b - @a)))) > 90))), 0), @n - 1), "
        "with_variable('parts', array_foreach(generate_series(0, array_length(@cuts) - 2), "
        "with_variable('cut', @element, make_line(array_foreach("
        "generate_series(array_get(@cuts, @cut), array_get(@cuts, @cut + 1)), "
        "point_n(@line, @element + 1))))), "
        "with_variable('heading', azimuth(start_point(array_get(@parts, 0)), end_point(array_get(@parts, 0))), "
        "with_variable('forward', array_filter(@parts, degrees(abs(atan2("
        "sin(azimuth(start_point(@element), end_point(@element)) - @heading), "
        "cos(azimuth(start_point(@element), end_point(@element)) - @heading)))) <= 45), "
        "with_variable('lines', array_length(string_to_array(\"text_string\", '\\n')), "
        "if(array_length(@forward) >= @lines, "
        "collect_geometries(array_slice(@forward, 0, @lines - 1)), "
        "collect_geometries(@parts))))))))))"
        " END"
    )


def patch_wrap_baseline(layer):
    """Put each line of a folded carto_text name on its own forward pass."""
    placement = layer.find("./labeling/settings/placement")
    if placement is None:
        return
    placement.set("geometryGenerator", wrap_baseline_expression())
    placement.set("geometryGeneratorEnabled", "1")
    placement.set("geometryGeneratorType", "LineGeometry")


def patch_labels(layer, layer_name, style=None, palette=None):
    style = style or STYLE
    family = style["fonts"]["raster_family"]
    labels = style["labels"]
    spot = labels["spot_height_layer_contains"]
    floor = int(
        labels["spot_height_floor_pt"] if layer_name and spot in layer_name else labels["size_floor_pt"]
    )
    count = 0
    for text_style in layer.findall(".//text-style"):
        text_style.set("namedStyle", upright_style_name(text_style.get("namedStyle"), style))
        text_style.set("fontItalic", "0")
        text_style.set("fontFamily", family)
        if text_style.get("fontSize") is not None:
            text_style.set("fontSize", size_floor(layer_name, text_style.get("fontSize"), style))
        count += 1
    size_expr = f'max({floor}, coalesce("size", {floor}))'
    for dd in layer.findall(".//dd_properties"):
        option = dd.find("Option")
        if option is None:
            continue
        props = option.find("Option[@name='properties']")
        if props is None or props.get("type") != "Map":
            continue
        present = {child.get("name") for child in props}
        if "Family" in present:
            put_expr(props, "Family", f"'{family}'")
        if "FontStyle" in present:
            put_expr(props, "FontStyle", _style_expr(style))
        if "Size" in present:
            put_expr(props, "Size", size_expr)
        # charplace stays. StretchWordSpacingToFit is the official along-line placement.
        # Mode 0 draws "Heathcote" upside down. The black question marks were missing SVGs.
    if layer_name == CARTO_TEXT_LAYER:
        patch_wrap_baseline(layer)
    patch_label_contrast(layer, style, palette)
    return count


def patch_contour(layer, style=None):
    style = style or STYLE
    index = style["contours"]["index"]
    intermediate = style["contours"]["intermediate"]
    _require_field(layer, "elevation")
    symbol = layer.find("renderer-v2/symbols/symbol")
    line = symbol.find("layer[@class='SimpleLine']")
    props = _properties_map(line.find("data_defined_properties"))
    # definition is null on the national contour table, so indefinite
    # contours cannot be dashed from that field.
    put_expr(
        props,
        "outlineColor",
        "CASE WHEN \"elevation\" IS NOT NULL AND round(\"elevation\") % 100 = 0"
        f" THEN {_rgb_call(index['colour'])}"
        f" ELSE {_rgb_call(intermediate['colour'])} END",
    )
    put_expr(
        props,
        "outlineWidth",
        'CASE WHEN "elevation" IS NOT NULL AND round("elevation") % 100 = 0'
        f" THEN {index['width_mm']} ELSE {intermediate['width_mm']} END",
    )


def _closed_crossbar(style=None):
    style = style or STYLE
    track = style["tracks"]["closed_foot"]
    ink = _rgba(track["crossbar_colour"], 255)
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
    for name, value, kind in (
        ("interval", str(track["crossbar_interval_mm"]), "QString"),
        ("interval_unit", "MM", "QString"),
        ("offset", "0", "QString"),
        ("offset_along_line", "0", "QString"),
        ("offset_along_line_unit", "MM", "QString"),
        ("offset_unit", "MM", "QString"),
        ("place_on_every_part", "true", "bool"),
        ("placements", "Interval", "QString"),
        ("rotate", "1", "QString"),
        ("ring_filter", "0", "QString"),
    ):
        ET.SubElement(options, "Option", {"name": name, "type": kind, "value": value})
    dd = ET.SubElement(layer, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    props = ET.SubElement(root, "Option", {"name": "properties", "type": "Map"})
    ET.SubElement(root, "Option", {"name": "type", "type": "QString", "value": "collection"})
    put_expr(props, "enabled", "\"status\" = 'closed'")
    symbol = ET.SubElement(
        layer,
        "symbol",
        {
            "alpha": "1",
            "clip_to_extent": "1",
            "force_rhr": "0",
            "frame_rate": "10",
            "is_animated": "0",
            "name": "@closed",
            "type": "marker",
        },
    )
    symbol_dd = ET.SubElement(symbol, "data_defined_properties")
    symbol_opt = ET.SubElement(symbol_dd, "Option", {"type": "Map"})
    ET.SubElement(symbol_opt, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(symbol_opt, "Option", {"name": "properties"})
    ET.SubElement(symbol_opt, "Option", {"name": "type", "type": "QString", "value": "collection"})
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
    for name, value in (
        ("angle", str(track["crossbar_angle_deg"])),
        ("cap_style", "square"),
        ("color", ink),
        ("horizontal_anchor_point", "1"),
        ("joinstyle", "bevel"),
        ("name", "line"),
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
    ):
        ET.SubElement(marker_opt, "Option", {"name": name, "type": "QString", "value": value})
    marker_dd = ET.SubElement(marker, "data_defined_properties")
    marker_root = ET.SubElement(marker_dd, "Option", {"type": "Map"})
    ET.SubElement(marker_root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(marker_root, "Option", {"name": "properties"})
    ET.SubElement(marker_root, "Option", {"name": "type", "type": "QString", "value": "collection"})
    return layer


def patch_tracks(layer, style=None):
    style = style or STYLE
    track = style["tracks"]["closed_foot"]
    _require_field(layer, "status")
    symbol = _category_symbol(layer, "foot")
    line = None
    for candidate in symbol.findall("layer[@class='SimpleLine']"):
        option = candidate.find("Option")
        use_dash = option.find("Option[@name='use_custom_dash']")
        if use_dash is not None and use_dash.get("value") == "1":
            line = candidate
            break
    if line is None:
        raise RuntimeError("foot track has no dashed line")
    props = _properties_map(line.find("data_defined_properties"))
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
    already = False
    for marker in symbol.findall("layer[@class='MarkerLine']"):
        dd = marker.find("data_defined_properties")
        if dd is None:
            continue
        props = dd.find("Option/Option[@name='properties']")
        if props is not None and _expr(props, "enabled") and "closed" in _expr(props, "enabled"):
            already = True
    if not already:
        symbol.append(_closed_crossbar(style))


def _scrub_hatch(style=None):
    """Diagonal lines. Scattered scrub already uses a dot pattern."""
    style = style or STYLE
    hatch = style["vegetation"]["scrub_hatch"]
    ink = _rgba(hatch["colour"], 255)
    layer = ET.Element(
        "layer",
        {
            "class": "LinePatternFill",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    options = ET.SubElement(layer, "Option", {"type": "Map"})
    for name, value, kind in (
        ("angle", str(hatch["angle_deg"]), "QString"),
        ("clip_mode", "during_render", "QString"),
        ("color", ink, "QString"),
        ("coordinate_reference", "feature", "QString"),
        ("distance", str(hatch["distance_mm"]), "QString"),
        ("distance_unit", "MM", "QString"),
        ("line_width", str(hatch["line_width_mm"]), "QString"),
        ("line_width_unit", "MM", "QString"),
        ("offset", "0", "QString"),
        ("offset_unit", "MM", "QString"),
    ):
        ET.SubElement(options, "Option", {"name": name, "type": kind, "value": value})
    dd = ET.SubElement(layer, "data_defined_properties")
    root = ET.SubElement(dd, "Option", {"type": "Map"})
    ET.SubElement(root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(root, "Option", {"name": "properties"})
    ET.SubElement(root, "Option", {"name": "type", "type": "QString", "value": "collection"})
    symbol = ET.SubElement(
        layer,
        "symbol",
        {
            "alpha": "1",
            "clip_to_extent": "1",
            "force_rhr": "0",
            "frame_rate": "10",
            "is_animated": "0",
            "name": "@scrub",
            "type": "line",
        },
    )
    symbol_dd = ET.SubElement(symbol, "data_defined_properties")
    symbol_opt = ET.SubElement(symbol_dd, "Option", {"type": "Map"})
    ET.SubElement(symbol_opt, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(symbol_opt, "Option", {"name": "properties"})
    ET.SubElement(symbol_opt, "Option", {"name": "type", "type": "QString", "value": "collection"})
    line = ET.SubElement(
        symbol,
        "layer",
        {
            "class": "SimpleLine",
            "enabled": "1",
            "id": "{" + str(uuid.uuid4()) + "}",
            "locked": "0",
            "pass": "0",
        },
    )
    line_opt = ET.SubElement(line, "Option", {"type": "Map"})
    for name, value in (
        ("capstyle", "square"),
        ("joinstyle", "bevel"),
        ("line_color", ink),
        ("line_style", "solid"),
        ("line_width", str(hatch["line_width_mm"])),
        ("line_width_unit", "MM"),
        ("offset", "0"),
        ("offset_unit", "MM"),
        ("use_custom_dash", "0"),
    ):
        ET.SubElement(line_opt, "Option", {"name": name, "type": "QString", "value": value})
    line_dd = ET.SubElement(line, "data_defined_properties")
    line_root = ET.SubElement(line_dd, "Option", {"type": "Map"})
    ET.SubElement(line_root, "Option", {"name": "name", "type": "QString", "value": ""})
    ET.SubElement(line_root, "Option", {"name": "properties"})
    ET.SubElement(line_root, "Option", {"name": "type", "type": "QString", "value": "collection"})
    return layer


def patch_vegetation(layer, style=None):
    style = style or STYLE
    native_ink = style["vegetation"]["native"]
    scrub_ink = style["vegetation"]["scrub"]
    native = _category_symbol(layer, "native")
    scrub = _category_symbol(layer, "scrub")
    native_fill = native.find("layer[@class='SimpleFill']")
    scrub_fill = scrub.find("layer[@class='SimpleFill']")
    _set_option(native_fill, "color", _rgba(native_ink["colour"], native_ink["alpha"]))
    _set_option(scrub_fill, "color", _rgba(scrub_ink["colour"], scrub_ink["alpha"]))
    # Colour alone does not separate these fills in greyscale (R-10).
    # Scattered scrub keeps its dot pattern. Scrub gets a line hatch.
    if scrub.find("layer[@class='LinePatternFill']") is None:
        scrub.insert(0, _scrub_hatch(style))


def patch_springs(layer, style=None):
    style = style or STYLE
    hot = style["springs"]["hot"]
    cold = style["springs"]["cold"]
    _require_field(layer, "type")
    _require_field(layer, "temperature_indicator")
    renderer = layer.find("renderer-v2")
    if renderer.get("attr") == "feature_type":
        renderer.set("attr", "type")
    symbol = _category_symbol(layer, "spring")
    marker = symbol.find("layer[@class='SimpleMarker']")
    props = _properties_map(marker.find("data_defined_properties"))
    put_expr(
        props,
        "name",
        f"if(\"temperature_indicator\" = 'hot', '{hot['glyph']}', '{cold['glyph']}')",
    )
    put_expr(
        props,
        "fillColor",
        "if(\"temperature_indicator\" = 'hot',"
        f" {_rgb_call(hot['colour'])},"
        f" {_rgb_call(cold['colour'])})",
    )


def apply(root):
    """Patch map layers. Return a count of label styles touched."""
    layers = root.find("projectlayers")
    if layers is None:
        raise RuntimeError("project has no projectlayers")
    labels = 0
    seen = set()
    palette = project_palette(root)
    for layer in layers.findall("maplayer"):
        name = layer.findtext("layername") or ""
        labels += patch_labels(layer, name, palette=palette)
        if name == "contour":
            patch_contour(layer)
            seen.add(name)
        elif name == "track_line map":
            patch_tracks(layer)
            seen.add(name)
        elif name == "vegetation map":
            patch_vegetation(layer)
            seen.add(name)
        elif name == "water_point":
            patch_springs(layer)
            seen.add(name)
    missing = {"contour", "track_line map", "vegetation map", "water_point"} - seen
    if missing:
        raise RuntimeError(f"missing layers: {', '.join(sorted(missing))}")
    return labels


def main(src, dst):
    doctype = ""
    with open(src, encoding="utf-8") as handle:
        first = handle.readline()
        if first.startswith("<!DOCTYPE"):
            doctype = first if first.endswith("\n") else first + "\n"
    root = ET.parse(src).getroot()
    labels = apply(root)
    body = ET.tostring(root, encoding="unicode")
    with open(dst, "w", encoding="utf-8") as handle:
        handle.write(doctype)
        handle.write(body)
    print(f"labels {labels}")
    print(f"wrote {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: override_topo50_project.py IN.qgs OUT.qgs", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
