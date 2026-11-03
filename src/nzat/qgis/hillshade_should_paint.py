import os

from nzat.qgis.dem_path import dem_path
from nzat.qgis.hillshade_rules import hillshade_rules


def hillshade_should_paint(project_dir, style=None):
    """Return whether raster hillshade should turn on."""
    if not project_dir:
        return False
    if not hillshade_rules(style)["painted"]:
        return False
    return os.path.isfile(dem_path(project_dir, style))
