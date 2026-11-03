from nzat.qgis.carto_text_width_expression import carto_text_width_expression


def curved_label_mode_expression(style=None):
    """Keep the stock stretch only where it adds space. A baseline shorter than the name would squeeze it."""
    width = carto_text_width_expression('length("text_string")', style)
    return (
        "CASE WHEN \"charplace\" IN ('StretchWordSpacingToFit', 'StretchCharacterSpacingToFit')"
        f" AND (strpos(\"text_string\", '\\n') > 0 OR length($geometry) <= {width})"
        " THEN 'default' ELSE \"charplace\" END"
    )
