# 0114 — Depression contours in the index ink; the `type` column is not the fix

**Date:** 2026-11-10

## Question

Seven symbols still failed the test tiles after log 0113. Which fails are a
style fault, which are a scene that cannot occur, and does reading the
`type` column give cemetery and training track their LINZ symbols?

## What we did

- Depression contours: the line takes the index ink at the intermediate
  width. The ticks were already in the index ink.
- Added written reasons for scenes that say nothing about a class.
- Tested the `type` idea on a scratch copy of the project before applying
  it: set the `landuse` and `structure_line` renderers from `feature_type`
  to `type` and drew twelve symbols.

## What we found

- **Depression contours** pass under a name in greyscale and red light. The
  pale intermediate ink had carried the line; a name halo cut the ticks,
  and nothing was left.
- **Ice contours** on forest, scrub, sand and swamp are not gated: ice
  contours draw only on ice. **Floodgate** on water and urban is not gated:
  the gate bar draws, and the sample watercourse beside it is under the
  fill, as on the stock map. Under a name the floodgate follows the
  point-mark rule (log 0113).
- **Reading `type` is wrong.** The two layers categorise on a
  `feature_type` column that the data does not have, so every feature
  takes the NULL category. With `type`, each class takes its own category,
  and those categories are unstyled: QGIS random colours (orange, purple,
  lime). LINZ styled only the NULL category. Stock `Map5View` hides both
  layers, so the stock sheet never shows them. We did not apply the change.
- The printed legend draws cemetery as a dashed outline with crosses,
  training track as a dashed oval, and weir as a thin blue line with a
  black bar. Our `Map5View-all` draws cyan slabs and a thick blue bar.
- 12 tiles and 4 symbols fail: cemetery and training track (protanopia),
  and unmetalled road and one-lane bridge on the urban fill under reduced
  acuity.

## What changed

- `src/nzat/qgis/patch_contour.py`, `tests/qgis/test_patch_contour.py`.
- `src/nzat/qgis/symbol_tile_scenes.py`: `NOT_ON` holds a reason per scene.
- `site/src/data/symbol-tiles.json`, the tile strips, the page text.

## Confidence & gaps

Grade D for the scores. The `type` result is a direct render, grade B.

- Josh asked for owned symbols for every `landuse` and `structure_line`
  class that has a printed legend row. Not started.
- Earlier advice in this project to "read `type`" for these layers is
  withdrawn. `patch_springs.py` does set `water_point` to `type`; that
  layer's categories are styled.
