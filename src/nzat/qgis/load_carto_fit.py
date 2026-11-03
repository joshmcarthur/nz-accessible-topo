import json
import os

from nzat.qgis.defaults import CARTO_FIT_FILE


def load_carto_fit(project_dir):
    """Return fitted flat names by row id from carto_fit.json beside the project, or {} when absent."""
    if not project_dir:
        return {}
    path = os.path.join(project_dir, CARTO_FIT_FILE)
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
