from nzat.qgis.defaults import FAMILY, STYLE, STYLE_PATH
from nzat.qgis.size_floor import size_floor


def test_style_file_has_no_sheet_code():
    # Catches a sheet code in the style file, or a settled ink the apply step no longer reads.
    with open(STYLE_PATH, encoding="utf-8") as handle:
        raw = handle.read()
    for token in (
        "BX24",
        "1577000",
        "5178000",
        "5172000",
        "1569000",
        "5165000",
        "1584000",
        "5173000",
    ):
        assert token not in raw, token
    style = STYLE
    assert style["fonts"]["raster_family"] == "Atkinson Hyperlegible Next Macron"
    assert style["fonts"]["vector_family"] == "Open Sans"
    assert style["fonts"]["stock_family"] == "Nimbus Sans LINZ"
    assert style["contours"]["index"]["colour"] == "#7A5542"
    assert style["contours"]["index"]["width_mm"] == 0.35
    assert style["contours"]["index"]["alpha"] == 0.85
    assert style["contours"]["intermediate"]["colour"] == "#B08872"
    assert style["contours"]["intermediate"]["casing_colour"] == "#7A5542"
    assert style["contours"]["intermediate"]["casing_width_mm"] == 0.2
    assert style["contours"]["intermediate"]["alpha"] == 0.5
    assert style["reference_inks"]["project_road"] == "#EC7000"
    assert style["reference_inks"]["project_highway"] == "#E31A1C"
    assert style["reference_inks"]["project_road_casing"] == "#232323"
    assert style["reference_inks"]["water_fill"] == "#D1E7F5"
    assert style["reference_inks"]["print_legend_highway"] == "#EA6300"
    assert style["reference_inks"]["stream"] == "#00276D"
    assert style["map"]["theme_paper"] == "Map5View-paper"
    assert style["map"]["theme_all"] == "Map5View-all"
    assert style["sizes"]["navigation_line_mm"] == 0.35
    assert style["sizes"]["line_floor_mm"] == 0.15
    assert style["water"]["stream_width_mm"] == 0.35
    assert style["water"]["drain_width_mm"] < style["water"]["stream_width_mm"]
    assert style["vegetation"]["scrub_dots"]["marker"] == "third_arc"
    assert style["vegetation"]["scrub_dots"]["distance_mm"] == 3
    assert style["vegetation"]["scrub_dots"]["size_mm"] == 1.4
    assert style["vegetation"]["scrub_dots"]["colour"] == "#6A9A50"
    assert style["vegetation"]["scrub_dots"]["stroke_mm"] > 0
    assert style["reference_inks"]["shelterbelt"] == "#008A00"
    assert style["reference_inks"]["grid"] == "#269FD2"
    assert style["reference_inks"]["urban_fill"] == "#BCBAB6"
    assert style["reference_inks"]["island_outline"] == "#0083BB"
    assert style["reference_inks"]["vegetation_outline"] == "#859E3E"
    assert style["vegetation"]["scattered"]["distance_mm"] == 5
    assert style["vegetation"]["trees"]["marker"] == "./symbol/nztopo50_tree_stroke.svg"
    assert style["vegetation"]["trees"]["size_mm"] == 0.2
    assert style["vegetation"]["trees"]["legend_size_mm"] == 1.4
    assert style["vegetation"]["exotic"]["colour"] == "#A4D65E"
    assert style["vegetation"]["exotic"]["alpha"] == 0.2
    assert style["fonts"]["raster_natural_style"] == "Regular"
    assert FAMILY == style["fonts"]["raster_family"]
    assert size_floor("contour", "1") == str(int(style["labels"]["size_floor_pt"]))
    assert size_floor("relief_point map", "1") == str(
        int(style["labels"]["spot_height_floor_pt"])
    )
    assert style["labels"]["web_floor_px"] == 10
    assert style["labels"]["place_name_floor_px"] == 11
    assert style["labels"]["letter_spacing_em"] == 0.05
    assert style["vegetation"]["native"]["marker"]["colour"] == "#3F6B32"
    assert style["vegetation"]["scrub"]["colour"] == "#A3CC90"
    assert style["vegetation"]["scrub"]["alpha"] == 26
    assert style["tracks"]["closed_foot"]["marker"] == "cross2"
    assert style["tracks"]["closed_foot"]["crossbar_angle_deg"] == 0
    assert style["tracks"]["closed_foot"]["crossbar_size_mm"] == 1.25
    assert style["tracks"]["closed_foot"]["marker_interval_mm"] == 3
    assert style["vegetation"]["scattered"]["colour"] == "#E0EDD8"
    assert style["tracks"]["closed_foot"]["casing_colour"] == "#1A1A1A"
    assert style["structures"]["locked_gate"]["bar_colour"] == "#000000"
    assert style["structures"]["locked_gate"]["lock_size_mm"] == 0.6
    assert style["structures"]["bivouac"]["marker"] == "./symbol/nztopo50_bivouac.svg"
    assert style["structures"]["bivouac"]["size_mm"] == 1.4
    assert style["structures"]["bivouac"]["stroke_mm"] == 0.15
    assert style["structures"]["church"]["marker"] == "./symbol/nztopo50_church.svg"
    assert style["structures"]["church"]["bar_stroke_mm"] == 0.15
    assert (
        style["structures"]["shipwreck"]["marker"] == "./symbol/nztopo50_wreck_ship.svg"
    )
    assert style["structures"]["tower"]["stroke_mm"] == 0.15
    assert style["structures"]["redoubt"]["size_mm"] == 2.5
    assert style["structures"]["mast"]["marker"] == "./symbol/nztopo50_mast.svg"
    assert (
        style["structures"]["beacon"]["marker"] == "./symbol/nztopo50_marine_beacon.svg"
    )
    assert style["structures"]["buried_gas_pipeline"]["colour"] == "#951600"
    assert style["structures"]["buried_gas_pipeline"]["dash"] == "2;0.5"
    assert style["tracks"]["access"]["reserved_channel"] == "casing_colour"
    assert style["tracks"]["access"]["painted"] is False
    assert style["draw_order"] == [{"name": "vegetation map", "below": "contour"}]
    assert style["label_contrast"]["red_light_min"] == 3.0
