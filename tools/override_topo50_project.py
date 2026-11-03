#!/usr/bin/env python3
"""Apply the research-frame overrides to a Topo50 QGIS project.

The print layout (legend, sheet index, scale, title) is left alone.
Changes are on the map layers the research names:

- labels: upright NZAT Legible Test, size floor (R-05, R-06, R-09)
- labels: draw the buffer already on the text style, cap it at halo_max_mm, and darken ink below the contrast floor and the red-light floor (R-07, R-11)
- labels: a multiline carto_text name is split onto the forward passes of a folded baseline
- labels: stretch-to-fit curved modes keep the stock spread only on a one-line name whose baseline is longer than the name, so the larger type is not squeezed
- labels: flat one-line carto_text names sit on a short horizontal line around the stock label, so QGIS can slide or flip a name that collides
- labels: a flat carto_text name listed in carto_fit.json beside the project is drawn at its fitted point and line count
- contour: index vs intermediate ink, width, stroke alpha, plus an index-ink casing on intermediates (R-04, R-01)
- track_line map: closed tracks get a heavier line and cross-bars (R-11)
- track_line map: track access is a reserved unpainted casing_colour channel (R-12)
- water_point: hot and cold springs get different glyphs (R-17)
- vegetation map: native forest and scrub use a larger lightness step (R-10, R-17)
- vegetation map: draws below contour so the darker fills do not hide relief (R-04)
- road fills: PMS151 two-lane and sealed fills become reference_inks.project_road (R-01)
- nztopo50_carto_symbol: contour_number FontMarkers use the index contour ink (R-17 P7)
- hillshade: optional overlay at 337.5°. Turns on when dem.tif sits beside the project (R-03)

Usage: python3 tools/override_topo50_project.py IN.qgs OUT.qgs

Colour, type size, font family, and symbol rules come from
tools/style-topo50.json.
"""

import copy
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
DEM_LAYER_NAME = "dem"
DEM_LAYER_ID = "dem_hillshade"
CARTO_TEXT_LAYER = "nztopo50_carto_text"
WRAP_TURN_DEG = 90
WRAP_HEADING_DEG = 45
SHEET_SCALE = 50000


def _hex_rgb(colour):
    text = colour.lstrip("#")
    return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))


def _rgb_call(colour):
    red, green, blue = _hex_rgb(colour)
    return f"color_rgb({red},{green},{blue})"


def _alpha_byte(alpha):
    return int(round(float(alpha) * 255))


def _rgba_call(colour, alpha):
    red, green, blue = _hex_rgb(colour)
    return f"color_rgba({red},{green},{blue},{_alpha_byte(alpha)})"


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


PMS151_RGB = (255, 127, 0)


def _rgb_tuple(text):
    parsed = parse_qgis_colour(text)
    if parsed is None:
        return None
    return tuple(int(round(channel)) for channel in parsed[:3])


def _rule_symbol(layer, token):
    renderer = layer.find("renderer-v2")
    symbol_name = None
    for rule in renderer.iter("rule"):
        filt = rule.get("filter") or ""
        if token in filt:
            symbol_name = rule.get("symbol")
            break
    if symbol_name is None:
        raise RuntimeError(f"no rule {token!r} on {layer.findtext('layername')}")
    for symbol in renderer.findall("symbols/symbol"):
        if symbol.get("name") == symbol_name:
            return symbol
    raise RuntimeError(f"no symbol {symbol_name}")


def is_owned_road_layer(name):
    """Two-lane and sealed road fills. Skip highway and background casings."""
    lower = name.lower()
    if "road_line" not in lower:
        return False
    if "highway" in lower or "background" in lower:
        return False
    return True


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


def capped_buffer_mm(size_text, max_mm):
    """Return the buffer width in mm. Do not go above max_mm."""
    try:
        size = float(size_text)
    except (TypeError, ValueError):
        return None
    return min(size, float(max_mm))


def format_buffer_mm(size):
    return f"{size:g}"


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


def label_behind(buffer_el):
    """Return the colour behind the ink. A drawn buffer is that colour. Else paper."""
    if buffer_el is None or buffer_el.get("bufferDraw") != "1":
        return WHITE
    parsed = parse_qgis_colour(buffer_el.get("bufferColor"))
    if parsed is None:
        return WHITE
    red, green, blue, alpha = parsed
    return pa.composite((red, green, blue, alpha / 255.0), WHITE)


