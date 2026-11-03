def is_place_name(layer_id, text_field):
    """A place-name label is a Place-Label layer with text to read."""
    if text_field in (None, ""):
        return False
    return isinstance(layer_id, str) and layer_id.startswith("Place-Label-")
