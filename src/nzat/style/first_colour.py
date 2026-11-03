from nzat.colour.parse_colour import parse_colour


def first_colour(paint, keys):
    for k in keys:
        v = paint.get(k)
        c = parse_colour(v) if isinstance(v, str) else None
        if c:
            return c
    return None