def colour_expression(palette, behind, min_ratio, red_min=None):
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
        new = bs.darken_for_text(fg, behind, min_ratio, red_min)
        if _rgb_key(new) == _rgb_key(fg):
            continue
        nr, ng, nb = _rgb_key(new)
        clauses.append(f"WHEN \"colour\" = '{name}' THEN color_rgb({nr},{ng},{nb})")
    if not clauses:
        return None
    return "CASE " + " ".join(clauses) + " ELSE project_color_object(\"colour\") END"


def _darken_text_color(text_style, behind, min_ratio, red_min=None):
    parsed = parse_qgis_colour(text_style.get("textColor"))
    if parsed is None:
        return
    red, green, blue, alpha = parsed
    fg = pa.composite((red, green, blue, alpha / 255.0), behind)
    new = bs.darken_for_text(fg, behind, min_ratio, red_min)
    if _rgb_key(new) == _rgb_key(fg):
        return
    text_style.set("textColor", format_qgis_colour(new, 255))


def patch_label_contrast(layer, style=None, palette=None):
    """Draw each configured label buffer. Darken ink that misses the contrast floor."""
    style = style or STYLE
    min_ratio = style["label_contrast"]["min_ratio"]
    red_min = style["label_contrast"]["red_light_min"]
    max_mm = style["label_contrast"]["halo_max_mm"]
    named = palette or []
    for settings in layer.findall(".//settings"):
        text_style = settings.find("text-style")
        if text_style is None:
            continue
        buffer_el = text_style.find("text-buffer")
        draw_configured_buffer(buffer_el, max_mm)
        behind = label_behind(buffer_el)
        props = _settings_props(settings)
        expression = _expr(props, "Color") if props is not None else None
        if _is_named_project_colour(expression):
            updated = colour_expression(named, behind, min_ratio, red_min)
            if updated:
                put_expr(props, "Color", updated)
            continue
        _darken_text_color(text_style, behind, min_ratio, red_min)


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


def carto_text_width_expression(chars, style=None):
    """Estimated width in metres of a carto_text line of chars characters at the sheet scale."""
    style = style or STYLE
    floor = style["labels"]["size_floor_pt"]
    metres_per_pt = 0.3528 / 1000 * SHEET_SCALE
    return (
        f"({chars} * max({floor}, coalesce(\"size\", {floor}))"
        f" * {style['labels']['carto_point']['advance_em']} * {metres_per_pt:g})"
    )


def curved_label_mode_expression(style=None):
    """Keep the stock stretch only where it adds space. A baseline shorter than the name would squeeze it."""
    width = carto_text_width_expression("length(\"text_string\")", style)
    return (
        "CASE WHEN \"charplace\" IN ('StretchWordSpacingToFit', 'StretchCharacterSpacingToFit')"
        f" AND (strpos(\"text_string\", '\\n') > 0 OR length($geometry) <= {width})"
        " THEN 'default' ELSE \"charplace\" END"
    )


def patch_wrap_baseline(layer):
    """Put each line of a folded carto_text name on its own forward pass."""
    placement = layer.find("./labeling/settings/placement")
    if placement is None:
        return
    placement.set("geometryGenerator", wrap_baseline_expression())
    placement.set("geometryGeneratorEnabled", "1")
    placement.set("geometryGeneratorType", "LineGeometry")


CARTO_POINT_FILTER = (
    "\"text_placement\" = 1 AND \"text_orientation\" = 0"
    " AND strpos(coalesce(\"text_string\", ''), '\\n') = 0"
    " AND num_points($geometry) <= 2"
)
CURVED_ONLY_PROPERTIES = (
    "LinePlacementFlags",
    "LineAnchorPercent",
    "LineAnchorTextPoint",
    "CurvedLabelMode",
)
ABOVE_BELOW_MAP_ORIENTED = 2 | 4 | 8
MULTILINE_CENTRE = "1"
CARTO_FLAT_TEXT = "regexp_replace(replace(\"text_string\", ' / ', ' /\\n'), '^Te ', 'Te\u00a0')"


def carto_flat_wrap_expression(style=None):
    """Wrap a long single name; a dual name already breaks after its slash."""
    chars = (style or STYLE)["labels"]["carto_point"]["wrap_chars"]
    return (
        f"CASE WHEN strpos(\"text_string\", ' / ') = 0 AND length(\"text_string\") > {chars}"
        f" THEN {chars} ELSE 0 END"
    )


