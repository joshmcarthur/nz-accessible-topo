from PIL import Image, ImageDraw

from nzat.render.tile_visibility import acuity_sigma_px, visible_fractions


def _tile(ground, *bars):
    """A 100 px tile. Each bar is (colour, box)."""
    image = Image.new("RGB", (100, 100), ground)
    draw = ImageDraw.Draw(image)
    for colour, box in bars:
        draw.rectangle(box, fill=colour)
    return image


def test_black_symbol_on_paper_is_all_visible():
    paper = _tile("white", ("black", (20, 45, 80, 55)))
    visible = visible_fractions(paper, paper, False)
    # The blur rounds the corners of a 0.4 mm bar and no more.
    assert visible.pop("acuity") > 0.95
    assert set(visible.values()) == {1.0}


def test_acuity_blur_is_the_detail_a_6_18_eye_resolves_at_400_mm():
    # 3 arc minutes at 400 mm is 0.349 mm, 8.2 px at 600 dpi, as a full width.
    assert round(acuity_sigma_px(), 2) == 3.5


def test_thin_black_line_is_lost_to_reduced_acuity_only():
    paper = _tile("white", ("black", (0, 50, 99, 50)))
    visible = visible_fractions(paper, paper, False)
    assert visible["normal"] == 1.0
    assert visible["acuity"] == 0.0


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
