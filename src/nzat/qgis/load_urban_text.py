import json
import os

from nzat.qgis.defaults import URBAN_TEXT_FILE


def load_urban_text(project_dir):
    """Return carto_text row ids inside the urban fill from urban_text.json beside the project, or [] when absent."""
    if not project_dir:
        return []
    path = os.path.join(project_dir, URBAN_TEXT_FILE)
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