CARTO_FIT_FILE = "carto_fit.json"


def load_carto_fit(project_dir):
    """Return fitted flat names by row id from carto_fit.json beside the project, or {} when absent."""
    if not project_dir:
        return {}
    path = os.path.join(project_dir, CARTO_FIT_FILE)
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def carto_fit_value(fit, key):
    """Expression for one fitted value of this row; NULL for a row with no fit."""
    literal = json.dumps(fit, separators=(",", ":")).replace("'", "''")
    return f"map_get(map_get(json_to_map('{literal}'), \"id\"), '{key}')"


def carto_fit_text_expression(fit):
    """A row fitted to one line drops the slash break."""
    return f"CASE WHEN {carto_fit_value(fit, 'lines')} = 1 THEN \"text_string\" ELSE {CARTO_FLAT_TEXT} END"


def carto_flat_line_expression(style=None):
    """Horizontal line at the stock baseline, centred on the stock label.

    It is the estimated width of the longest label line plus the allowance at each end.
    @map_scale is null in a label geometry generator, so the sheet scale is fixed.
    """
    style = style or STYLE
    allowance = style["labels"]["carto_point"]["allowance_mm"] * SHEET_SCALE / 1000
    longest = f"array_max(array_foreach(string_to_array({CARTO_FLAT_TEXT}, '\\n'), length(@element)))"
    half = f"({carto_text_width_expression(longest, style)} / 2 + {allowance:g})"
    return (
        "with_variable('cx', x(centroid(bounds(@geometry))), with_variable('y', y_min(@geometry), "
        f"make_line(make_point(@cx - {half}, @y), make_point(@cx + {half}, @y))))"
    )


def _rule(settings, filter_expression, description):
    rule = ET.Element(
        "rule",
        {"description": description, "filter": filter_expression, "key": "{" + str(uuid.uuid4()) + "}"},
    )
    rule.append(settings)
    return rule


def patch_carto_point_labels(layer, style=None, fit=None):
    """Let QGIS slide a flat one-line carto_text name a short way, or flip it below its baseline.

    A dual name breaks after its slash and a long single name wraps, so the label is narrower and easier to place.
    A row in fit is drawn at its fitted bottom-centre point, on one line or in the default form.
    """
    style = style or STYLE
    labeling = layer.find("labeling")
    if labeling is None or labeling.get("type") != "simple":
        return
    settings = labeling.find("settings")
    if settings is None or settings.find("placement") is None:
        return
    point = copy.deepcopy(settings)
    carto = style["labels"]["carto_point"]
    placement = point.find("placement")
    placement.set("placement", "2")
    placement.set("placementFlags", str(ABOVE_BELOW_MAP_ORIENTED))
    placement.set("overrunDistance", str(carto["overrun_mm"]))
    placement.set("overrunDistanceUnit", "MM")
    placement.set("geometryGenerator", carto_flat_line_expression(style))
    placement.set("geometryGeneratorEnabled", "1")
    placement.set("geometryGeneratorType", "LineGeometry")
    placement.set("multipartBehavior", "LabelLargestPartOnly")
    text_style = point.find("text-style")
    if text_style is not None:
        text_style.set("fieldName", carto_fit_text_expression(fit) if fit else CARTO_FLAT_TEXT)
        text_style.set("isExpression", "1")
        text_style.set("multilineHeight", str(carto["line_height"]))
        text_style.set("multilineHeightUnit", "Percentage")
    text_format = point.find("text-format")
    if text_format is not None:
        text_format.set("multilineAlign", MULTILINE_CENTRE)
        text_format.set("useMaxLineLengthForAutoWrap", "1")
    props = _settings_props(point)
    if props is not None:
        for child in list(props):
            if child.get("name") in CURVED_ONLY_PROPERTIES:
                props.remove(child)
        wrap = carto_flat_wrap_expression(style)
        if fit:
            wrap = f"CASE WHEN {carto_fit_value(fit, 'lines')} = 1 THEN 0 ELSE {wrap} END"
        put_expr(props, "AutoWrapLength", wrap)
        if fit:
            put_expr(props, "PositionX", carto_fit_value(fit, "x"))
            put_expr(props, "PositionY", carto_fit_value(fit, "y"))
            put_expr(props, "Hali", "'Center'")
            put_expr(props, "Vali", "'Bottom'")
    labeling.remove(settings)
    labeling.set("type", "rule-based")
    rules = ET.SubElement(labeling, "rules", {"key": "{" + str(uuid.uuid4()) + "}"})
    rules.append(_rule(settings, f"NOT ({CARTO_POINT_FILTER})", "Baseline"))
    rules.append(_rule(point, CARTO_POINT_FILTER, "Flat one-line"))


