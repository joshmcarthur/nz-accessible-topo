# 0111 — Tile scores, and the road casing is back

**Date:** 2026-11-10

## Question

Which legend symbols stop being readable on a fill, or under another class,
in each vision condition? The tiles from log 0110 need a number.

## What we did

`tools/export_symbol_tiles.py` scores each test tile. The ink pixels of the
paper tile are the symbol. A pixel stays visible when it still differs from
the ground just outside the symbol (a ring 0.5 mm wide): 3:1 for greyscale
and for red light (R-01), CIEDE2000 10 for normal vision and the three
dichromacies (R-04). In a conflict tile the pixel must also keep its
paper-tile colour, so ink from the other class does not count. A tile fails
a condition when under half of the ink stays visible. That half is our own
floor.

We drew the stock road tiles with the same tool (`--theme Map5View`) to
compare.

## What we found

353 of 1146 tiles failed one condition or more.

- **Roads had lost their dark casing.** Every road class scored 0 under red
  light. Stock scored 0.32, which is the casing share of the road ink. Stock
  draws static widths: fill 0.45 mm on a 0.75 mm casing for two lanes, and
  0.25 mm on 0.5 mm for one lane. Its `lane_count` width expression is
  stored but inactive. The N-1 floor (commit `4f18cee`, log 0097) wrapped
  that expression in `max()` and wrote it back active. The two-lane fill
  became 0.715 mm on a 0.75 mm casing. Log 0051 says the casing carries the
  road under red light, so this broke R-01 for roads.
- **Fix.** The apply step leaves an inactive width expression off. The
  one-lane fill is still 0.35 mm (N-1), so the one-lane casing layer goes
  from 0.5 to 0.6 mm and keeps the stock 0.125 mm edge (Josh, 2026-11-10).
  Road scores now equal stock. 335 tiles fail.
- A cased road still scores under 0.5 in red light, in stock too. The score
  counts the share of ink. A casing is a third of the road ink, but two
  dark edges are enough to follow a road. Read the road rows against the
  stock number, not against the 0.5 floor.
- Index contour on native and exotic forest: 0.34 visible under red light.
- Rock outcrops and fumarole fail under red light on paper. Unmetalled
  road, cemetery and training track fail in greyscale on paper.
- Water and urban fills hide 21 symbols in every condition. That is the
  LINZ layer order (log 0110).
- A name across the symbol hides half or more of 49 symbols. The test puts
  the name on the symbol, so it is the worst case.
- The three dichromacies fail the same tiles as normal vision, apart from
  cemetery and training track in protanopia.

## What changed

- `src/nzat/render/tile_visibility.py`, `src/nzat/site/export_symbol_tiles.py`,
  `tools/export_symbol_tiles.py`, `site/src/data/symbol-tiles.json`.
- `src/nzat/qgis/patch_road_widths.py`: an inactive width expression stays
  off; `patch_one_lane_casing` widens the one-lane casing.
- `tools/style-topo50.json`: `sizes.one_lane_road_casing_mm` is 0.6.
- The BX24 project is applied again. The face, the grid and the tiles are
  drawn again.

## Confidence & gaps

Grade D. The score is our own model on our own render.

- The score does not test shape. A spot-height dot on the sand stipple
  passes. A cased line reads better than its score.
- The 0.5 floor and the 0.5 mm ring are not from a source.
- No reduced-acuity condition yet.
- The `/symbols/` crops, the legend picture and the sheet rasters predate
  logs 0110 and 0111.
