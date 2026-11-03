from nzat.qgis.render_square_main import DPI, PX
from nzat.qgis.square_extent import METRES, square_extent


def test_square_extent_is_one_kilometre():
    # Catches a square that is not 1000 m on a side, or a pixel size other than the 600 dpi sheet size.
    assert METRES == 1000
    assert DPI == 600
    assert PX == 472
    assert square_extent(1577000, 5178000) == (1577000, 5178000, 1578000, 5179000)
