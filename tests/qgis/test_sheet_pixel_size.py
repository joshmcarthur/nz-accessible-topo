from nzat.qgis.sheet_file_name import sheet_file_name
from nzat.qgis.sheet_geotransform import sheet_geotransform
from nzat.qgis.sheet_pixel_size import sheet_pixel_size

BX24 = (1564000, 5154000, 1588000, 5190000)


def test_sheet_pixel_size_is_the_printed_face_at_the_dpi():
    # Catches a wrong mm-to-pixel step: BX24 is 480 x 720 mm at 1:50,000.
    assert sheet_pixel_size(*BX24, 150) == (2835, 4252)
    assert sheet_pixel_size(*BX24, 300) == (5669, 8504)


def test_sheet_geotransform_is_north_up_from_the_top_left():
    # Catches a raster that is flipped or anchored at the south-west corner.
    x0, dx, rx, y0, ry, dy = sheet_geotransform(*BX24, 2835, 4252)
    assert (x0, y0, rx, ry) == (1564000, 5190000, 0.0, 0.0)
    assert dx * 2835 == 24000
    assert round(dy * 4252, 6) == -36000


def test_sheet_file_name_has_no_path_separator():
    # Catches "AS21/AS22" writing into a missing AS21 folder and failing.
    assert sheet_file_name("BX24") == "BX24.tif"
    assert sheet_file_name("AS21/AS22") == "AS21_AS22.tif"
    assert sheet_file_name("BJ43ptsBJ42,BH42,BH43") == "BJ43ptsBJ42_BH42_BH43.tif"
