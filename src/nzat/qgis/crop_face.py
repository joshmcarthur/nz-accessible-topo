import os

from nzat.qgis.sample_grid import crop_box, crop_name, face_pixels


def crop_face(image, cells, cell_px, cols, rows, variant, out_dir):
    """Write one PNG per cell. Stop if the face size does not match the grid."""
    expected = face_pixels(cols, rows, cell_px)
    if image.size != expected:
        raise ValueError(
            f"face is {image.size[0]} by {image.size[1]}, expected {expected[0]} by {expected[1]}"
        )
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for col, row, east, north in cells:
        path = os.path.join(out_dir, crop_name(east, north, variant))
        image.crop(crop_box(col, row, cell_px, rows)).save(path)
        written.append(path)
    return written