def patch_labels(layer, layer_name, style=None, palette=None, fit=None):
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
        if layer_name == CARTO_TEXT_LAYER and "CurvedLabelMode" in present:
            put_expr(props, "CurvedLabelMode", curved_label_mode_expression(style))
    if layer_name == CARTO_TEXT_LAYER:
        patch_wrap_baseline(layer)
        patch_carto_point_labels(layer, style, fit)
    patch_label_contrast(layer, style, palette)
    return count


def patch_contour(layer, style=None):
    style = style or STYLE
    index = style["contours"]["index"]
    intermediate = style["contours"]["intermediate"]
    _require_field(layer, "elevation")
    symbol = layer.find("renderer-v2/symbols/symbol")
    lines = symbol.findall("layer[@class='SimpleLine']")
    if not lines:
        raise RuntimeError("contour symbol has no SimpleLine")
    if len(lines) == 1:
        casing = copy.deepcopy(lines[0])
        casing.set("id", "{" + str(uuid.uuid4()) + "}")
        symbol.insert(list(symbol).index(lines[0]), casing)
        fill = lines[0]
    else:
        casing = lines[0]
        fill = lines[1]
    # definition is null on the national contour table, so indefinite
    # contours cannot be dashed from that field.
    casing_props = _properties_map(casing.find("data_defined_properties"))
    put_expr(
        casing_props,
        "enabled",
        '"elevation" IS NOT NULL AND round("elevation") % 100 <> 0',
    )
    put_expr(casing_props, "outlineColor", _rgba_call(intermediate["casing_colour"], intermediate["alpha"]))
    put_expr(casing_props, "outlineWidth", str(intermediate["casing_width_mm"]))
    _set_option(casing, "line_color", _rgba(intermediate["casing_colour"], _alpha_byte(intermediate["alpha"])))
    _set_option(casing, "line_width", str(intermediate["casing_width_mm"]))
    fill_props = _properties_map(fill.find("data_defined_properties"))
    put_expr(
        fill_props,
        "outlineColor",
        "CASE WHEN \"elevation\" IS NOT NULL AND round(\"elevation\") % 100 = 0"
        f" THEN {_rgba_call(index['colour'], index['alpha'])}"
        f" ELSE {_rgba_call(intermediate['colour'], intermediate['alpha'])} END",
    )
    put_expr(
        fill_props,
        "outlineWidth",
        'CASE WHEN "elevation" IS NOT NULL AND round("elevation") % 100 = 0'
        f" THEN {index['width_mm']} ELSE {intermediate['width_mm']} END",
    )


def patch_road_fills(layer, style=None):
    """Replace painted PMS151 road fills with the owned road ink."""
    style = style or STYLE
    ink = _rgba(style["reference_inks"]["project_road"], 255)
    for line in layer.findall(".//layer[@class='SimpleLine']"):
        option = line.find("Option/Option[@name='line_color']")
        if option is None:
            continue
        if _rgb_tuple(option.get("value") or "") != PMS151_RGB:
            continue
        _set_option(line, "line_color", ink)


def patch_contour_numbers(layer, style=None):
    """Paint contour_number FontMarkers with the index contour ink."""
    style = style or STYLE
    symbol = _rule_symbol(layer, "contour_number")
    marker = symbol.find("layer[@class='FontMarker']")
    if marker is None:
        raise RuntimeError("contour_number has no FontMarker")
    _set_option(marker, "color", _rgba(style["contours"]["index"]["colour"], 255))


def _mask_contour_casing(root):
    contour = None
    for layer in root.findall("projectlayers/maplayer"):
        if (layer.findtext("layername") or "") == "contour":
            contour = layer
            break
    if contour is None:
        return
    lines = contour.findall("renderer-v2/symbols/symbol/layer[@class='SimpleLine']")
    if len(lines) < 2:
        return
    fill_id = lines[1].get("id")
    casing_id = lines[0].get("id")
    if not fill_id or not casing_id:
        return
    layer_id = contour.findtext("id") or ""
    token = f"{layer_id};{casing_id}" if layer_id else casing_id
    for mask in root.iter("text-mask"):
        current = mask.get("maskedSymbolLayers") or ""
        if fill_id in current and casing_id not in current:
            mask.set("maskedSymbolLayers", current + ";" + token)


