from PIL import Image, ImageDraw

from nzat.render.tile_visibility import visible_fractions


def _tile(ground, *bars):
    """A 100 px tile. Each bar is (colour, box)."""
    image = Image.new("RGB", (100, 100), ground)
    draw = ImageDraw.Draw(image)
    for colour, box in bars:
        draw.rectangle(box, fill=colour)
    return image


def test_black_symbol_on_paper_is_all_visible():
    paper = _tile("white", ("black", (20, 45, 80, 55)))
    assert set(visible_fractions(paper, paper, False).values()) == {1.0}


def test_red_symbol_is_lost_under_red_light_only():
    paper = _tile("white", ((255, 0, 0), (20, 45, 80, 55)))
    visible = visible_fractions(paper, paper, False)
    assert visible["normal"] == 1.0
    assert visible["grey"] == 1.0
    assert visible["red"] == 0.0


def test_symbol_under_an_opaque_fill_is_not_visible():
    paper = _tile("white", ("black", (20, 45, 80, 55)))
    hidden = _tile((188, 186, 182))
    assert set(visible_fractions(paper, hidden, False).values()) == {0.0}


def test_other_ink_over_the_symbol_does_not_count_as_the_symbol():
    paper = _tile("white", ("black", (20, 45, 80, 55)))
    crossed = _tile(
        "white", ("black", (20, 45, 80, 55)), ((0, 76, 153), (20, 45, 49, 55))
    )
    visible = visible_fractions(paper, crossed, True)
    assert 0.45 < visible["normal"] < 0.55


def test_symbol_with_no_ground_has_no_score():
    full = _tile("black")
    assert visible_fractions(full, full, False) is None
