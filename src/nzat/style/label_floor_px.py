from nzat.style.is_place_name import is_place_name


def label_floor_px(layer_id, text_field, rules):
    """Return the web size floor in px for this label."""
    labels = rules["labels"]
    if is_place_name(layer_id, text_field):
        return labels["place_name_floor_px"]
    return labels["web_floor_px"]
