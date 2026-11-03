def place_rank_size(layer_id, rules):
    """Return the place-rank size in px. A layer with no rank returns None."""
    for rank in rules["labels"]["place_hierarchy"]:
        if layer_id in rank["layers"]:
            return rank["size_px"]
    return None
