from nzat.style.floor_text_size import floor_text_size
from nzat.style.hierarchy_ratios import hierarchy_ratios
from nzat.style.is_place_name import is_place_name
from nzat.style.label_floor_px import label_floor_px
from nzat.style.load_rules import load_rules
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.place_rank_size import place_rank_size
from nzat.style.resolved_text_size import resolved_text_size
from nzat.style.vector_params import P


def test_vector_size_floor_reads_the_style_file():
    # Catches a place name left under 11 px, or a web floor that ignores the style file.
    rules = load_rules()
    labels = rules["labels"]
    assert (
        label_floor_px("Place-Label-Suburb", "{label}", rules)
        == labels["place_name_floor_px"]
    )
    assert label_floor_px("All-Road-Labels", "{name}", rules) == labels["web_floor_px"]
    assert label_floor_px("Place-Symbol-Peak-12", "", rules) == labels["web_floor_px"]
    assert floor_text_size(10, labels["place_name_floor_px"]) == 11
    assert floor_text_size(12, labels["place_name_floor_px"]) == 12
    assert floor_text_size(8, labels["web_floor_px"]) == 10
    assert is_place_name("Place-Label-Suburb", "{label}") is True
    assert is_place_name("Place-Symbol-Peak-12", "") is False
    assert lookup_style_path(rules, "labels.letter_spacing_em") == 0.05
    assert "letter_spacing_em" not in P


def test_place_ranks_differ_by_at_least_20_percent():
    # Catches a town size under 20% above suburb, or an island layer pulled into the place ladder.
    rules = load_rules()
    ranks = rules["labels"]["place_hierarchy"]
    assert [rank["rank"] for rank in ranks] == ["suburb-locality", "town", "city"]
    assert all(ratio >= 1.2 for ratio in hierarchy_ratios(ranks))
    assert place_rank_size("Place-Label-Suburb", rules) == place_rank_size(
        "Place-Label-Locality", rules
    )
    assert place_rank_size("Place-Label-City-14", rules) == place_rank_size(
        "Place-Label-City-7", rules
    )
    assert (
        place_rank_size("Place-Label-Town", rules)
        / place_rank_size("Place-Label-Suburb", rules)
        >= 1.2
    )
    assert place_rank_size("Place-Label-Island-12", rules) is None
    assert resolved_text_size(12, 11, 14) == 14
    assert resolved_text_size(10, 11, None) == 11
