# 0106 — Legend swatches: no lime disc, relief ticks draw

**Date:** 2026-11-06

## Question

Why were some N-6 `/symbols/` crops a lime disc, or a white box, at sheet size?

## What we did

Josh flagged the lime background. We re-applied `$W/accessible/nztopo50.qgs`,
redrew the legend with `--theme Map5View-all`, and exported `/symbols/`.

Stroke-only SvgMarkers now use fill `0,0,0,0`. A leftover SimpleMarker circle
under a gate bar is dropped. Locked and unlocked gates keep the black bar;
the locked gate still has the 0.6 mm square. Saddle reads parquet `type`.
Inactive renderer rules turn on only for `relief_line` and `bridge_line`.
Swatch memory layers do not grow a fake `feature_type` field.

## What we found

QGIS paints SvgMarker `color` as a disc when the SVG is `fill="none"` and does
not use `param(fill)`. That disc is the default lime. Church does not show it
because its SVG has an opaque black fill. Trees bind `param(outline)`.

Cliff, slip, stopbank, cutting, embankment, and both bridges were empty
because those rules sit at stock `checkstate=0`. Enabling them on the swatch
copy draws the ticks. MarkerLine interval was already short enough.

Saddle was a 0.3 mm height dot because the filter used `feature_type` and the
parquet column is `type`.

Weir, breakwater, and cemetery went mint when the swatch copy invented
`feature_type`. Those layers categorize on `feature_type`, but the sheet
features only have `type`, so they hit the NULL category (process-blue
`65,76,219`, cemetery cyan `129,234,234`). A new `feature_type` field matched
unique QGIS mint colours the sheet never paints.

## What changed

- `src/nzat/qgis/patch_structures.py`, `patch_relief_point.py`, `patch_springs.py`
- `src/nzat/qgis/render_legend_main.py`, `legend_swatches.py`
- `tests/qgis/test_legend_swatches.py` (empty, lime disc, high-G mint)
- `tests/qgis/test_patch_structures.py`, `test_patch_relief_point.py`,
  `test_patch_springs.py`
- `site/public/symbols/*-ours.png`

## Confidence & gaps

Gates, lighthouse, mast, cliff ticks, and saddle arcs now match the map at
1:50,000. Fumarole stays proposed (log 0096). Waterfall is a hollow black
circle. Cemetery is still a cyan slab, not the LINZ dashed crosses. Weir and
breakwater are process-blue NULL bars, not the black bars in `symbol_rows`.
Rock outcrops stay a brown circle (`landcover_point map` is absent). The
locked-gate square is easy to miss at 0.6 mm.
