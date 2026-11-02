# 0043 — Contours above vegetation

**Date:** 2026-11-02

## Question

Should contours draw above the vegetation fill, instead of under it?

## What we did

Stock Topo50 draws `vegetation map` above `contour`. The stock fill is pale, so the brown lines still read. Accessible native and scrub fills are darker, and scrub is hatched, so those fills hid the contours on the cold-spring square.

`draw_order` in `tools/style-topo50.json` is `vegetation map` below `contour`. The QGIS apply step moves that layer in the layer tree so it sits immediately under `contour`. Custom-order stays off. Vegetation alpha stays 180 native and 200 scrub. `vegetation_line map` stays above contours. `landcover map` was already under `contour`. The vector style already paints contours after vegetation fills.

The four accessible squares were drawn again at 600 dpi.

## What we found

On the cold-spring square the brown contour lines now sit on top of the green fills. The hatch still reads under the lines. Forest versus scrub still reads. The estuary square and the closed-track square do not change this pair.

## What changed

- `tools/style-topo50.json` holds the draw-order pair.
- `tools/override_topo50_project.py` moves `vegetation map` under `contour`.
- The four accessible square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

Accessible sheets now diverge from LINZ layer order on this one pair. Stock order stays. Opaque vegetation fills are a later choice.
