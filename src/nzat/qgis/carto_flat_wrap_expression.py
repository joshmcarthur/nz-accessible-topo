from nzat.qgis.defaults import STYLE


def carto_flat_wrap_expression(style=None):
    """Wrap a long single name; a dual name already breaks after its slash."""
    chars = (style or STYLE)["labels"]["carto_point"]["wrap_chars"]
    return (
        f'CASE WHEN strpos("text_string", \' / \') = 0 AND length("text_string") > {chars}'
        f" THEN {chars} ELSE 0 END"
    )
