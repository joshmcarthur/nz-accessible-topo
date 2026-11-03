from nzat.paths import STYLE_PATH as STYLE_PATH_OBJ
from nzat.style.load_rules import load_rules

STYLE_PATH = str(STYLE_PATH_OBJ)
STYLE = load_rules()
FAMILY = STYLE["fonts"]["raster_family"]
DEM_LAYER_NAME = "dem"
DEM_LAYER_ID = "dem_hillshade"
CARTO_TEXT_LAYER = "nztopo50_carto_text"
WRAP_TURN_DEG = 90
WRAP_HEADING_DEG = 45
SHEET_SCALE = 50000
WHITE = (255, 255, 255)
PMS151_RGB = (255, 127, 0)
CARTO_FIT_FILE = "carto_fit.json"
CARTO_POINT_FILTER = (
    '"text_placement" = 1 AND "text_orientation" = 0'
    " AND strpos(coalesce(\"text_string\", ''), '\\n') = 0"
    " AND num_points($geometry) <= 2"
)
CURVED_ONLY_PROPERTIES = (
    "LinePlacementFlags",
    "LineAnchorPercent",
    "LineAnchorTextPoint",
    "CurvedLabelMode",
)
ABOVE_BELOW_MAP_ORIENTED = 2 | 4 | 8
MULTILINE_CENTRE = "1"
CARTO_FLAT_TEXT = (
    "regexp_replace(replace(\"text_string\", ' / ', ' /\\n'), '^Te ', 'Te\u00a0')"
)
