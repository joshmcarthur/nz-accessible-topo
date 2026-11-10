# 0115 — Index contours draw opaque

**Date:** 2026-11-10

## Question

The index contour on native and exotic forest was 34% visible under red
light before the located-ink rule, and 54% after it. Log 0054 set the index
alpha to 0.85 to quieten the contour mesh. Does alpha 1.0 fix the forest
case without bringing the clutter back?

## What we did

Applied `contours.index.alpha` 1.0 on a scratch copy of the project. Drew
the index contour tiles and a 2 km Port Hills area at 600 dpi at both
values. Scored a foot track and a stream under the contour mesh at both
values.

## What we found

- Index contour on native and exotic forest under red light: 54% to 100%
  visible.
- A foot track and a stream under the contour mesh stay 100% visible.
- On the Port Hills the index line is a little darker. No name, track or
  stream is harder to find.
- Pair audit: index contour vs paper is 6.55:1 grey and 4.29:1 red (was
  4.60 and 3.28). Index vs native forest is 5.59 and 3.56.
- **Decision (Josh):** use 1.0. This replaces the 0.85 from log 0054.
  Intermediate contours stay at 0.5.
- **Decision (Josh):** an unmetalled road and a one-lane bridge on the
  urban fill are a written exception under reduced acuity. Their dark
  edges and white centre blur to the urban grey. Both are rare inside
  towns, and stock draws them the same way.
- 10 tiles fail, all on cemetery and training track.

## What changed

- `tools/style-topo50.json`: `contours.index.alpha` is 1.0.
- `styles/`, `docs/styles/`, `site/src/data/ink-matrix.json`, tokens.
- `docs/recommendations.md` (R-04 starting values), `docs/style-topo50.md`.
- `src/nzat/qgis/symbol_tile_scenes.py`: the two urban exceptions.
- `tests/site/test_export_ink_matrix.py`: a ratio shown as exactly 3.0 can
  be just under it; the test skips that edge.

## Confidence & gaps

Grade D. One hill area at one scale.

- OQ-09 is still open: a steep alpine sheet may show more mesh at alpha
  1.0. Check it when the sheets are redrawn.
- "Index vs intermediate contour" is now 3.88:1 grey and 2.996:1 under red
  light. The width step still carries that pair.
