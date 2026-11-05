from nzat.qgis.defaults import SHEET_SCALE

MM_PER_INCH = 25.4


def sheet_pixel_size(xmin, ymin, xmax, ymax, dpi, scale=SHEET_SCALE):
    """Return (width, height) in pixels for an NZTM box printed at 1:scale and dpi."""
    width_mm = (xmax - xmin) * 1000 / scale
    height_mm = (ymax - ymin) * 1000 / scale
    return round(width_mm / MM_PER_INCH * dpi), round(height_mm / MM_PER_INCH * dpi)
