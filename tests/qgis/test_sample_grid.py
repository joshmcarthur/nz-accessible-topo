import os
import tempfile

from PIL import Image

from nzat.qgis.crop_face import crop_face
from nzat.qgis.parse_extent import parse_extent
from nzat.qgis.render_jobs import DPI, PX, render_jobs
from nzat.qgis.sample_grid import (
    BX24_EXTENT,
    CELL_M,
    CELL_PX,
    PHASE,
    chequerboard,
    crop_box,
    crop_name,
    face_pixels,
    grid_cells,
    grid_shape,
)


def test_bx24_chequerboard_has_twenty_seven_cells():
    # Catches a 4 km grid that is not 6 by 9, or a phase that drops the south-west cell.
    cols, rows = grid_shape(BX24_EXTENT, CELL_M)
    assert (cols, rows) == (6, 9)
    cells = grid_cells(BX24_EXTENT, CELL_M)
    assert len(cells) == 54
    kept = chequerboard(cells, PHASE)
    assert len(kept) == 27
    assert kept[0] == (0, 0, 1564000.0, 5154000.0)
    assert (1, 0, 1568000.0, 5154000.0) not in kept
    assert crop_name(1564000, 5154000, "stock") == "1564000-5154000-stock.png"


def test_crop_box_puts_north_at_the_top():
    # Catches an origin that treats row 0 as the north edge.
    cols, rows = grid_shape(BX24_EXTENT, CELL_M)
    assert face_pixels(cols, rows, CELL_PX) == (5670, 8505)
    assert crop_box(0, 0, CELL_PX, rows) == (0, 8505 - 945, 945, 8505)
    assert crop_box(0, 8, CELL_PX, rows) == (0, 0, 945, 945)


def test_crop_face_reads_the_matching_cell():
    # Catches a crop that takes the neighbour cell or flips north and south.
    cols, rows = 2, 2
    cell_px = 4
    width, height = face_pixels(cols, rows, cell_px)
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    colours = {
        (0, 0): (10, 20, 30),
        (1, 0): (40, 50, 60),
        (0, 1): (70, 80, 90),
        (1, 1): (100, 110, 120),
    }
    for col, row, colour in (
        (col, row, colours[(col, row)]) for col in range(cols) for row in range(rows)
    ):
        left, top, right, bottom = crop_box(col, row, cell_px, rows)
        for x in range(left, right):
            for y in range(top, bottom):
                pixels[x, y] = colour
    cells = [(0, 0, 1000, 2000), (1, 1, 3000, 4000)]
    with tempfile.TemporaryDirectory() as out_dir:
        paths = crop_face(image, cells, cell_px, cols, rows, "stock", out_dir)
        assert [os.path.basename(path) for path in paths] == [
            "1000-2000-stock.png",
            "3000-4000-stock.png",
        ]
        south_west = Image.open(paths[0])
        north_east = Image.open(paths[1])
        assert south_west.getpixel((0, 0)) == (10, 20, 30)
        assert north_east.getpixel((0, 0)) == (100, 110, 120)


def test_crop_face_rejects_a_wrong_size():
    # Catches a crop from a 150 dpi face, or a pad, without a size check.
    image = Image.new("RGB", (10, 10))
    try:
        crop_face(image, [], 945, 6, 9, "stock", ".")
    except ValueError as error:
        assert "expected 5670 by 8505" in str(error)
    else:
        raise AssertionError("wrong-size face must stop")


def test_render_jobs_keep_one_kilometre_squares():
    # Catches an extent path that changes the 1 km 600 dpi square size.
    jobs = render_jobs([(1577000, 5178000, "out.png")])
    assert jobs == [(1577000, 5178000, 1578000, 5179000, PX, PX, DPI, "out.png")]


def test_render_jobs_accept_one_rectangle():
    # Catches a face job that still uses the 1 km square size.
    jobs = render_jobs(
        [],
        extent="1564000,5154000,1588000,5190000",
        output="face.png",
        width=5670,
        height=8505,
        dpi=300,
    )
    assert jobs == [
        (1564000.0, 5154000.0, 1588000.0, 5190000.0, 5670, 8505, 300, "face.png")
    ]


def test_parse_extent_rejects_a_short_string():
    try:
        parse_extent("1,2,3")
    except ValueError as error:
        assert "xmin,ymin,xmax,ymax" in str(error)
    else:
        raise AssertionError("short extent must stop")
