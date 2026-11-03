METRES = 1000


def square_extent(east, north, metres=METRES):
    """Return xmin, ymin, xmax, ymax for a square whose south-west corner is given."""
    return (east, north, east + metres, north + metres)
