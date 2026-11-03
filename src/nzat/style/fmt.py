def fmt(rgb, a=1.0):
    r, g, b = (int(round(max(0, min(255, v)))) for v in rgb)
    return f"rgba({r}, {g}, {b}, {a:g})"
