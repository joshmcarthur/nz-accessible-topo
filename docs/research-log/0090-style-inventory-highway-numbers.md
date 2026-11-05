# 0090 — Remaining style work, and state highway numbers

**Date:** 2026-11-05

## Question

Josh parked label placement. What raster style and symbology work is left?
Which item can we finish now, without a download or a decision?

## What we did

Read the "Met when" of each recommendation, the BACKLOG status and table,
grid gaps G1–G6 (log 0057), and logs 0071–0089. Counted italic faces and
font families on the applied project, including FontMarkers.

Tried an urban-fill halo for black names on urban fill (G4). Rendered the
4 km grid. Then fixed state highway numbers. Rendered the 4 km grid again
and compared each cell with the previous render and with stock.

## What we found

### Remaining raster style items

G2 and B-31 (label placement) are parked and not listed.

| # | Item | What is left | Why | Needs first |
|---|---|---|---|---|
| 1 | B-45, G4 urban halos | Black names on urban fill get an urban-fill halo | White halos cut holes in the street grid | Josh's decision: a precomputed urban flag, or a selective label mask |
| 2 | B-34, G5 scrub | A stronger scrub cue at sheet size | Plant marks read only at 3× zoom (log 0071) | Vector build applies `vegetation.scrub.alpha` (log 0076) |
| 3 | R-09 rank step | Spot heights 6 pt vs names 7 pt is a 17% step | "Met when" asks for ≥20% | Josh's decision (for example a 7.2 pt name floor). It also moves the label fit, which is parked |
| 4 | R-01, B-35, G6 | Index vs stream is 1.83:1 grey. Width (0.35 vs 0.25 mm) and hue carry the rest | "Met when" asks for 3:1 grey or a shape difference | Josh's decision: does a width step count as shape |
| 5 | R-05 close-out | Full-grid G3 review, then mark met | Italic count is 0 on labels and FontMarkers (this log) | None. Review only |
| 6 | B-36 shelterbelt | Grid review | Pairs pass (log 0063). No grid check is logged | None. Review only |
| 7 | B-37 contour numbers | Grid review | Face, size and halo are done (log 0082) | None. Review only |
| 8 | Blend after log 0082 | Check golf, opencast and shield symbols on `nztopo50_carto_symbol` | Normal blend can draw one over another | None. Review only |
| 9 | B-44 highway numbers | "74A" is a little wider than its shield | Three characters at 6 pt | None. Small follow-up |
| 10 | R-04 "Also" | Dash indefinite contours | `definition` is null on the national table (log 0026) | Data from LINZ |
| 11 | B-38 tree glyph | Paint the native tree marker | BX24 native is fill-only | A sheet with tree markers (download) |
| 12 | R-03, B-43 relief | Draw the 337.5° shade | No `dem.tif` beside the project | Download |
| 13 | R-13 variants | Greyscale-safe and high-contrast inks | Do not invent palettes (log 0046) | Josh's decision |
| 14 | Vector parity | Natural brown, Bold, stream widths, scrub alpha, shields | The vector build does not read these yet | Vector build (priority 4) |

R-08 stays provisional. It needs a user test, and R-16 is skipped.
B-39 (dual names) is label work and is parked.

### Urban halo (item 1)

- Stock draws no buffer on carto_text. The apply step draws the 0.4 mm
  `#FAFAFA` buffer on every name.
- Black is 10.84:1 on the urban fill `#BCBAB6`. Index brown is 3.38:1 and
  process blue 2.63:1. So only black names can take an urban halo.
- A data-defined buffer colour with `overlay_intersects('residential_area
  map')` hung the render. A sample showed the label thread waiting in the
  expression. `QgsMapRendererParallelJob.waitForFinished` blocks the main
  thread, and the overlay asks the main thread for the layer.
- The LINZ map container may render another way. A render-time overlay is
  not safe. We reverted it.

### State highway numbers (fixed)

- `nztopo50_carto_symbol_label` draws the number in each highway shield. Its
  source is `../../../../../Users/KBaker/Downloads/nztopo50_carto_symbol.parquet`.
  That path does not exist, so stock draws empty shields. BX24 has 14
  shields (SH 1, 73, 74, 74A, 75, 76).
- That layer's FontMarker still said `Nimbus Sans LINZ` `Narrow`. The
  accessible render loads no Nimbus file.
- The number is pure red `#FF0000`. The shield draws below the roads, so
  the number sat on the red highway line and could not be read.
- `#E31A1C` darkened against the white shield fill is `#940000`. It is 9.3:1
  on white and 3.0:1 in red light.

Evidence (4 km grid render, after vs before):

- 3 of 27 cells changed: `1564000-5170000` (SH 75), `1564000-5178000`
  (SH 73) and `1564000-5186000` (SH 1). Each change is only the shield box,
  37 × 37 px.
- Stock and the previous accessible render show an empty red outline under
  the road. The new render shows a white shield above the road with a dark
  red number.
- In the simulation panels the number reads in deutan, protan, tritan,
  grey and red light.

## What changed

- `src/nzat/qgis/patch_shield_numbers.py`: the number layer reads the symbol
  layer's source. The FontMarker uses `fonts.raster_family` and
  `fonts.raster_upright_style`, at least 6 pt. Its ink is
  `reference_inks.project_highway` darkened to `label_contrast.min_ratio`
  and `label_contrast.red_light_min` against the shield fill. A copy of the
  shield SVG draws under the number.
- `src/nzat/qgis/apply.py` calls it. The override docstring lists it.
- Test: `test_highway_numbers_draw_in_a_shield_in_the_raster_face`.
- `docs/style-topo50.md`. BACKLOG status paragraph refreshed to current
  facts. B-44 and B-45 added.
- `tools/style-topo50.json` did not change.

## Confidence & gaps

Grade C for the cause (the path and the font are in the project XML).
Grade D for the look (our review on 3 cells).

- "74A" overruns the shield a little. A smaller size for three characters
  would go under the 6 pt floor.
- The stock shield on `nztopo50_carto_symbol` still draws under the roads.
  The new copy covers it.
- The stock sheet keeps empty shields. Stock vs accessible now differs here.
- The vector style does not draw shield numbers in the raster face.
