# 0071 — Width steps, not one line floor

**Date:** 2026-11-05

## Question

Does the log 0070 line floor (0.35 mm on every owned stroke) cause
regressions on the 4 km grid? Does the pale scrub still read as a class?

## What we did

Rendered the log 0070 face and compared 8 of the 27 cells with stock
(`1564000-5162000`, `1564000-5178000`, `1568000-5166000`,
`1576000-5174000`, `1580000-5154000`, `1580000-5170000`, and two more).
Read the stock widths for each stream, shelterbelt, and grid symbol.
Counted `water_line` types: river 711,639, drain 40,595, canal 359.
Scored candidate scrub and native fills against the index contour in grey
and red light.

## What we found

The single floor caused regressions:

- Field drains on the plain drew at river weight. The plain read as a mesh
  of rivers (`1564000-5162000`).
- Pond and lake rims at 0.35 mm turned small ponds into blue blobs.
- Rivers drew heavier than the index contour and as heavy as roads.

Stock draws every water line at 0.1 mm. MN (F-31) treats 1 pt as the thin
end of a line family. A class hierarchy needs steps, not one floor.

Scrub was nearly invisible. The fill composites to `#F6FAF4`. The marks
were hairline arcs in `#B2DF8A`. Most marks were clipped in narrow strips.

A greener fill fails red light. The index ink is settled (R-04). Index on
the stock scrub fill is 2.90:1 in red light, and greener candidates are
2.3–2.6:1. So the marks must carry scrub, not the fill.

## What changed

- `tools/style-topo50.json`: removed `sizes`. `water.stream_width_mm` 0.25
  (the width Josh locked in log 0067). New `water.drain_width_mm` 0.15.
  `scrub_dots.colour` `#6A9A50`, new `scrub_dots.stroke_mm` 0.18.
- `src/nzat/qgis/patch_water_line.py`: data-defined width by `type`.
- `patch_owned_lines` changes colour only again. Coastline, water outlines,
  shelterbelt, and grid keep stock widths in the darker inks.
- Scrub marks clip by centroid, so a mark draws whole or not at all.
- F-31 implication, R-04 print widths, B-35, B-36, `docs/style-topo50.md`.

## Confidence & gaps

Grade D (our review). Drains at 0.15 mm are still visible. Rivers no longer
outweigh the index line. Scrub arcs are visible at 3× zoom. At sheet size
the scrub cue is still weak. G5 stays open. A steep sheet is still OQ-09.
