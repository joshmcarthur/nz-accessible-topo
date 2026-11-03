from nzat.qgis.parse_extent import parse_extent
from nzat.qgis.square_extent import square_extent

DPI = 600
PX = 472


def render_jobs(squares, extent=None, output=None, width=None, height=None, dpi=None):
    """Return (xmin, ymin, xmax, ymax, width, height, dpi, output) jobs."""
    if extent is not None:
        if squares:
            raise ValueError("use --square or --extent, not both")
        if output is None or width is None or height is None or dpi is None:
            raise ValueError("--extent needs --output --width --height --dpi")
        xmin, ymin, xmax, ymax = parse_extent(extent)
        return [(xmin, ymin, xmax, ymax, width, height, dpi, output)]
    if not squares:
        raise ValueError("need --square or --extent")
    return [
        (*square_extent(east, north), PX, PX, DPI, path)
        for east, north, path in squares
    ]
