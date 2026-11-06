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
    {
        "key": "watercourse_drain",
        "box": (1655, 8318, 2035, 8376),
        "features": (
            ("water_line", {"type": "river"}, _line(8345, 1667, 1835)),
            ("water_line", {"type": "drain"}, _line(8345, 1860, 2015)),
        ),
    },
    {
        "key": "vegetation",
        "box": (1655, 8728, 2035, 9216),
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
