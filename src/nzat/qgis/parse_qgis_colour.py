def parse_qgis_colour(text):
    """Return (r, g, b, a) with alpha 0–255. Return None when text is not a colour."""
    if not text:
        return None
    parts = text.split(",")
    if len(parts) < 3:
        return None
    try:
        red, green, blue = (
            int(float(parts[0])),
            int(float(parts[1])),
            int(float(parts[2])),
        )
        alpha = int(float(parts[3])) if len(parts) >= 4 else 255
    except ValueError:
        return None
    return (red, green, blue, alpha)
