BX24_EXTENT = (1564000.0, 5154000.0, 1588000.0, 5190000.0)
CELL_M = 4000
CELL_PX = 945
PHASE = 0


def grid_shape(extent, cell_m):
    """Return column and row counts. The extent must divide by cell_m."""
    xmin, ymin, xmax, ymax = extent
    width_m = xmax - xmin
    height_m = ymax - ymin
    cols, rem_x = divmod(width_m, cell_m)
    rows, rem_y = divmod(height_m, cell_m)
    if rem_x or rem_y:
        raise ValueError(
            f"extent {width_m} by {height_m} m does not divide by {cell_m} m"
        )
    return int(cols), int(rows)


def face_pixels(cols, rows, cell_px):
    """Return the face width and height in pixels so cells tile with no leftover."""
    return cols * cell_px, rows * cell_px


def grid_cells(extent, cell_m):
    """Return (col, row, east, north) for each cell. Row 0 is the south edge."""
    xmin, ymin, _, _ = extent
    cols, rows = grid_shape(extent, cell_m)
    return [
        (col, row, xmin + col * cell_m, ymin + row * cell_m)
        for row in range(rows)
        for col in range(cols)
    ]


def chequerboard(cells, phase=PHASE):
    """Keep cells whose column plus row matches phase. Phase 0 includes the south-west cell."""
    return [cell for cell in cells if (cell[0] + cell[1]) % 2 == phase]


def crop_box(col, row, cell_px, rows):
    """Return a Pillow crop box. Image row 0 is the north edge."""
    left = col * cell_px
    top = (rows - 1 - row) * cell_px
    return left, top, left + cell_px, top + cell_px


def crop_name(east, north, variant):
    """Return a PNG name from the south-west NZTM corner and the style variant."""
    return f"{int(east)}-{int(north)}-{variant}.png"
