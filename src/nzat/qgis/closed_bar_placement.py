def _mm(value):
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def closed_bar_placement(track):
    """Return the marker interval and the offset that sits the first mark in a dash gap."""
    on_text, off_text = track["closed_dash"].split(";")
    on = float(on_text)
    off = float(off_text)
    cycle = on + off
    interval = float(track.get("marker_interval_mm", cycle))
    return _mm(interval), _mm(on + off / 2)
