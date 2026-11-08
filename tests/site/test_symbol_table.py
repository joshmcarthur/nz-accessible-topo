from nzat.qgis.cover_set import map_png_name
from nzat.qgis.legend_swatches import LEGEND_SIZE, SWATCHES
from nzat.site.export_symbol_table import IMAGE_DIR, build_table, clear_legend_crops
from nzat.site.symbol_checks import evaluate, passes
from nzat.site.symbol_rows import SECTIONS, STATUSES, SYMBOLS, ink, spec


def test_checks_flag_red_light_thin_lines_and_colour_only():
    # Catches a red-light, width, size or colour-only fail that the table would show as a pass.
    locked = spec(
        "",
        (ink("#FF4500", "bar"),),
        stroke_mm=0.2,
        mark_mm=1.4,
        colour_only={"label": "gate", "hex": "#000000"},
    )
    failed = {c["label"] for c in evaluate(locked) if not c["pass"]}
    assert failed == {"Red light 3:1", "Not colour alone"}
    fence = spec("", (ink("#000000", "line"),), line_mm=0.05)
    assert [c["label"] for c in evaluate(fence) if not c["pass"]] == ["Line width"]
    outline = spec("", (ink("#004C99", "o"),), line_mm=0.1, exempt={"line_mm": "x"})
    assert passes(evaluate(outline))
    fill = spec("", (ink("#BCBAB6", "fill", "fill"),))
    assert evaluate(fill) == []
    merged = evaluate(spec("", (ink("#000000", "l"),)), merged_with="single track")
    assert not passes(merged)


def test_every_row_status_matches_its_checks():
    # Catches a row marked done that fails a floor, a proposal that fails its own floors, or a duplicate key or box.
    keys = [s["key"] for s in SYMBOLS]
    assert len(keys) == len(set(keys))
    width, height = LEGEND_SIZE
    boxes = [s["box"] for s in SYMBOLS if s["box"]]
    assert len(boxes) == len(set(boxes))
    for x0, y0, x1, y1 in boxes:
        assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height
    for symbol in SYMBOLS:
        assert symbol["section"] in SECTIONS and symbol["status"] in STATUSES
        measured = evaluate(symbol["measured"], symbol["merged_with"])
        if symbol["status"] == "done":
            assert passes(measured), symbol["key"]
            continue
        assert passes(evaluate(symbol["proposal"])), symbol["key"]
        if symbol["status"] == "proposed":
            assert not passes(measured), symbol["key"]
        else:
            assert symbol["drawn"] == "no", symbol["key"]


def test_blocked_rows_are_not_redrawn():
    # Catches a blocked stock row marked as if the accessible legend redraws it.
    for symbol in SYMBOLS:
        if symbol["status"] == "blocked":
            assert not symbol["redrawn"], symbol["key"]


def test_redrawn_rows_sit_inside_the_legend_swatch_boxes():
    # Catches an "ours today" crop taken from a row the accessible legend does not redraw.
    swatch_boxes = [s["box"] for s in SWATCHES]
    for symbol in SYMBOLS:
        if not symbol["redrawn"]:
            continue
        x0, y0, x1, y1 = symbol["box"]
        assert any(
            bx0 <= x0 and x1 <= bx1 and by0 <= y0 and y1 <= by1
            for bx0, by0, bx1, by1 in swatch_boxes
        ), symbol["key"]


def test_legend_crop_clear_keeps_map_pngs(tmp_path):
    # Catches export_symbol_table wiping in-situ {key}-map.png crops.
    linz = tmp_path / "gate-linz.png"
    ours = tmp_path / "gate-ours.png"
    situ = tmp_path / map_png_name("gate")
    linz.write_bytes(b"a")
    ours.write_bytes(b"b")
    situ.write_bytes(b"c")
    clear_legend_crops(tmp_path)
    assert not linz.exists()
    assert not ours.exists()
    assert situ.exists()


def test_table_links_a_map_crop_when_the_png_exists():
    # Catches /symbols/ omitting an in-situ crop that is already on disk.
    table = build_table()
    rows = [row for section in table["sections"] for row in section["rows"]]
    by_key = {row["key"]: row for row in rows}
    situ = IMAGE_DIR / map_png_name("bivouac")
    if situ.is_file():
        assert by_key["bivouac"]["map_image"] == f"symbols/{map_png_name('bivouac')}"
    else:
        assert by_key["bivouac"]["map_image"] is None
    assert by_key["cattlestop"]["map_image"] is None
    assert by_key["cattlestop"]["map_note"] == "No national type"
    assert by_key["helipad"]["map_image"] is None
    assert "transport_point" in by_key["helipad"]["map_note"]


def test_table_counts_every_symbol_once():
    # Catches a section that drops rows or counts that disagree with the rows.
    table = build_table()
    rows = [row for section in table["sections"] for row in section["rows"]]
    assert len(rows) == len(SYMBOLS)
    assert sum(table["counts"].values()) == len(SYMBOLS)
