from nzat.colour.parse_colour import parse_colour
from nzat.style.fmt import fmt


def vegetation_fill(kind, rules):
    """Return the opaque vector fill for a vegetation class."""
    colour = rules["vegetation"][kind]["colour"]
    return fmt(parse_colour(colour)[:3])
