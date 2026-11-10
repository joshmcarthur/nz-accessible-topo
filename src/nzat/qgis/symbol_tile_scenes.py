"""Test scenes for one legend symbol: each background fill, then each conflict.

A tile is a 10 mm square at sheet size, centred on the legend swatch. The
symbol features come from `legend_swatches.SWATCHES`. A scene adds one fill
under the symbol, or one other class across it. Geometry is WKT in stock
legend pixels, as in the swatch table.
"""

TILE_PX = 236  # 10 mm at 600 dpi
_MARGIN_PX = 20
_CONTOUR_STEP_PX = 24  # 1 mm: a steep slope at 1:50,000

# The fill classes a symbol can sit on. None is bare paper.
BACKGROUNDS = {
    "paper": None,
    "native": ("vegetation", {"type": "native"}),
    "exotic": ("vegetation", {"type": "exotic", "subtype": "coniferous"}),
    "scrub": ("vegetation", {"type": "scrub"}),
    "scattered": ("vegetation", {"type": "scattered_scrub"}),
    "water": ("water", {"type": "lake"}),
    "urban": ("residential_area", {}),
    "sand": ("landcover", {"type": "sand"}),
    "swamp": ("landcover", {"type": "swamp"}),
    "ice": ("landcover", {"type": "ice"}),
}

# A flat black settlement name, with the attributes a real row has.
_NAME = {
    "id": "nzat-symbol-tile-name",
    "full_text": "Ōtira",
    "text_string": "Ōtira",
    "text_bend": 0,
    "text_char_spacing_distance": 0.0,
    "text_colour": 9,
    "text_font": "ATTriumMou-Cond",
    "text_height": 0.0019,
    "text_orientation": 0.0,
    "text_placement": 1,
    "text_size_type": 0,
    "text_stretch_length": 0.0,
    "text_word_spacing_distance": 0.0,
    "font": "Nimbus Sans LINZ",
    "style": "Narrow",
    "colour": "black",
    "size": 8.0,
    "placement": "AL",
    "offset": -2.7,
}


def tile_box(box):
    """Return the TILE_PX square centred on a swatch box."""
    x0, y0, x1, y1 = box
    left = round((x0 + x1) / 2 - TILE_PX / 2)
    top = round((y0 + y1) / 2 - TILE_PX / 2)
    return (left, top, left + TILE_PX, top + TILE_PX)


def _fill(tile):
    x0, y0, x1, y1 = tile
    x0, y0, x1, y1 = (
        x0 - _MARGIN_PX,
        y0 - _MARGIN_PX,
        x1 + _MARGIN_PX,
        y1 + _MARGIN_PX,
    )
    return f"POLYGON (({x0} {y0}, {x1} {y0}, {x1} {y1}, {x0} {y1}, {x0} {y0}))"


def _contours(tile):
    """Parallel 20 m contours on a diagonal. Every fifth is an index contour."""
    x0, y0, x1, y1 = tile
    features = []
    for index, shift in enumerate(range(-TILE_PX, TILE_PX, _CONTOUR_STEP_PX)):
        wkt = f"LINESTRING ({x0 + shift} {y1}, {x0 + shift + TILE_PX} {y0})"
        attrs = {"type": "contour", "elevation": 20 * (index + 1)}
        features.append(("contour", attrs, wkt))
    return features


def _grid(tile):
    x0, y0, x1, y1 = tile
    x = (x0 + x1) / 2
    wkt = f"LINESTRING ({x} {y0 - _MARGIN_PX}, {x} {y1 + _MARGIN_PX})"
    return [("nz_topo50_grid", {"direction": "y", "value": 1570000.0}, wkt)]


def _stream(tile):
    x0, y0, x1, y1 = tile
    return [("water_line", {"type": "river"}, f"LINESTRING ({x0} {y0}, {x1} {y1})")]


