def _mm(value):
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def closed_bar_placement(track):
    """Return the interval and the offset that put one bar in each dash gap."""
    on_text, off_text = track["closed_dash"].split(";")
    on = float(on_text)
    off = float(off_text)
    return _mm(on + off), _mm(on + off / 2)
