from nzat.qgis.with_dem_layer import with_dem_layer


def test_with_dem_layer_puts_the_dem_under_the_map():
    assert with_dem_layer(["a", "b"], None) == ["a", "b"]
    assert with_dem_layer(["a", "b"], "dem") == ["dem", "a", "b"]
    assert with_dem_layer(["dem", "a"], "dem") == ["dem", "a"]
