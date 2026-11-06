"""Swatches the accessible legend draws over the stock legend image.

The stock legend is `topo-legend-1.tif` (2323 x 11247 px, 600 dpi). Its labels
are part of the image, so the labels stay. Each swatch box is cleared and
redrawn with the applied map layers that read the swatch tables (log 0092).

Boxes are (x0, y0, x1, y1) and geometry is WKT, both in stock legend pixels.
Each feature carries the attributes a real feature of that class has.
"""

STOCK_LEGEND_FILE = "topo-legend-1.tif"
ACCESSIBLE_LEGEND_FILE = "topo-legend-accessible.png"
LEGEND_DPI = 600
LEGEND_SIZE = (2323, 11247)


def _line(y, x0=1667, x1=2015):
    return f"LINESTRING ({x0} {y}, {x1} {y})"


def _strip(y0, y1, x0=1667, x1=2015):
    return f"POLYGON (({x0} {y0}, {x1} {y0}, {x1} {y1}, {x0} {y1}, {x0} {y0}))"


def _road(lanes, surface, y, highway=None):
    attrs = {"type": "road", "lane_count": lanes, "surface": surface}
    if highway is not None:
        attrs["highway_number"] = highway
    return ("road_line", attrs, _line(y))


def _track(y, x0=1667, x1=2015, **attrs):
    return (
        "track_line",
        {"type": "track", "subtype": "foot", **attrs},
        _line(y, x0, x1),
    )


def _contour(table, elevation, y, **attrs):
    return (table, {"type": "contour", "elevation": elevation, **attrs}, _line(y))


def _vegetation(kind, y0, y1, subtype=None):
    attrs = {"type": kind}
    if subtype is not None:
        attrs["subtype"] = subtype
    return ("vegetation", attrs, _strip(y0, y1))


def _pt(x, y):
    return f"POINT ({x} {y})"


def _typed(table, kind, wkt, **extra):
    return (table, {"type": kind, "feature_type": kind, **extra}, wkt)


def _box_line(box, inset=12):
    x0, y0, x1, y1 = box
    return _line((y0 + y1) / 2, x0 + inset, x1 - inset)


def _box_pt(box):
    x0, y0, x1, y1 = box
    return _pt((x0 + x1) / 2, (y0 + y1) / 2)


def _box_strip(box, inset=8):
    x0, y0, x1, y1 = box
    return _strip(y0 + inset, y1 - inset, x0 + inset, x1 - inset)


def _row(key, box, *features, **extra):
    item = {"key": key, "box": box, "features": features}
    item.update(extra)
    return item


