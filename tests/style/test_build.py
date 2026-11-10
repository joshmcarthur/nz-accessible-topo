from nzat.paths import UPSTREAM
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.vector_params import P


def test_vector_build_reads_the_style_file():
    # Catches a contour hex left in P, or a catalog path that no longer points at Shortbread.
    assert str(UPSTREAM).endswith("upstream/linz-topographic-v2.json")
    assert UPSTREAM.is_file()
    assert "contour_index" not in P
    assert "contour_intermediate" not in P
    rules = load_rules()
    assert (
        lookup_style_path(rules, "contours.index.colour")
        == rules["contours"]["index"]["colour"]
    )
    assert (
        lookup_style_path(rules, "contours.intermediate.colour")
        == rules["contours"]["intermediate"]["colour"]
    )
    assert lookup_style_path(rules, "contours.index.alpha") == 1.0
    assert lookup_style_path(rules, "contours.intermediate.alpha") == 0.5
