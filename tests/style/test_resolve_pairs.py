import json

from nzat.colour.parse_colour import parse_colour
from nzat.paths import PAIRS_PATH, ROOT
from nzat.style.load_rules import load_rules
from nzat.style.pair_audit import pair_audit
from nzat.style.resolve_colour_spec import resolve_colour_spec
from nzat.style.resolve_pairs import resolve_pairs

LINE_ON_FILL_NAMES = (
    "Index contour vs scrub",
    "Index contour vs native forest",
    "Index contour vs water",
    "Index contour vs urban",
    "Intermediate contour vs scrub",
    "Intermediate contour vs native forest",
    "Intermediate contour vs water",
    "Intermediate contour vs urban",
    "Stream vs scrub",
    "Stream vs native forest",
    "Stream vs water",
    "Stream vs urban",
    "Track vs scrub",
    "Track vs native forest",
    "Track vs water",
    "Track vs urban",
    "Stream vs paper",
    "Shelterbelt vs paper",
    "Grid vs paper",
    "Index contour vs stream",
    "Intermediate contour vs stream",
    "Shelterbelt vs native forest",
)


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
    assert parsed_index[3] == 1.0

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


def test_qgis_byte_pair_alpha_resolves_to_unit_range():
    # Catches a vegetation fill alpha left as a QGIS 0-255 byte in pair compositing.
    colour = resolve_colour_spec(
        {"colour": "vegetation.scrub.colour", "alpha": "vegetation.scrub.alpha"},
        {"vegetation": {"scrub": {"colour": "#A3CC90", "alpha": 200}}},
    )
    parsed = parse_colour(colour)
    assert parsed[3] != 200
    assert abs(parsed[3] - 200 / 255) < 1e-6


def test_topo_line_on_fill_pairs_use_style_paths():
    # Catches a line-on-fill pair left as hex, or Stream vs paper using the grid ink.
    topo_path = ROOT / "tools" / "pairs-topo50-accessible.json"
    topo = json.load(open(topo_path))
    by_name = {pair["name"]: pair for pair in topo}
    missing = [name for name in LINE_ON_FILL_NAMES if name not in by_name]
    assert missing == []
    stream_raw = by_name["Stream vs paper"]
    assert stream_raw["a"]["colour"] == "reference_inks.stream"
    native_raw = next(pair for pair in topo if pair["name"] == "Native forest vs scrub")
    assert native_raw["a"]["alpha"] == "vegetation.native.alpha"
    assert native_raw["b"]["alpha"] == "vegetation.scrub.alpha"
    water_raw = next(pair for pair in topo if pair["name"] == "Scrub vs water")
    assert water_raw["a"]["alpha"] == "vegetation.scrub.alpha"
    for name in LINE_ON_FILL_NAMES:
        pair = by_name[name]
        for side in ("a", "b"):
            colour = pair[side]["colour"]
            if colour != "#FFFFFF":
                assert colour.startswith("reference_inks.") or "." in colour
                assert not colour.startswith("#"), (name, side, colour)
    rules = load_rules()
    result = next(iter(pair_audit(resolve_pairs([stream_raw], rules), (255, 255, 255))))
    assert result["grey_cr"] >= 3
    assert result["red_cr"] >= 3
    scrub_raw = by_name["Index contour vs scrub"]
    scrub = next(iter(pair_audit(resolve_pairs([scrub_raw], rules), (255, 255, 255))))
    assert scrub["grey_cr"] >= 3
    assert scrub["red_cr"] >= 3
    for name in ("Shelterbelt vs paper", "Grid vs paper"):
        row = next(
            iter(pair_audit(resolve_pairs([by_name[name]], rules), (255, 255, 255)))
        )
        assert row["grey_cr"] >= 3
        assert row["red_cr"] >= 3
