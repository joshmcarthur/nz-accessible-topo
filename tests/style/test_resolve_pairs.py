import json

from nzat.colour.parse_colour import parse_colour
from nzat.paths import PAIRS_PATH, ROOT
from nzat.style.load_rules import load_rules
from nzat.style.resolve_pairs import resolve_pairs


def test_pair_audit_reads_the_style_file():
    # Catches a pair colour that stays hardcoded after the style file changes, or a casing that drops its alpha.
    rules = json.loads(json.dumps(load_rules()))
    raw = json.load(open(PAIRS_PATH))
    index_raw = next(pair for pair in raw if pair["name"] == "Index contour vs paper")
    assert index_raw["a"]["colour"] == "contours.index.colour"
    assert index_raw["a"]["alpha"] == "contours.index.alpha"
    mid_raw = next(
        pair for pair in raw if pair["name"] == "Intermediate contour vs paper"
    )
    assert mid_raw["a"]["alpha"] == "contours.intermediate.alpha"
    assert mid_raw["floor"]["grey"] < 3
    assert mid_raw["floor"]["red"] < 3
    highway_raw = next(
        pair for pair in raw if pair["name"] == "Index contour vs state highway"
    )
    assert highway_raw["b"]["colour"].startswith("rgba(")
    casing_raw = next(
        pair for pair in raw if pair["name"] == "Closed-track casing vs paper"
    )
    assert casing_raw["a"]["colour"] == "tracks.closed_foot.casing_colour"
    assert casing_raw["a"]["alpha"] == "tracks.closed_foot.casing_alpha"

    resolved = resolve_pairs(raw, rules)
    index = next(pair for pair in resolved if pair["name"] == "Index contour vs paper")
    parsed_index = parse_colour(index["a"]["colour"])
    assert parsed_index[:3] == parse_colour(rules["contours"]["index"]["colour"])[:3]
    assert parsed_index[3] == 0.85

    casing = next(
        pair for pair in resolved if pair["name"] == "Closed-track casing vs paper"
    )
    got = parse_colour(casing["a"]["colour"])
    expect = parse_colour(rules["tracks"]["closed_foot"]["casing_colour"])
    assert got[:3] == expect[:3]
    assert got[3] == rules["tracks"]["closed_foot"]["casing_alpha"]

    topo_path = ROOT / "tools" / "pairs-topo50-accessible.json"
    topo = json.load(open(topo_path))
    index_topo = next(pair for pair in topo if pair["name"] == "Index contour vs paper")
    assert index_topo["a"]["alpha"] == "contours.index.alpha"
    mid_topo = next(
        pair for pair in topo if pair["name"] == "Intermediate contour vs paper"
    )
    assert mid_topo["a"]["alpha"] == "contours.intermediate.alpha"
    road_raw = next(
        pair for pair in topo if pair["name"] == "Intermediate contour vs project road"
    )
    assert road_raw["b"]["colour"] == "reference_inks.project_road"
    highway_raw = next(
        pair
        for pair in topo
        if pair["name"] == "Intermediate contour vs project highway"
    )
    assert highway_raw["b"]["colour"] == "reference_inks.project_highway"
    number_raw = next(
        pair for pair in topo if pair["name"] == "Contour number vs project road"
    )
    assert number_raw["a"]["colour"] == "contours.index.colour"
    road_highway_raw = next(
        pair for pair in topo if pair["name"] == "Project road vs project highway"
    )
    assert road_highway_raw["a"]["colour"] == "reference_inks.project_road"
    water_raw = next(pair for pair in topo if pair["name"] == "Scrub vs water")
    assert water_raw["b"]["colour"] == "reference_inks.water_fill"
    historic_raw = next(
        pair for pair in topo if pair["name"] == "Historic label vs paper"
    )
    assert historic_raw["a"]["colour"] == "rgb(145, 0, 0)"

    rules["contours"]["index"]["colour"] = "#000000"
    changed = resolve_pairs(raw, rules)
    index2 = next(pair for pair in changed if pair["name"] == "Index contour vs paper")
    assert parse_colour(index2["a"]["colour"])[:3] == (0, 0, 0)
