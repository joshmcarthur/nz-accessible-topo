# 0047 — Vector form of the raster style

**Date:** 2026-11-02

## Question

Can the MapLibre style be the raster style on Shortbread tiles, rather than a fork of LINZ `topographic-v2`?

## What we did

Josh rejected a vector style that is a fork of `topographic-v2`. The vector style is now the raster style in `tools/style-topo50.json` on LINZ Basemaps Shortbread tiles.

`upstream/linz-topographic-v2.json` is the catalog: sources, glyphs, layer ids, filters, and paint for layers the style file does not name. `tools/build_style.py` writes owned paint from the style file onto that catalog. Roads, water fills, and buildings keep LINZ paint. That matches the QGIS apply step.

`P` no longer holds contour hexes. Vector zoom width stops stay in the builder. They are not a palette. Token export reads contour inks from the style file.

The four squares were drawn again at 600 dpi. The inks did not change.

## What we found

C1–C6 pass. `P` holds no colour hex. R-15 Met when is true. The vector face stays Open Sans until macron glyph PBFs exist.

## What changed

- `tools/build_style.py` writes owned paint from the style file. `P` holds no colour hex.
- `tools/export_tokens.py` reads contour inks from the style file.
- `styles/accessible-v0.json` and `styles/accessible-v0-multidir.json`.
- `docs/recommendations.md` R-15 text.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

Layers the JSON does not name can still change when upstream LINZ paint changes. R-13 stays open. The next step is Step C.
