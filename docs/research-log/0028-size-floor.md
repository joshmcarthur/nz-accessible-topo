# 0028 — Label size floor

**Date:** 2026-11-02

## Question

Do the accessible raster style and the vector style meet R-09?

## What we did

Added `labels.web_floor_px` 10 and `labels.place_name_floor_px` 11 to `tools/style-topo50.json`. Pointed `tools/build_style.py` at those floors. Rebuilt the vector style. Regenerated the accessible QGIS project. Rendered four 1 km squares at 600 dpi. 1000 m on the ground is 472 px. Stock and accessible use the same extent and the same scale.

## What we found

Print text layers use `max(7, coalesce("size", 7))`. The 6 pt spot-height floor stays in the style file. It applies when the layer name contains `relief_point`. Those labels are off. This step did not measure the size field in the data.

Place names in the vector style are at least 11 px. Other web labels stay at a 10 px floor.

These sizes differ by less than 20%:

- `Place-Label-Suburb` is 11 px. `Place-Label-Locality` is 11 px. The ratio is 1.00.
- `Place-Label-Locality` is 11 px. `Place-Label-Town` is 12 px. The ratio is 1.09.
- `Place-Label-Island-12` is 12 px. `Place-Label-Island-8`, `Place-Label-Island-6`, and `Place-Label-Island-4` are 14 px. The ratio is 1.17.

`Place-Label-Town` is 12 px. `Place-Label-City-14` is 15 px. The ratio is 1.25.

R-09 says adjacent hierarchy levels differ by at least 20%. It does not say which layers are one hierarchy. This step does not pick a spread.

The estuary square has no black question marks. The black marks were missing landcover SVGs. The sand symbol and the swamp symbol now sit beside the project. The estuary name is blue letters. `CurvedLabelMode` is Default (0). The words "Estuary" and "Heathcote" both draw. "Heathcote" follows the bend upside down. Stock still uses `StretchWordSpacingToFit`. Stock draws "Estuary" upright. This step does not pick a new placement value.

The pair audit is unchanged. R-09 does not own those pairs. Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/style-topo50.json` holds the web size floors.
- `tools/build_style.py` reads those floors.
- `tools/render_square.py` draws one 1 km square from inside the map container.
- The four squares are in `site/src/data/comparisons.json`. Each variant has the six conditions.

## Confidence & gaps

R-09 stays open. The floors are in. The hierarchy step is not met. The next step is that choice. Do not start R-07.
