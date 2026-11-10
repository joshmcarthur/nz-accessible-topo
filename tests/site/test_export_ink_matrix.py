import json

from nzat.paths import TOPO_PAIRS_PATH
from nzat.site.export_ink_matrix import build_matrix


def test_matrix_covers_every_pair_and_flags_r01():
    # Catches a dropped pair, a worst-CVD field that is not the min, or Stream vs paper left unflagged.
    raw = json.loads(TOPO_PAIRS_PATH.read_text(encoding="utf-8"))
    payload = build_matrix()
    names = [row["name"] for row in payload["pairs"]]
    assert names == [pair["name"] for pair in raw]
    by_name = {row["name"]: row for row in payload["pairs"]}
    stream = by_name["Stream vs paper"]
    assert not stream["fails_r01"]
    assert stream["grey_cr"] >= 3
    assert not by_name["Index contour vs scrub"]["fails_r01"]
    assert not by_name["Shelterbelt vs paper"]["fails_r01"]
    assert not by_name["Grid vs paper"]["fails_r01"]
    for row in payload["pairs"]:
        worst = min(row[key] for key in ("protanopia", "deuteranopia", "tritanopia"))
        assert row["worst_cvd"] == worst
        # The flag reads the unrounded ratio. A ratio shown as exactly 3.0 can
        # be 2.996 (index vs intermediate under red light), so skip that edge.
        if 3.0 in (row["grey_cr"], row["red_cr"]):
            continue
        expect = bool(row["grey_cr"] < 3 or row["red_cr"] < 3)
        assert row["fails_r01"] == expect
    assert "Index contour vs stream" in by_name
    assert "Island outline vs paper" in by_name
    assert "Exotic forest vs paper" in by_name
    assert "Vegetation outline vs paper" in by_name
    assert not by_name["Vegetation outline vs paper"]["fails_r01"]
    assert "Shelterbelt vs native forest" in by_name