def _mm(value):
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def closed_bar_placement(track):
    """Return the interval and the offset that put one bar in each dash gap."""
    on_text, off_text = track["closed_dash"].split(";")
    on = float(on_text)
    off = float(off_text)
    return _mm(on + off), _mm(on + off / 2)


def _closed_crossbar(style=None):
    style = style or STYLE
    track = style["tracks"]["closed_foot"]
    ink = _rgba(track["crossbar_colour"], 255)
    interval, along = closed_bar_placement(track)
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


def _closed_marker(symbol):
    for marker in symbol.findall("layer[@class='MarkerLine']"):
        dd = marker.find("data_defined_properties")
        if dd is None:
            continue
        props = dd.find("Option/Option[@name='properties']")
        if props is not None and _expr(props, "enabled") and "closed" in _expr(props, "enabled"):
            return marker
    return None


def _sync_closed_crossbar(marker, style):
    track = style["tracks"]["closed_foot"]
    ink = _rgba(track["crossbar_colour"], 255)
    interval, along = closed_bar_placement(track)
    _set_option(marker, "interval", interval)
    _set_option(marker, "offset_along_line", along)
    simple = marker.find("symbol/layer[@class='SimpleMarker']")
    if simple is None:
        raise RuntimeError("closed cross-bar has no marker")
    for name, value in (
        ("angle", str(track["crossbar_angle_deg"])),
        ("color", ink),
        ("outline_color", ink),
        ("outline_width", str(track["crossbar_outline_width_mm"])),
        ("size", str(track["crossbar_size_mm"])),
    ):
        _set_option(simple, name, value)


def patch_tracks(layer, style=None):
    style = style or STYLE
    if style["tracks"]["access"]["painted"]:
        raise RuntimeError("track access is reserved and must not be painted")
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
    existing = _closed_marker(symbol)
    if existing is None:
        symbol.append(_closed_crossbar(style))
    else:
        _sync_closed_crossbar(existing, style)


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


def _tree_layer_parent(group, name):
    """Return (parent, node) for a layer-tree-layer with this name."""
    for child in list(group):
        if child.tag == "layer-tree-layer" and child.get("name") == name:
            return group, child
        if child.tag == "layer-tree-group":
            found = _tree_layer_parent(child, name)
            if found is not None:
                return found
    return None


def hillshade_rules(style=None):
    """Return the hillshade block. Values live in tools/style-topo50.json."""
    return (style or STYLE)["hillshade"]


def dem_path(project_dir, style=None):
    """Return the DEM path beside the project."""
    return os.path.join(project_dir, hillshade_rules(style)["raster_file"])


def hillshade_should_paint(project_dir, style=None):
    """Return whether raster hillshade should turn on."""
    if not project_dir:
        return False
    if not hillshade_rules(style)["painted"]:
        return False
    return os.path.isfile(dem_path(project_dir, style))


def _copy_project_srs(root):
    source = root.find("projectCrs/spatialrefsys")
    if source is None:
        raise RuntimeError("project has no projectCrs")
    return copy.deepcopy(source)


def _ensure_dem_layer(root, style=None):
    layers = root.find("projectlayers")
    if layers is None:
        raise RuntimeError("project has no projectlayers")
    rules = hillshade_rules(style)
    existing = None
    for layer in layers.findall("maplayer"):
        if layer.findtext("layername") == DEM_LAYER_NAME:
            existing = layer
            break
    if existing is None:
        layer = ET.SubElement(layers, "maplayer")
        layer.set("type", "raster")
        layer.set("styleCategories", "AllStyleCategories")
        ident = ET.SubElement(layer, "id")
        ident.text = DEM_LAYER_ID
        name = ET.SubElement(layer, "layername")
        name.text = DEM_LAYER_NAME
        provider = ET.SubElement(layer, "provider")
        provider.text = "gdal"
        srs = ET.SubElement(layer, "srs")
        srs.append(_copy_project_srs(root))
        pipe = ET.SubElement(layer, "pipe")
        renderer = ET.SubElement(pipe, "rasterrenderer")
        renderer.set("type", "singlebandgray")
        renderer.set("opacity", "0")
        renderer.set("grayBand", "1")
        elevation = ET.SubElement(layer, "elevation")
        elevation.set("enabled", "1")
        elevation.set("mode", "RepresentsElevationSurface")
        elevation.set("band", "1")
        tree = root.find("layer-tree-group")
        if tree is not None:
            node = ET.SubElement(tree, "layer-tree-layer")
            node.set("checked", "Qt::Unchecked")
            node.set("expanded", "0")
            node.set("id", DEM_LAYER_ID)
            node.set("name", DEM_LAYER_NAME)
            node.set("providerKey", "gdal")
            node.set("source", f"./{rules['raster_file']}")
        existing = layer
    datasource = existing.find("datasource")
    if datasource is None:
        datasource = ET.SubElement(existing, "datasource")
    datasource.text = f"./{rules['raster_file']}"


