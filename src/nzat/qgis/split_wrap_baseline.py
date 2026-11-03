import math

from nzat.qgis.defaults import WRAP_HEADING_DEG, WRAP_TURN_DEG


def _heading(start, end):
    return math.degrees(math.atan2(end[0] - start[0], end[1] - start[1]))


def _heading_delta(left, right):
    delta = abs(left - right) % 360
    return min(delta, 360 - delta)


def _turn_deg(before, corner, after):
    ax = corner[0] - before[0]
    ay = corner[1] - before[1]
    bx = after[0] - corner[0]
    by = after[1] - corner[1]
    if math.hypot(ax, ay) < 1 or math.hypot(bx, by) < 1:
        return 0.0
    return abs(math.degrees(math.atan2(ax * by - ay * bx, ax * bx + ay * by)))


def split_wrap_baseline(points, line_count):
    """Return one polyline per text line for a folded multiline baseline.

    A turn sharper than 90 degrees starts a new pass. Passes within 45
    degrees of the first pass are the forward baselines. When there are
    at least line_count of those, the first line_count are returned.
    Otherwise every pass is returned. A one-line label is not split.
    """
    if line_count <= 1 or len(points) < 3:
        return [list(points)]
    cuts = [0]
    for index in range(1, len(points) - 1):
        if (
            _turn_deg(points[index - 1], points[index], points[index + 1])
            > WRAP_TURN_DEG
        ):
            cuts.append(index)
    cuts.append(len(points) - 1)
    parts = [
        points[cuts[index] : cuts[index + 1] + 1] for index in range(len(cuts) - 1)
    ]
    parts = [part for part in parts if len(part) >= 2]
    if not parts:
        return [list(points)]
    heading = _heading(parts[0][0], parts[0][-1])
    forward = [
        part
        for part in parts
        if _heading_delta(_heading(part[0], part[-1]), heading) <= WRAP_HEADING_DEG
    ]
    if len(forward) >= line_count:
        return forward[:line_count]
    return parts
