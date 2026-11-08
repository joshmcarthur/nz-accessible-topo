# 0109 — Bivouac tent at character height, no lime disc

**Date:** 2026-11-08

## Question

On the Shannon cover square, is the bivouac tent large enough next to its
name, and why did a lime disc sit under it?

## What we did

Josh reviewed `render/legend-cover/1820000-5506000-accessible.png` (BN34
Shannon, Map5View-all). The tent was tiny versus 7 pt type. The name sat on
the mark. A lime disc sat behind it.

The tent stays `structures.bivouac.size_mm` 2.5 mm (one 7 pt character; same
band as redoubt). The SVG `viewBox` hugs the strokes. A carto_text name that
contains `Bivouac` or `Bivvy` takes `labels.carto_point.offset_mm` (2.5 mm)
on the flat-name baseline. That offset is a static millimetre distance. It
does not use `overlay_intersects()`.

Map5View-all no longer turns on a layer in `map.all_layers` when `{name} map`
exists. The categorized `structure_point` copy stays off. `structure_point
map` still draws the tent.

## What we found

The lime disc was not the SvgMarker fill. Map5View-all had been turning on
`structure_point` (unique-value colours) over `structure_point map`. Parquet
has `type`, not `feature_type`, so those points hit the QGIS default lime.

A `param(fill)` bind on the tent SVG broke the glyph (QGIS drew a speck).
Keep `fill="none"` and QGIS fill `0,0,0,0` (log 0106). Skip the non-map
copy instead.

Josh: "Happy!" The Shannon square shows an open tent about one character
tall, the name off the mark, and no lime.

## What changed

- `tools/style-topo50.json`: `structures.bivouac.size_mm` 2.5;
  `labels.carto_point.offset_mm` 2.5
- `src/nzat/qgis/symbols/nztopo50_bivouac.svg` (tight viewBox)
- `src/nzat/qgis/patch_map_themes.py` (skip `{name}` when `{name} map` exists)
- `src/nzat/qgis/carto_flat_line_expression.py`, `patch_carto_point_labels.py`,
  `defaults.py`
- `src/nzat/site/symbol_rows.py` (bivouac mark 2.5 mm)
- Tests and `docs/style-topo50.md`

## Confidence & gaps

The offset matches the name string, not a spatial join. A hut named without
`Bivouac`/`Bivvy` does not move. Other extra cover squares are not signed
off. Fumarole stays proposed (log 0096). N-8 stays deferred. `/symbols/`
export was not re-run in this pass.
