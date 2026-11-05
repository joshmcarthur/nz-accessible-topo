import re

_PAIR = re.compile(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)")


def legend_wkt(wkt, metres_per_px):
    """Turn WKT in legend pixels (y down) into ground metres (y up)."""

    def _scale(match):
        x = float(match.group(1)) * metres_per_px
        y = -float(match.group(2)) * metres_per_px
        return f"{x:.4f} {y:.4f}"

    return _PAIR.sub(_scale, wkt)
