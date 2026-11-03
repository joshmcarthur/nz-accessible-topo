def sheet_layer_ids(ordered_ids, visible_ids):
    """Keep the layers the sheet map draws. Keep the project draw order."""
    visible = set(visible_ids)
    return [layer_id for layer_id in ordered_ids if layer_id in visible]
