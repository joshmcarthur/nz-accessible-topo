def format_rgba(rgb, alpha):
    """Return an rgba() string. Alpha comes from the style file."""
    r, g, b = (int(round(v)) for v in rgb[:3])
    return f"rgba({r}, {g}, {b}, {alpha:g})"
