# 0100 — Trees legend swatch at legend_size_mm

**Date:** 2026-11-06

## Question

Tree points on the map stay **0.2 mm** (log 0070). F-31 needs **1.4 mm** on the
legend. How do we draw the trees row without changing map symbology?

## What we did

Added a **trees** swatch to `legend_swatches.py` (box matches symbol_rows). After
the applied `vegetation_point map` style is copied onto memory features,
`render_legend.py` sets the SvgMarker size from
`vegetation.trees.legend_size_mm` (**1.4 mm**). Map apply still uses
`size_mm` **0.2**.

Marked the `/symbols/` trees row **done** with `redrawn=True`.

## What changed

- `src/nzat/qgis/legend_swatch_marker.py`
- `src/nzat/qgis/render_legend_main.py`
- `src/nzat/qgis/legend_swatches.py`
- `src/nzat/site/symbol_rows.py` (trees)
- `tests/qgis/test_legend_swatches.py`

## Confidence & gaps

Re-run `render_legend.py` after apply so `trees-ours.png` updates. Orchard and
mangrove rows are still stock art.
