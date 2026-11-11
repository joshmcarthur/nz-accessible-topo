# 0117 — Web map tiles from the sheet rasters

**Date:** 2026-11-12

## Question

Can the accessible style be served as raster map tiles, made from the LINZ
`nztopo50` project and GeoParquet layers with tools we already have? How
big is one sheet?

## What we did

- Drew sheet BX24 at 300 dpi with `tools/render_sheets.py`: the stock
  project with the stock fonts, and the applied accessible project
  (`squares/accessible`, which has the BX24 name fit). Each sheet is
  5669 × 8504 px, 4.23 m a pixel, EPSG:2193.
- New tool `tools/make_tiles.py`. It runs four commands: `gdalbuildvrt`
  joins the input sheets; `gdal_translate -of MBTILES` warps them to web
  mercator WebP tiles; `gdaladdo` builds the lower zooms; `pmtiles convert`
  writes one PMTiles file. An `--extent` in NZTM metres crops the area.
- Built the whole sheet and a 12 km area (1568000–1580000 E,
  5168000–5180000 N: Cashmere, the Port Hills, Lyttelton and part of the
  estuary) for both styles.

## What we found

| Step | Time | Size |
|---|---|---|
| Draw one sheet at 300 dpi | 35 s | 33 MB stock, 40 MB accessible (GeoTIFF) |
| Tile the whole sheet, zoom 10 to 15 | about 15 s | 21 MB a style, 1598 tiles |
| Tile the 12 km area, zoom 11 to 15 | about 5 s | 4.4 MB a style, 314 tiles |

- 300 dpi gives zoom 15 as the top zoom (3.46 m a pixel at this latitude
  against 4.23 m in the sheet), so the top zoom is a small upsample.
  150 dpi stops at zoom 14.
- A stock tile and an accessible tile with the same z/x/y show the same
  ground. The NZTM grid lines lean a little, because the tiles are web
  mercator.
- At 21 MB a sheet, all 445 sheets are about 9 GB a style at zoom 15. That
  is an estimate from one sheet; sea sheets are smaller.
- **Decision (Josh, 2026-11-10):** the repo holds a small demo area only.
  The 12 km area is in `site/public/tiles/` (8.8 MB for both styles). The
  whole-sheet files stay outside the repo.

## What changed

- `tools/make_tiles.py`, `src/nzat/render/make_tiles.py`,
  `tests/render/test_make_tiles.py`.
- `site/public/tiles/bx24-stock.pmtiles`, `bx24-accessible.pmtiles`.
- `tools/README.md`.

## Confidence & gaps

Grade B for the pipeline on one sheet. Grade C for the national size.

- Each sheet is drawn alone, so a name at a sheet edge can differ between
  two sheets (log 0091). One sheet does not show this.
- Names off BX24 are not fitted (no `carto_fit.json`).
- The 445 sheet rasters from log 0091 are 150 dpi and predate logs 0094 to
  0116. A national tile set needs them drawn again.
- No tile server. A PMTiles file needs a client that reads byte ranges
  (MapLibre with the pmtiles protocol). The site page is the next step.
- `pmtiles convert` writes a wrong centre longitude in the metadata. The
  bounds are right.
