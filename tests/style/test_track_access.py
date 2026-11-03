from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path

RULES = load_rules()


def test_track_access_channel_is_reserved():
    # Catches access painted, a reserved channel other than casing_colour, or an access ink added to the style file.
    access = RULES["tracks"]["access"]
    assert access["reserved_channel"] == "casing_colour"
    assert access["painted"] is False
    assert "colour" not in access
    assert lookup_style_path(RULES, "tracks.access.reserved_channel") == "casing_colour"
    assert lookup_style_path(RULES, "tracks.access.painted") is False
