from nzat.qgis.cover_set import (
    BBOX_AREA,
    IN_SITU_M,
    cell_origin,
    extra_square_jobs,
    greedy_cells,
    in_extent,
    in_situ_extent,
    in_situ_jobs,
    map_paint_note,
    map_png_name,
    paints_on_map_all,
    split_base_hits,
)
from nzat.qgis.sample_grid import BX24_EXTENT
from nzat.qgis.symbol_queries import missing_symbol_keys


def test_every_legend_row_has_a_query():
    # Catches a new /symbols/ key that never got a parquet predicate.
    missing, extra = missing_symbol_keys()
    assert missing == []
    assert extra == []


def test_cell_origin_snaps_to_four_km():
    # Catches a cell that is not the south-west 4000 m corner used by crop_grid.
    assert cell_origin(1571683, 5172106) == (1568000, 5170000)
    assert cell_origin(1564000, 5154000) == (1564000, 5154000)


def test_bx24_extent_contains_sugarloaf():
    assert in_extent(1571683, 5172106, BX24_EXTENT)
    assert not in_extent(1200000, 4800000, BX24_EXTENT)


def test_split_keeps_bx24_keys_off_the_extra_list():
    # Catches a cover set that re-asks for a class BX24 already holds.
    hits = [
        {"key": "mast", "x": 1571683, "y": 5172106},
        {"key": "fumarole", "x": 1880000, "y": 5712000},
        {"key": "mast", "x": 1880000, "y": 5712000},
    ]
    base, extra = split_base_hits(hits)
    assert base == ["mast"]
    assert [hit["key"] for hit in extra] == ["fumarole"]


def test_greedy_cells_merge_keys_in_one_square():
    # Catches one square per key when two hits share a 4 km cell.
    hits = [
        {"key": "ford", "x": 1200100, "y": 4800100},
        {"key": "helipad", "x": 1200200, "y": 4800200},
        {"key": "walkwire", "x": 1600100, "y": 5300100},
    ]
    cells, leftover = greedy_cells(hits)
    assert leftover == []
    assert len(cells) == 2
    first = max(cells, key=lambda cell: len(cell["keys"]))
    assert first["keys"] == ["ford", "helipad"]
    assert first["east"] == 1200000
    assert first["north"] == 4798000


def test_in_situ_extent_is_centred_on_the_hit():
    # Catches a 1 km crop whose south-west corner is the hit, so the mark sits on the edge.
    xmin, ymin, xmax, ymax = in_situ_extent(1821234, 5506789)
    assert xmax - xmin == IN_SITU_M
    assert ymax - ymin == IN_SITU_M
    assert (xmin + xmax) / 2 == 1821234
    assert (ymin + ymax) / 2 == 5506789
    assert map_png_name("bivouac") == "bivouac-map.png"


def test_in_situ_jobs_skip_absent_keys():
    # Catches a crop job for a class with no parquet hit.
    hits = [
        {"key": "bivouac", "x": 1821234, "y": 5506789, "parquet": "structure_point"},
        {"key": "helipad", "x": 1, "y": 2, "parquet": "transport_point"},
        {"key": "grave", "x": 3, "y": 4, "parquet": "place_point"},
    ]
    jobs = in_situ_jobs(hits, "/tmp/symbols")
    assert len(jobs) == 1
    assert jobs[0]["output"].endswith("bivouac-map.png")
    assert jobs[0]["extent"] == in_situ_extent(1821234, 5506789)
    assert not paints_on_map_all("transport_point")
    assert map_paint_note(None) == "No national type"
    assert "ORDER" not in BBOX_AREA
    assert "bbox.xmax" in BBOX_AREA
    squares = extra_square_jobs(
        [{"east": 1820000, "north": 5506000, "extent": [1, 2, 3, 4]}],
        "/tmp/cover",
    )
    assert squares[0]["output"].endswith("1820000-5506000-accessible.png")
