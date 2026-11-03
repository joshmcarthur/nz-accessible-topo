from nzat.qgis.map_layers import SHEET_PRESET
from nzat.qgis.sheet_layer_ids import sheet_layer_ids


def test_square_uses_the_sheet_layer_set():
    # Catches a square that draws landcover_line. The sheet map hides that layer.
    ordered = [
        "contour_id",
        "landcover_line_id",
        "building_point_id",
        "building_point_map_id",
    ]
    visible = ["contour_id", "building_point_map_id"]
    assert SHEET_PRESET == "Map5View"
    assert sheet_layer_ids(ordered, visible) == ["contour_id", "building_point_map_id"]
