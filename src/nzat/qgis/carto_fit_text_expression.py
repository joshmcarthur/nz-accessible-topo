from nzat.qgis.carto_fit_value import carto_fit_value
from nzat.qgis.defaults import CARTO_CLEAN_TEXT, CARTO_FLAT_TEXT


def carto_fit_text_expression(fit):
    """A row fitted to one line drops the slash break."""
    one_line = f"replace({CARTO_CLEAN_TEXT}, '\\n', ' ')"
    return f'CASE WHEN {carto_fit_value(fit, "lines")} = 1 THEN {one_line} ELSE {CARTO_FLAT_TEXT} END'
