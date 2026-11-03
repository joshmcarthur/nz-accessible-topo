from nzat.colour.parse_colour import parse_colour
from nzat.style.fmt import fmt


def spring_colour(kind, rules):
    """Return the spring ink."""
    colour = rules["springs"][kind]["colour"]
    return fmt(parse_colour(colour)[:3])
