# 0093 — Urban halos from a precomputed flag, and two R-01/R-09 decisions

**Date:** 2026-11-05

## Question

Josh made three decisions on the log 0090 inventory. How do we record them?
How do black names on the urban fill get an urban-fill halo without a
render-time layer lookup?

## What we did

Recorded Josh's three decisions:

1. B-45, G4 urban halos: "Precompute urban flag".
2. R-09 rank step: "Accept 17%".
3. R-01 stream vs index contour: "Yes, width counts".

Checked which layer draws the grey urban fill in the stock project. Counted
the carto_text rows inside that fill with QGIS and with DuckDB spatial.
Added a tag tool and an apply step that reads its output. Rendered the 4 km
BX24 grid. Compared three urban cells with the previous render and stock.

## What we found

### Urban fill source

- `residential_area map` draws the fill. It is one SimpleFill `#BCBAB6`
  on every row. It has no subset string and no rule filter.
- Its source is `residential_area.parquet` in EPSG:4167. carto_text is in
  EPSG:2193. The tag step must reproject the fill.
- The country has 2924 fill polygons and 213,702 carto_text rows.

### Size of the flag

- 3456 carto_text rows intersect the fill: 3378 black and 78 process blue.
  QGIS and DuckDB give the same count.
- The id list is 135 KB. The apply step writes it into two label rules, so
  the project grows by about 0.3 MB.
- The tag step takes about 10 s for the whole country.
- The BX24 apply, render and crop took 55 s with the whole-country list.
  CPU stayed busy. The render did not hang.
- So the whole-country list fits in a static expression. We do not limit it
  to an extent. `--extent` is there if a smaller list is needed.

### Render (4 km grid)

- Urban cells change: `1564000-5178000`, `1568000-5182000`,
  `1572000-5178000`, `1568000-5174000` and others with residential fill.
- Black names in the fill now sit on a grey halo. The street grid runs up
  to the letters. Before, each name cut a white hole in the grid.
- Brown and blue names keep the white halo.
- Rural cells change little. The previous render predates the open
  foot-track fix (commit `7325b52`), so some diffs are track crosses, not
  halos.

- Before and after crops: `docs/visuals/13-urban-halo-before-after.png`.
  Cells `1564000-5178000` (top) and `1572000-5178000` (bottom). Each row is
  stock, the previous accessible render, then this render, at 3× zoom.

### Decisions

- R-09: spot heights 6 pt vs names 7 pt is a 17% step. Josh accepts it as
  a written exception. Colour, digits and position separate a height from
  a name. Sizes do not change.
- R-01: stream vs index contour is 1.83:1 grey. Josh counts the width step
  (0.25 mm vs 0.35 mm) as the shape cue. Hue and red light (6.41:1) add to
  it. That pair is closed.

## What changed

- `tools/tag_urban_text.py` and `src/nzat/qgis/tag_urban_text_main.py`:
  QGIS Python. They read `residential_area map` and `nztopo50_carto_text`
  from the project. They write `urban_text.json` beside the project: the
  sorted ids of carto_text rows that intersect the fill. The tool stops if
  the fill renderer is not one symbol.
- `src/nzat/qgis/load_urban_text.py` reads that file, or returns an empty
  list.
- `src/nzat/qgis/patch_labels.py`: on carto_text, a data-defined
  `BufferColor` is `CASE WHEN "id" IN (...) AND "colour" = 'black' AND NOT
  natural-italic THEN urban fill ELSE paper END`. Spot heights stay black,
  so they count as black.
- `src/nzat/qgis/apply.py` passes the list. `defaults.py` names the file and
  the fill layer.
- Test: `test_black_names_in_urban_fill_take_an_urban_halo`.
- `docs/recommendations.md`: R-01 decision and R-09 exception.
- `docs/style-topo50.md`, `tools/README.md`, `BACKLOG.md` (B-45, B-35,
  B-33).
- `squares/accessible/urban_text.json` written for BX24. The sheet project
  in `squares/accessible-sheets/` was not touched.

## Confidence & gaps

Grade C for the flag (two tools agree on 3456 rows). Grade D for the look
(our review on three cells).

- A name tagged by its baseline can stick out past the fill. Its grey halo
  then sits on paper. Black on grey still passes.
- A name near the fill but not on it keeps a white halo over the fill edge.
- The sheet batch has no `urban_text.json`. Run the tag step on the sheet
  project, then apply again, before the next sheet batch.
- The flag is stale if the carto_text or residential data changes. Run the
  tag step again after a data refresh.
- The vector style does not use the flag.
