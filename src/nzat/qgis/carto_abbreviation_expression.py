from nzat.qgis.carto_text_width_expression import carto_text_width_expression
from nzat.qgis.defaults import STYLE


def carto_abbreviation_expression(style=None):
    """Abbreviate a road suffix only when the larger type overruns the stock baseline.

    Topo50 already uses RD, ST and AVE where a name is tight. Other names keep their text.
    """
    style = style or STYLE
    text = '"text_string"'
    for word, short in style["labels"]["road_abbreviations"].items():
        text = f"regexp_replace({text}, ' {word}$', ' {short}')"
    width = carto_text_width_expression('length("text_string")', style)
    return (
        f"CASE WHEN length($geometry) < {width} THEN {text}"
        ' ELSE "text_string" END'
    )
