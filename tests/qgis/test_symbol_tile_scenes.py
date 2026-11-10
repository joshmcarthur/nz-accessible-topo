from nzat.qgis.legend_swatches import SWATCHES
from nzat.qgis.symbol_tile_scenes import (
    BACKGROUNDS,
    CONFLICTS,
    TILE_PX,
    tile_box,
    tile_scenes,
)


def _swatch(key):
    return next(s for s in SWATCHES if s["key"] == key)


def test_tile_is_a_10_mm_square_on_the_swatch_centre():
    x0, y0, x1, y1 = tile_box((1655, 737, 2035, 825))
    assert (x1 - x0, y1 - y0) == (TILE_PX, TILE_PX)
    assert ((x0 + x1) / 2, (y0 + y1) / 2) == (1845, 781)


def test_line_symbol_gets_every_fill_and_every_conflict():
    scenes = tile_scenes(_swatch("foot_track"))
    assert [name for name, _ in scenes] == [*BACKGROUNDS, *CONFLICTS]
    for name, features in scenes:
        # The symbol sample is in every scene.
        assert any(table == "track_line" for table, _attrs, _wkt in features), name


def test_fill_sample_has_the_class_attributes():
    scenes = dict(tile_scenes(_swatch("foot_track")))
    assert scenes["scrub"][0][0] == "vegetation"
    assert scenes["scrub"][0][1] == {"type": "scrub"}


def test_area_symbol_skips_the_fills_under_it():
    names = [name for name, _ in tile_scenes(_swatch("swamp"))]
    assert names == ["paper", *CONFLICTS]
