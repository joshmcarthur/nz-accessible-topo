from nzat.colour.composite import composite
from nzat.colour.darken import darken_for_text
from nzat.qgis.parse_qgis_colour import parse_qgis_colour
from nzat.qgis.rgb_key import rgb_key


def colour_expression(palette, behind, min_ratio, red_min=None):
    """Map a named project colour that fails the floor to a darker ink."""
    clauses = []
    for name, colour_text in palette:
        if not name:
            continue
        parsed = parse_qgis_colour(colour_text)
        if parsed is None:
            continue
        red, green, blue, alpha = parsed
        fg = composite((red, green, blue, alpha / 255.0), behind)
        new = darken_for_text(fg, behind, min_ratio, red_min)
        if rgb_key(new) == rgb_key(fg):
            continue
        nr, ng, nb = rgb_key(new)
        clauses.append(f"WHEN \"colour\" = '{name}' THEN color_rgb({nr},{ng},{nb})")
    if not clauses:
        return None
    return "CASE " + " ".join(clauses) + ' ELSE project_color_object("colour") END'
