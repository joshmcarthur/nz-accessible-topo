from nzat.qgis.carto_fit_value import carto_fit_value
from nzat.qgis.defaults import CARTO_FLAT_TEXT


def carto_fit_text_expression(fit):
    """A row fitted to one line drops the slash break."""
    return f'CASE WHEN {carto_fit_value(fit, "lines")} = 1 THEN "text_string" ELSE {CARTO_FLAT_TEXT} END'
