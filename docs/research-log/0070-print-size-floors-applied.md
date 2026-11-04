# 0070 — Print size floors applied

**Date:** 2026-11-05

## Question

Can the F-31 floors (0.35 mm lines, 1.4 mm area marks) go onto every owned
stroke and symbol without swamping tracks or the contour mesh?

## What we did

Adopted `sizes.line_floor_mm` 0.35 and `sizes.symbol_floor_mm` 1.4 in the
style file. After the owned-ink colour rewrite, apply raises SimpleLine and
fill outlines in stream, shelterbelt, or grid ink, and SimpleMarkers whose
size is greater than 0. A thicker stroke stays. Scrub plants use 1.4 mm.
Contours, tracks, and the closed-track × are not those inks, so they stay.

## What we found

Stock ice contours and coastline are process-blue, so they take the stream
ink and the line floor. Lake and swamp outlines in that ink take the floor
too. Gold casings stay 0.6 mm.

The first paint raised every owned SimpleMarker, including 0.05 mm
vegetation_point tree dots, to 1.4 mm. Those dots overlap into opaque
shelterbelt blobs and hide contours (cell `1568000-5166000`). The symbol
floor now applies only to PointPatternFill markers. Standalone point
markers stay at stock size.

G5 and G6 stay open until the 4 km cells are reviewed.

## What changed

- `tools/style-topo50.json`: `sizes`, `water.stream_width_mm` 0.35,
  `vegetation.scrub_dots.size_mm` 1.4
- `src/nzat/qgis/patch_owned_lines.py` raises owned sizes
- Removed `patch_stream_width` (water_line-only)
- F-31, R-04 print widths, this log

## Confidence & gaps

Grade C floors. Confirm on `render/bx24-4km/`. A steep sheet is still OQ-09.
