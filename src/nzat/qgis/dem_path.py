import os

from nzat.qgis.hillshade_rules import hillshade_rules


def dem_path(project_dir, style=None):
    """Return the DEM path beside the project."""
    return os.path.join(project_dir, hillshade_rules(style)["raster_file"])
