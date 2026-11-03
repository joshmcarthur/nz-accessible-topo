from nzat.qgis.defaults import STYLE


def size_floor(layer_name, size_text, style=None):
    """Return the label size in points after the R-09 floor.

    Spot-height layers may stay at 6 pt. Every other map label is at least 7 pt.
    """
    labels = (style or STYLE)["labels"]
    spot = labels["spot_height_layer_contains"]
    floor = (
        float(labels["spot_height_floor_pt"])
        if layer_name and spot in layer_name
        else float(labels["size_floor_pt"])
    )
    try:
        size = float(size_text)
    except (TypeError, ValueError):
        return size_text
    if size < floor:
        return str(int(floor))
    return size_text
