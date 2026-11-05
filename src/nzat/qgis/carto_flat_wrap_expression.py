from nzat.qgis.defaults import STYLE


def carto_flat_wrap_expression(style=None):
    """Wrap a long single name. A dual name breaks after its slash. A name with its own break keeps it."""
    chars = (style or STYLE)["labels"]["carto_point"]["wrap_chars"]
    return (
        f"CASE WHEN strpos(\"text_string\", ' / ') = 0"
        f" AND strpos(\"text_string\", '\\n') = 0"
        f' AND length("text_string") > {chars}'
        f" THEN {chars} ELSE 0 END"
    )