def _set_raster_terrain(root):
    props = root.find("ElevationProperties")
    if props is None:
        props = ET.SubElement(root, "ElevationProperties")
    provider = props.find("terrainProvider")
    if provider is None:
        provider = ET.SubElement(props, "terrainProvider")
    provider.set("type", "raster")
    inner = provider.find("TerrainProvider")
    if inner is None:
        inner = ET.SubElement(provider, "TerrainProvider")
        inner.set("offset", "0")
        inner.set("scale", "1")
    inner.set("layer", DEM_LAYER_ID)


def patch_hillshade(root, project_dir=None, style=None):
    """Write R-03 lights onto the project shader. Turn it on only when dem.tif is present."""
    renderer = root.find("elevation-shading-renderer")
    if renderer is None:
        return
    rules = hillshade_rules(style)
    renderer.set("light-azimuth", str(rules["azimuth_deg"]))
    renderer.set("light-altitude", str(rules["altitude_deg"]))
    renderer.set("hillshading-is-multidirectional", "1" if rules["multidirectional"] else "0")
    renderer.set("hillshading-z-factor", str(rules["z_factor"]))
    on = hillshade_should_paint(project_dir, style)
    renderer.set("is-active", "1" if on else "0")
    renderer.set("hillshading-is-active", "1" if on else "0")
    if on:
        _ensure_dem_layer(root, style)
        _set_raster_terrain(root)


def patch_draw_order(root, style=None):
    """Move named layer-tree nodes so each sits immediately under its pair."""
    style = style or STYLE
    rules = style.get("draw_order") or []
    if not rules:
        return
    tree = root.find("layer-tree-group")
    if tree is None:
        raise RuntimeError("project has no layer-tree-group")
    for rule in rules:
        moving_name = rule["name"]
        below_name = rule["below"]
        moving_found = _tree_layer_parent(tree, moving_name)
        below_found = _tree_layer_parent(tree, below_name)
        if moving_found is None:
            raise RuntimeError(f"missing layer-tree node: {moving_name}")
        if below_found is None:
            raise RuntimeError(f"missing layer-tree node: {below_name}")
        parent, moving = moving_found
        below_parent, below = below_found
        if parent is not below_parent:
            raise RuntimeError(f"{moving_name} and {below_name} are not in the same group")
        parent.remove(moving)
        index = list(parent).index(below)
        parent.insert(index + 1, moving)


def apply(root, project_dir=None):
    """Patch map layers. Return a count of label styles touched."""
    layers = root.find("projectlayers")
    if layers is None:
        raise RuntimeError("project has no projectlayers")
    labels = 0
    seen = set()
    palette = project_palette(root)
    fit = load_carto_fit(project_dir)
    for layer in layers.findall("maplayer"):
        name = layer.findtext("layername") or ""
        labels += patch_labels(layer, name, palette=palette, fit=fit)
        if name == "contour":
            patch_contour(layer)
            seen.add(name)
        elif is_owned_road_layer(name):
            patch_road_fills(layer)
        elif name == "nztopo50_carto_symbol":
            patch_contour_numbers(layer)
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
    _mask_contour_casing(root)
    patch_draw_order(root)
    patch_hillshade(root, project_dir)
    return labels


def main(src, dst):
    doctype = ""
    with open(src, encoding="utf-8") as handle:
        first = handle.readline()
        if first.startswith("<!DOCTYPE"):
            doctype = first if first.endswith("\n") else first + "\n"
    root = ET.parse(src).getroot()
    labels = apply(root, project_dir=os.path.dirname(os.path.abspath(dst)))
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
