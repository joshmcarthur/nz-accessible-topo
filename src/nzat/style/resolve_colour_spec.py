from nzat.colour.parse_colour import parse_colour
from nzat.style.format_rgba import format_rgba
from nzat.style.is_style_path import is_style_path
from nzat.style.lookup_style_path import lookup_style_path


def resolve_colour_spec(side, rules):
    """Return a colour string. A dotted path is read from the shared config."""
    colour = side["colour"]
    if is_style_path(colour):
        colour = lookup_style_path(rules, colour)
        if not isinstance(colour, str):
            raise TypeError(side["colour"])
    alpha = side.get("alpha")
    if alpha is None:
        return colour
    if is_style_path(alpha):
        alpha = lookup_style_path(rules, alpha)
    parsed = parse_colour(colour)
    if parsed is None:
        raise ValueError(colour)
    return format_rgba(parsed, alpha)
