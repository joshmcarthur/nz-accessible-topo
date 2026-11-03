from nzat.qgis.defaults import SHEET_SCALE, STYLE


def carto_text_width_expression(chars, style=None):
    """Estimated width in metres of a carto_text line of chars characters at the sheet scale."""
    style = style or STYLE
    floor = style["labels"]["size_floor_pt"]
    metres_per_pt = 0.3528 / 1000 * SHEET_SCALE
    return (
        f'({chars} * max({floor}, coalesce("size", {floor}))'
        f" * {style['labels']['carto_point']['advance_em']} * {metres_per_pt:g})"
    )
