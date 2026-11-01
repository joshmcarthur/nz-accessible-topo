# 0023 — Correction: the starting point is `topo-raster-gridded`, not `topographic-v2`

**Date:** 2026-11-01

## What went wrong
The intent was to make LINZ Basemaps' **`topo-raster-gridded`** style more
accessible. From log 0004 onward we audited and transformed
**`topographic-v2`** (the vector topographic basemap) instead. The error was
ours in log 0004: we chose the vector style without confirming which LINZ
layer was meant.

## What `topo-raster-gridded` is
`config/style/topo-raster-gridded.json` (vendored in `upstream/`): a single
`raster` layer of pre-rendered **Topo50** WebP tiles with the NZTM grid baked
in, plus a client-side hillshade (315°, the same as `topographic-v2`).
A MapLibre style can only change such a layer globally (brightness,
contrast, saturation, hue rotation, opacity) — not contours, fonts,
italics, symbols or individual colours.

## Where Topo50's cartography actually lives
- `linz/topographic-qgis` (MIT, public): the Topo50 QGIS project — 43 layer
  QMLs, 75 SVG symbols, a six-ink spot palette (`nztopo50_colours.gpl`:
  black, warm red, PMS 151 orange, process blue, PMS 367 green, PMS 442 grey,
  plus tints) and the Nimbus Sans LINZ fonts (AGPL-3.0 with exemption).
- `linz/topographic-system` (MIT): the containerised QGIS production
  pipeline (`packages/map`: `map prepare` / `map export`).
- Labels are **data-defined** (carto_text `text_font`, `style`, `size`).
  Sample: 67% italic, mostly condensed italic at 5.5–6.5 pt (F-30).
- The project's elevation shading is off; relief appears to come from
  elsewhere — whether served tiles bake it in is open (B-26).

## Impact assessment
| Work | Status |
|---|---|
| Research: sources, F-01–F-29, R-01–R-17 | **Valid** — it's about Topo50 and map readers, not a specific style |
| Print legend audit, real-render simulations (log 0019) | **Valid and now central** — that *is* the raster's cartography |
| `accessible-v0` vector styles, `build_style.py`, C1–C6 | **Valid but secondary**: a web-vector track, kept and gated, not the product |
| Synthetic scene renders (log 0017) | Secondary: compare vector styles only |
| Atkinson Ō/ō gap | Less urgent: QGIS shapes text with HarfBuzz (F-28) |
| Site, Sankey, comparisons, S1–S3 | **Valid**; the Sankey's "style changes" column currently describes the vector track |
| Preview / screenshot tooling | Needs raster support (B-03) |

## What we did in this entry
- Vendored `topo-raster-gridded.json`.
- Cloned and analysed `linz/topographic-qgis`;
  `tools/analyse_qgis_project.py` → `docs/current-state/topo50-qgis-cartography.md`.
- Added F-30 (labels), R-18 (fork the QGIS symbology and re-render; primary
  deliverable), sources S-LINZ-RASTER-STYLE, S-LINZ-TOPO-QGIS,
  S-LINZ-TOPO-SYSTEM, S-OUR-QGIS-ANALYSIS.
- Re-planned `BACKLOG.md`: new primary items B-22–B-29; vector items moved to
  a "Secondary" column.
- **Deliberately not done:** changing the raster style's client hillshade to
  NNW. If the tiles carry baked NW relief, that would create two conflicting
  light sources. Check first (B-26).

## Confidence & gaps
- The label statistics come from a small test-area sample.
- We haven't yet run LINZ's container or obtained sheet data (B-22, B-23).
- Font licensing for modified fonts is unresolved (B-28).