def _road(tile):
    x0, y0, x1, y1 = tile
    attrs = {"type": "road", "lane_count": 2, "surface": "sealed"}
    return [("road_line", attrs, f"LINESTRING ({x0} {y1}, {x1} {y0})")]


def _name(tile):
    x0, y0, x1, y1 = tile
    y = (y0 + y1) / 2
    wkt = f"LINESTRING ({x0 + 20} {y}, {x1 - 20} {y})"
    return [("nztopo50_carto_text", dict(_NAME), wkt)]


# The other classes that can cross a symbol. Each one draws on bare paper.
CONFLICTS = {
    "contours": _contours,
    "grid": _grid,
    "stream": _stream,
    "road": _road,
    "name": _name,
}


def is_area_swatch(features):
    """True when every sample is a polygon. A fill has no fill to sit on."""
    return all(wkt.startswith("POLYGON") for _table, _attrs, wkt in features)


def tile_scenes(swatch):
    """Return (scene name, features) for one swatch, backgrounds first."""
    tile = tile_box(swatch["box"])
    symbol = tuple(swatch["features"])
    scenes = []
    for name, fill in BACKGROUNDS.items():
        if fill is None:
            scenes.append((name, symbol))
        elif not is_area_swatch(symbol):
            table, attrs = fill
            scenes.append((name, ((table, attrs, _fill(tile)), *symbol)))
    for name, build in CONFLICTS.items():
        scenes.append((name, (*symbol, *build(tile))))
    return scenes


# Conditions that do not gate an area fill. Only the ink that draws a shape
# must meet the floors; lines and points on the fill stay gated.
AREA_SHOWN = ("grey", "red", "acuity")
HIDDEN_BELOW = 0.05

# Josh accepted these as written exceptions.
ACCEPTED = {
    "intermediate_contours": "The 20 m mesh is recessive by design (log 0054).",
    "supplementary_contour": "It draws as an intermediate contour (log 0054).",
}

# Scenes that say nothing about a class, with the reason the page shows.
_ICE_ONLY = "Ice contours draw only on ice."
_GATE_ON_WATER = (
    "The gate mark draws. The sample watercourse beside it is under the fill,"
    " as on the stock map."
)
_RARE_ON_URBAN = (
    "Accepted: rare inside the urban fill, and the stock map draws it the same"
    " way. Its dark edges and white centre blur to the urban grey."
)
NOT_ON = {
    "unmetalled": {"urban": _RARE_ON_URBAN},
    "bridge_one_lane": {"urban": _RARE_ON_URBAN},
    "ice_contours": {
        scene: _ICE_ONLY
        for scene in ("native", "exotic", "scrub", "scattered", "sand", "swamp")
    },
    "floodgate": {
        "water": _GATE_ON_WATER,
        "urban": _GATE_ON_WATER,
        # The gate is a point mark. Its sample has a watercourse line too.
        "name": "The name wins. Its halo keeps the name clear of the mark.",
    },
}


def is_point_swatch(features):
    """True when every sample is a point."""
    return all(wkt.startswith("POINT") for _table, _attrs, wkt in features)


def scene_exception(key, scene, features, normal_visible):
    """Return why a tile does not gate the symbol, or None when it does."""
    if key in ACCEPTED:
        return ACCEPTED[key]
    if scene in NOT_ON.get(key, {}):
        return NOT_ON[key][scene]
    if scene in ("water", "urban") and normal_visible < HIDDEN_BELOW:
        return "LINZ draws this class under the fill. The stock map does the same."
    if scene == "road" and is_point_swatch(features):
        return "A road does not cross a point mark."
    if scene == "name" and is_point_swatch(features):
        return "The name wins. Its halo keeps the name clear of the mark."
    return None


def gated_conditions(features, conditions):
    """Return the conditions that can fail this symbol."""
    if is_area_swatch(features):
        return [c for c in conditions if c not in AREA_SHOWN]
    return list(conditions)
