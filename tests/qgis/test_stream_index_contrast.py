from nzat.colour.composite import composite
from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.parse_colour import parse_colour
from nzat.colour.rel_luminance import rel_luminance
from nzat.qgis.defaults import STYLE


def test_stream_is_3_to_1_grey_against_painted_index():
    # Catches stream #004C99 after the N-1 width step removed the index vs stream cue.
    stream = parse_colour(STYLE["reference_inks"]["stream"])[:3]
    index = parse_colour(STYLE["contours"]["index"]["colour"])
    painted = composite(
        (index[0], index[1], index[2], STYLE["contours"]["index"]["alpha"]),
        (255, 255, 255),
    )
    grey = contrast_ratio(rel_luminance(stream), rel_luminance(painted))
    assert grey >= 3.0
    assert STYLE["reference_inks"]["stream"] == "#00276D"