SWATCHES = (
    {
        "key": "state_highway",
        "box": (1655, 258, 2035, 353),
        "features": (
            _road(2, "sealed", 305.5, highway="1"),
            (
                "nztopo50_carto_symbol",
                {"type": "highway_shield", "label": "1", "orientation": 0},
                "POINT (1841 305.5)",
            ),
        ),
    },
    {
        "key": "four_lanes",
        "box": (1655, 357, 2035, 445),
        "features": (_road(4, "sealed", 400.5),),
    },
    {
        "key": "two_lanes",
        "box": (1655, 451, 2035, 539),
        "features": (_road(2, "sealed", 494.5),),
    },
    {
        "key": "narrow_road",
        "box": (1655, 545, 2035, 633),
        "features": (_road(1, "sealed", 589),),
    },
    {
        "key": "vehicle_track",
        "box": (1655, 641, 2035, 729),
        "features": (_track(685, subtype="vehicle"),),
    },
    {"key": "foot_track", "box": (1655, 737, 2035, 825), "features": (_track(781.5),)},
    {
        "key": "closed_track",
        "box": (1655, 831, 2035, 919),
        "features": (_track(875, status="closed"),),
    },
    {
        "key": "poled_route_connector",
        "box": (1655, 926, 2035, 1014),
        "features": (
            _track(970, x1=1825, track_type="route"),
            _track(970, x0=1870, track_type="connector"),
        ),
    },
    {
        "key": "sealed",
        "box": (1655, 1015, 2035, 1103),
        "features": (_road(2, "sealed", 1058.5),),
    },
    {
        "key": "metalled",
        "box": (1655, 1110, 2035, 1198),
        "features": (_road(2, "metalled", 1153.5),),
    },
    {
        "key": "unmetalled",
        "box": (1655, 1204, 2035, 1292),
        "features": (_road(1, "unmetalled", 1247.5),),
    },
    _row(
        "tunnel",
        (1655, 1290, 1880, 1384),
        _typed("tunnel_line", "tunnel", _box_line((1655, 1290, 1880, 1384))),
    ),
    _row(
        "tunnel_under_road",
        (1880, 1290, 2035, 1384),
        _typed("tunnel_line", "tunnel", _box_line((1880, 1290, 2035, 1384))),
    ),
    _row(
        "bridge_two_lane",
        (1655, 1388, 1850, 1478),
        (
            "bridge_line",
            {"bridge_use": "vehicle", "lanes": "2"},
            _box_line((1655, 1388, 1850, 1478)),
        ),
    ),
    _row(
        "bridge_one_lane",
        (1850, 1388, 2035, 1478),
        (
            "bridge_line",
            {"bridge_use": "vehicle", "lanes": "1"},
            _box_line((1850, 1388, 2035, 1478)),
        ),
    ),
    _row(
        "gate",
        (1655, 1576, 1780, 1668),
        (
            "road_line",
            {"type": "road", "lane_count": 2, "surface": "sealed"},
            _box_line((1655, 1576, 1780, 1668)),
        ),
        _typed(
            "structure_point",
            "gate",
            _box_pt((1655, 1576, 1780, 1668)),
            orientation=0,
        ),
    ),
    _row(
        "locked_gate",
        (1780, 1576, 1900, 1668),
        (
            "road_line",
            {"type": "road", "lane_count": 2, "surface": "sealed"},
            _box_line((1780, 1576, 1900, 1668)),
        ),
        _typed(
            "structure_point",
            "gate",
            _box_pt((1780, 1576, 1900, 1668)),
            restrictions="locked",
            subtype="locked",
            orientation=0,
        ),
    ),
    _row(
        "cableway",
        (1745, 1667, 1825, 1765),
        _typed(
            "structure_line",
            "cableway_people",
            _box_line((1745, 1667, 1825, 1765), inset=8),
        ),
    ),
    _row(
        "rail_double",
        (1655, 1962, 2035, 2054),
        _typed(
            "railway_line",
            "railway",
            _box_line((1655, 1962, 2035, 2054)),
            track_type="multiple",
        ),
    ),
    _row(
        "rail_single",
        (1655, 2056, 2035, 2148),
        _typed(
            "railway_line",
            "railway",
            _box_line((1655, 2056, 2035, 2148)),
            track_type="single",
        ),
    ),
    _row(
        "rail_tunnel",
        (1840, 2245, 2035, 2337),
        _typed("tunnel_line", "tunnel", _box_line((1840, 2245, 2035, 2337))),
    ),
    _row(
        "level_crossing",
        (1655, 2339, 2035, 2431),
        _road(2, "sealed", 2385),
        _typed("railway_line", "railway", _line(2385)),
    ),
    _row(
        "road_over_railway",
        (1655, 2434, 2035, 2526),
        (
            "bridge_line",
            {"bridge_use": "vehicle", "lanes": "2"},
            _box_line((1655, 2434, 2035, 2526)),
        ),
        _typed(
            "railway_line",
            "railway",
            _box_line((1655, 2434, 2035, 2526)),
        ),
    ),
    _row(
        "residential_area",
        (1655, 2901, 2035, 2993),
        ("residential_area", {}, _box_strip((1655, 2901, 2035, 2993))),
    ),
    _row(
        "large_buildings",
        (1655, 3001, 2035, 3093),
        ("building", {}, _box_strip((1655, 3001, 2035, 3093), 20)),
    ),
    _row(
        "isolated_building",
        (1655, 3095, 2035, 3187),
        ("building_point", {}, _box_pt((1655, 3095, 2035, 3187))),
    ),
    _row(
        "homestead",
        (1655, 3190, 1880, 3282),
        ("building_point", {"subtype": "homestead"}, _box_pt((1655, 3190, 1880, 3282))),
    ),
    _row(
        "stockyard",
        (1880, 3190, 2035, 3282),
        _typed("structure_point", "stockyard", _box_pt((1880, 3190, 2035, 3282))),
    ),
    _row(
        "glasshouse",
        (1655, 3284, 2035, 3376),
        ("building", {"subtype": "greenhouse"}, _box_strip((1655, 3284, 2035, 3376))),
    ),
    _row(
        "church",
        (1655, 3379, 1735, 3471),
        ("building_point", {"subtype": "church"}, _box_pt((1655, 3379, 1735, 3471))),
    ),
    _row(
        "cemetery",
        (1735, 3379, 1945, 3471),
        _typed("landuse", "cemetery", _box_strip((1735, 3379, 1945, 3471))),
    ),
    _row(
        "training_track",
        (1655, 3465, 2035, 3565),
        _typed("landuse", "racetrack", _box_strip((1655, 3465, 2035, 3565))),
    ),
    _row(
        "golf_course",
        (1655, 3565, 1880, 3660),
        (
            "nztopo50_carto_symbol",
            {"type": "golf_course"},
            _box_pt((1655, 3565, 1880, 3660)),
        ),
    ),
    _row(
        "redoubt",
        (1765, 3662, 1850, 3754),
        _typed("structure_point", "redoubt", _box_pt((1765, 3662, 1850, 3754))),
    ),
    _row(
        "reservoir_uncovered",
        (1770, 3755, 1890, 3847),
        _typed("water", "reservoir", _box_strip((1770, 3755, 1890, 3847))),
    ),
    _row(
        "tank",
        (1890, 3755, 2035, 3847),
        _typed(
            "structure_point",
            "tank",
            _box_pt((1890, 3755, 2035, 3847)),
            stored_item="water",
        ),
    ),
    _row(
        "mast",
        (1655, 3850, 1770, 3942),
        _typed("structure_point", "mast", _box_pt((1655, 3850, 1770, 3942))),
    ),
    _row(
        "tower",
        (1770, 3850, 1890, 3942),
        _typed("structure_point", "tower", _box_pt((1770, 3850, 1890, 3942))),
    ),
    _row(
        "wind_machine",
        (1890, 3850, 2035, 3942),
        _typed("structure_point", "windmill", _box_pt((1890, 3850, 2035, 3942))),
    ),
    _row(
        "shipwreck",
        (1655, 3946, 1790, 4038),
        _typed(
            "structure_point",
            "wreck",
            _box_pt((1655, 3946, 1790, 4038)),
            wreck_of="ship",
        ),
    ),
    _row(
        "lighthouse",
        (1790, 3946, 1890, 4038),
        _typed("structure_point", "lighthouse", _box_pt((1790, 3946, 1890, 4038))),
    ),
    _row(
        "marine_beacon",
        (1890, 3946, 2035, 4038),
        _typed("structure_point", "beacon", _box_pt((1890, 3946, 2035, 4038))),
    ),
    _row(
        "fence",
        (1655, 4040, 2035, 4132),
        ("fence_line", {}, _box_line((1655, 4040, 2035, 4132))),
    ),
    _row(
        "industrial_cableway",
        (1655, 4702, 2035, 4794),
        _typed(
            "structure_line",
            "cableway_industrial",
            _box_line((1655, 4702, 2035, 4794)),
        ),
    ),
    _row(
        "mine_opencast",
        (1840, 4796, 2035, 4888),
        (
            "nztopo50_carto_symbol",
            {"type": "mine_opencast"},
            _box_pt((1840, 4796, 2035, 4888)),
        ),
    ),
    {
        "key": "index_contour",
        "box": (1655, 5180, 2035, 5246),
        "features": (
            _contour("contour", 100, 5220),
            (
                "nztopo50_carto_symbol",
                {"type": "contour_number", "label": "100", "orientation": 0},
                "POINT (1837 5220)",
            ),
        ),
    },
    {
        "key": "intermediate_contours",
        "box": (1655, 5250, 2035, 5336),
        "features": tuple(
            _contour("contour", elevation, y)
            for elevation, y in ((80, 5270), (60, 5286), (40, 5302), (20, 5318))
        ),
    },
    {
        "key": "ice_contours",
        "box": (1655, 5341, 2035, 5432),
        # The stock row has no number. The map labels the index ice contour.
        "labels": False,
        "features": tuple(
            _contour("nztopo50_ice_contour", elevation, y)
            for elevation, y in ((120, 5364), (110, 5380), (100, 5396), (90, 5411))
        ),
    },
    {
        "key": "supplementary_contour",
        "box": (1655, 5466, 2035, 5520),
        "features": (_contour("contour", 10, 5496, designation="supplementary"),),
    },
    _row(
        "depression_contours",
        (1655, 5515, 2035, 5615),
        _contour("contour", 40, 5565, formation="depression"),
    ),
    _row(
        "small_depression_shaft",
        (1890, 5625, 2035, 5712),
        _typed("structure_point", "shaft", _box_pt((1890, 5625, 2035, 5712))),
    ),
    _row(
        "trig",
        (1655, 5740, 2035, 5835),
        ("trig_point", {"elevation": 1234}, _box_pt((1655, 5740, 2035, 5835))),
    ),
    _row(
        "trig_elevation",
        (1655, 5830, 1875, 5922),
        ("trig_point", {"elevation": 1234}, _box_pt((1655, 5830, 1875, 5922))),
    ),
    _row(
        "spot_height",
        (1875, 5830, 2035, 5922),
        (
            "relief_point",
            {"feature_type": "spot_height", "elevation": 842},
            _box_pt((1875, 5830, 2035, 5922)),
        ),
    ),
    _row(
        "cliff",
        (1655, 5930, 1782, 6022),
        _typed("relief_line", "cliff_edge", _box_line((1655, 5930, 1782, 6022), 8)),
    ),
    _row(
        "slip",
        (1910, 5930, 2035, 6022),
        _typed("relief_line", "slip_edge", _box_line((1910, 5930, 2035, 6022), 8)),
    ),
    _row(
        "rock_outcrops",
        (1655, 6025, 2035, 6117),
        _typed("landcover_point", "rock_outcrop", _box_pt((1655, 6025, 2035, 6117))),
    ),
    _row(
        "stopbank",
        (1655, 6119, 1850, 6211),
        _typed(
            "relief_line",
            "embankment",
            _box_line((1655, 6119, 1850, 6211)),
            relief_use="stopbank",
            subtype="stopbank",
        ),
    ),
    _row(
        "cutting",
        (1850, 6119, 2035, 6211),
        _typed("relief_line", "cutting_edge", _box_line((1850, 6119, 2035, 6211))),
    ),
    _row(
        "embankment",
        (1655, 6213, 2035, 6305),
        _typed(
            "relief_line",
            "embankment",
            _box_line((1655, 6213, 2035, 6305)),
            relief_use="causeway",
            subtype="causeway",
        ),
    ),
    _row(
        "saddle",
        (1655, 6306, 1840, 6398),
        (
            "relief_point",
            {"feature_type": "saddle", "type": "saddle"},
            _box_pt((1655, 6306, 1840, 6398)),
        ),
    ),
    _row(
        "moraine",
        (1655, 6492, 2035, 6584),
        _typed("landcover", "moraine", _box_strip((1655, 6492, 2035, 6584))),
    ),
    _row(
        "moraine_wall",
        (1655, 6586, 2035, 6678),
        _typed("landcover", "moraine_wall", _box_strip((1655, 6586, 2035, 6678))),
    ),
    _row(
        "scree",
        (1655, 6681, 2035, 6773),
        _typed("landcover", "scree", _box_strip((1655, 6681, 2035, 6773))),
    ),
    _row(
        "sand_mud",
        (1655, 7153, 2035, 7245),
        _typed("landcover", "mud", _box_strip((1655, 7153, 2035, 7245))),
    ),
    _row(
        "sand",
        (1655, 7248, 2035, 7340),
        _typed("landcover", "sand", _box_strip((1655, 7248, 2035, 7340))),
    ),
    _row(
        "shingle",
        (1655, 7347, 2035, 7439),
        _typed("landcover", "shingle", _box_strip((1655, 7347, 2035, 7439))),
    ),
    _row(
        "swamp",
        (1655, 7442, 2035, 7534),
        _typed("landcover", "swamp", _box_strip((1655, 7442, 2035, 7534))),
    ),
    _row(
        "boat_ramp",
        (1655, 7536, 2035, 7628),
        _typed("structure_line", "boatramp", _box_line((1655, 7536, 2035, 7628))),
    ),
    _row(
        "breakwater_wharf_jetty",
        (1655, 7631, 2035, 7723),
        _typed(
            "structure_line",
            "wharf",
            _box_line((1655, 7631, 1845, 7723)),
        ),
        _typed(
            "structure_line",
            "breakwater",
            _box_line((1845, 7631, 2035, 7723)),
        ),
    ),
    _row(
        "slipway",
        (1655, 7725, 2035, 7817),
        _typed("structure_line", "slipway", _box_line((1655, 7725, 2035, 7817))),
    ),
    _row(
        "marine_farm",
        (1655, 7818, 1860, 7910),
        _typed("structure_line", "marine_farm", _box_line((1655, 7818, 1860, 7910))),
    ),
    _row(
        "dam",
        (1655, 7920, 1780, 8015),
        ("water_line", {"type": "river"}, _box_line((1655, 7920, 1780, 8015), 8)),
        _typed("structure_line", "dam", _box_line((1655, 7920, 1780, 8015), 20)),
    ),
    _row(
        "floodgate",
        (1780, 7920, 1900, 8015),
        ("water_line", {"type": "drain"}, _box_line((1780, 7920, 1900, 8015))),
        _typed(
            "structure_point",
            "floodgate",
            _box_pt((1780, 7920, 1900, 8015)),
            orientation=0,
        ),
    ),
    _row(
        "weir",
        (1900, 7920, 2035, 8015),
        _typed("structure_line", "weir", _box_line((1900, 7920, 2035, 8015), 8)),
    ),
    _row(
        "waterfall",
        (1655, 8021, 1770, 8113),
        _typed("water_point", "waterfall", _box_pt((1655, 8021, 1770, 8113))),
    ),
    _row(
        "rapids",
        (1770, 8021, 2035, 8113),
        _typed("landcover", "rapid", _box_strip((1770, 8021, 2035, 8113))),
    ),
    _row(
        "cold_spring",
        (1655, 8115, 1840, 8207),
        _typed(
            "water_point",
            "spring",
            _box_pt((1655, 8115, 1840, 8207)),
            temperature_indicator="cold",
        ),
    ),
    _row(
        "hot_spring",
        (1840, 8115, 2035, 8207),
        _typed(
            "water_point",
            "spring",
            _box_pt((1840, 8115, 2035, 8207)),
            temperature_indicator="hot",
        ),
    ),
    _row(
        "fumarole",
        (1655, 8210, 1840, 8302),
        _typed("landcover_point", "fumarole", _box_pt((1655, 8210, 1840, 8302))),
    ),
    {
        "key": "watercourse_drain",
        "box": (1655, 8318, 2035, 8376),
        "features": (
            ("water_line", {"type": "river"}, _line(8345, 1667, 1835)),
            ("water_line", {"type": "drain"}, _line(8345, 1860, 2015)),
        ),
    },
    _row(
        "canal_large",
        (1655, 8399, 1842, 8491),
        _typed("water", "canal", _box_strip((1655, 8399, 1842, 8491))),
    ),
    _row(
        "canal_small",
        (1842, 8399, 2035, 8491),
        ("water_line", {"type": "canal"}, _box_line((1842, 8399, 2035, 8491), 8)),
    ),
    {
        "key": "vegetation",
        "box": (1655, 8736, 2035, 9216),
        "features": (
            _vegetation("native", 8736, 8831),
            _vegetation("exotic", 8831, 8926, subtype="coniferous"),
            _vegetation("exotic", 8926, 9021, subtype="non-coniferous"),
            _vegetation("scrub", 9021, 9116),
            # Marks draw only when whole inside the polygon, on a 5 mm grid
            # whose first row is about 104 px under the polygon top. The
            # polygon starts above its strip so one row lands in the strip.
            # It has no fill, so the overlap on scrub draws nothing.
            _vegetation("scattered_scrub", 9060, 9211),
        ),
    },
    {
        "key": "shelter_belt",
        "box": (1655, 9228, 2035, 9284),
        "features": (("vegetation_line", {"type": "shelter_belt"}, _line(9256)),),
    },
    {
        "key": "trees",
        "box": (1655, 9315, 2035, 9390),
        "features": (("vegetation_point", {"type": "tree"}, "POINT (1845 9352.5)"),),
        "legend_marker_size_mm": "vegetation.trees.legend_size_mm",
    },
)
