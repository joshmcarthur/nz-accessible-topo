def floor_text_size(size, floor):
    """Raise one text size to the floor. Keep a size that is already high enough."""
    if isinstance(size, (int, float)) and not isinstance(size, bool) and size < floor:
        return floor
    return size
