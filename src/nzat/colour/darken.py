from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.lab_to_rgb import lab_to_rgb
from nzat.colour.red_light import red_light_reflectance
from nzat.colour.rel_luminance import rel_luminance
from nzat.colour.rgb_to_lab import rgb_to_lab


def _darken_until(rgb, ok):
    L, a, b = rgb_to_lab(rgb)
    cur = rgb
    while not ok(cur) and L > 0:
        L -= 0.5
        cur = lab_to_rgb((L, a, b))
    return cur


def darken_for_text(rgb, behind, min_ratio, red_min=None):
    """Lower L* until the ink meets min_ratio against behind. Keep hue.

    When red_min is set, the ink must also meet that floor under the red-light model.
    """

    def ok(colour):
        contrast = (
            contrast_ratio(rel_luminance(colour), rel_luminance(behind)) >= min_ratio
        )
        if red_min is None:
            return contrast
        red = (
            contrast_ratio(red_light_reflectance(colour), red_light_reflectance(behind))
            >= red_min
        )
        return contrast and red

    return _darken_until(rgb, ok)
