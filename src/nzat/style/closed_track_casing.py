from nzat.colour.parse_colour import parse_colour
from nzat.style.fmt import fmt


def closed_track_casing(rules):
    """Return the vector closed-track casing."""
    track = rules["tracks"]["closed_foot"]
    colour = parse_colour(track["casing_colour"])[:3]
    return fmt(colour, track["casing_alpha"])
