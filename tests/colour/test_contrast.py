from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.rel_luminance import rel_luminance


def test_contrast_black_white():
    assert (
        round(
            contrast_ratio(rel_luminance((0, 0, 0)), rel_luminance((255, 255, 255))), 2
        )
        == 21.0
    )
