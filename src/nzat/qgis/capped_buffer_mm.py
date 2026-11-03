def capped_buffer_mm(size_text, max_mm):
    """Return the buffer width in mm. Do not go above max_mm."""
    try:
        size = float(size_text)
    except (TypeError, ValueError):
        return None
    return min(size, float(max_mm))
