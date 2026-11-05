from nzat.qgis.defaults import SHEET_SCALE

MM_PER_INCH = 25.4


def legend_metres_per_px(dpi, scale=SHEET_SCALE):
    """Return ground metres per legend pixel, so a swatch draws at sheet size."""
    return MM_PER_INCH / dpi / 1000 * scale
