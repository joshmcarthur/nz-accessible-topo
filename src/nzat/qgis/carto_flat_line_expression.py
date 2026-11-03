from nzat.qgis.carto_text_width_expression import carto_text_width_expression
from nzat.qgis.defaults import CARTO_FLAT_TEXT, SHEET_SCALE, STYLE


def carto_flat_line_expression(style=None):
    """Horizontal line at the stock baseline, centred on the stock label.

    It is the estimated width of the longest label line plus the allowance at each end.
    @map_scale is null in a label geometry generator, so the sheet scale is fixed.
    """
    style = style or STYLE
    allowance = style["labels"]["carto_point"]["allowance_mm"] * SHEET_SCALE / 1000
    longest = f"array_max(array_foreach(string_to_array({CARTO_FLAT_TEXT}, '\\n'), length(@element)))"
    half = f"({carto_text_width_expression(longest, style)} / 2 + {allowance:g})"
    return (
        "with_variable('cx', x(centroid(bounds(@geometry))), with_variable('y', y_min(@geometry), "
        f"make_line(make_point(@cx - {half}, @y), make_point(@cx + {half}, @y))))"
    )
