from nzat.render.make_tiles import tile_commands


def test_commands_mosaic_then_tile_then_overviews_then_pmtiles():
    commands = tile_commands(["a.tif", "b.tif"], "out.pmtiles", "/work")
    assert [command[0] for command in commands] == [
        "gdalbuildvrt",
        "gdal_translate",
        "gdaladdo",
        "pmtiles",
    ]
    assert commands[0][-2:] == ["a.tif", "b.tif"]
    assert commands[-1][-1] == "out.pmtiles"
    assert "-projwin" not in commands[1]


def test_extent_becomes_a_projwin_with_north_before_south():
    # Catches an empty crop: gdal wants upper-left then lower-right.
    commands = tile_commands(["a.tif"], "out.pmtiles", "/work", (1, 2, 3, 4))
    at = commands[1].index("-projwin")
    assert commands[1][at + 1 : at + 5] == ["1", "4", "3", "2"]
