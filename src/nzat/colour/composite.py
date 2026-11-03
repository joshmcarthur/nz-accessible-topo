def composite(fg, bg):
    """Alpha-composite fg (r,g,b,a) over opaque bg (r,g,b[,a]) -> opaque (r,g,b)."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))
