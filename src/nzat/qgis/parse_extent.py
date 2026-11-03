def parse_extent(text):
    """Return xmin, ymin, xmax, ymax from a comma-separated string."""
    parts = text.split(",")
    if len(parts) != 4:
        raise ValueError("extent must be xmin,ymin,xmax,ymax")
    xmin, ymin, xmax, ymax = (float(part) for part in parts)
    if xmax <= xmin or ymax <= ymin:
        raise ValueError("extent must have xmax > xmin and ymax > ymin")
    return xmin, ymin, xmax, ymax
