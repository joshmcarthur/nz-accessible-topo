import json

from nzat.paths import ROOT
from nzat.style.load_rules import load_rules
from nzat.style.pair_audit import pair_audit
from nzat.style.resolve_pairs import resolve_pairs


def test_painted_contour_pairs_meet_r04():
    # Catches contour inks that fail ΔE ≥10 against painted road and highway fills.
    topo_path = ROOT / "tools" / "pairs-topo50-accessible.json"
    rules = json.loads(json.dumps(load_rules()))
    names = (
        "Index contour vs project road",
        "Intermediate contour vs project road",
        "Index contour vs project highway",
        "Intermediate contour vs project highway",
        "Index contour vs paper",
        "Contour number vs project road",
        "Project road vs project highway",
        "Project road vs paper",
    )
    raw = [pair for pair in json.load(open(topo_path)) if pair["name"] in names]
    assert {pair["name"] for pair in raw} == set(names)
    resolved = resolve_pairs(raw, rules)
    for result in pair_audit(resolved, (255, 255, 255)):
        worst = min(
            result[key]
            for key in ("normal", "protanopia", "deuteranopia", "tritanopia")
        )
        assert worst >= 10, result["name"]
        if result["name"] in ("Index contour vs paper", "Project road vs paper"):
            assert result["grey_cr"] >= 3, result["name"]
        if result["name"] == "Index contour vs paper":
            assert result["red_cr"] >= 3
