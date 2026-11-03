def is_style_path(value):
    """Return True when value is a dotted path into the shared style file."""
    if not isinstance(value, str):
        return False
    lowered = value.lower()
    if lowered.startswith("#") or lowered.startswith("rgb"):
        return False
    return "." in value
