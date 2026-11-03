def is_owned_road_layer(name):
    """Two-lane and sealed road fills. Skip highway and background casings."""
    lower = name.lower()
    if "road_line" not in lower:
        return False
    if "highway" in lower or "background" in lower:
        return False
    return True
