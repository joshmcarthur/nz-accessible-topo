# 0091 — Accessible rasters for every Topo50 sheet

**Date:** 2026-11-05

## Question

Can we draw the accessible style for all 445 Topo50 sheet faces as
georeferenced rasters, from the national GeoParquet cache we already have?
How long does it take, and how much disk does it use?

## What we did

- Sheet index: `nztopo50_map_sheet.parquet` from the stock project
  (445 rows: `sheet_code`, `sheet_name`, geometry in NZTM EPSG:2193).
- Every sheet in the index is 24 km × 36 km. At 1:50,000 that is
  480 × 720 mm. At 150 dpi that is 2835 × 4252 px. The tool computes the
  size from each sheet bbox, so an odd sheet would get its own size.
- 41 codes are not plain `AA00` codes, for example `AS21/AS22` and
  `BJ43ptsBJ42,BH42,BH43`. The file name replaces each run of other
  characters with `_` (`AS21_AS22.tif`).
- New tool `tools/render_sheets.py`. One QGIS 4.2.3 process loads the
  project and fonts once. Then it loops over the sheets. Each face goes to
  an RGB GeoTIFF in EPSG:2193, DEFLATE with PREDICTOR=2, tiled 256 × 256.
  `render_square.py` and the new tool share `open_map` and `render_image`.
- Project: a new applied copy in
  `~/Projects/github.com/linz/topo50-bx24/squares/accessible-sheets/`.
  It has the same relative symlinks to `../../.cache` as
  `squares/accessible`, a copy of `symbol/`, and `nztopo50.qgs` from
  `override_topo50_project.py`, applied from commit `6eda74b`.
- Test sheets: BQ31 Wellington (coast and city), BX24 Christchurch, CA11
  Aspiring Flats (alpine, ice).

## What we found

| Sheet | Time | GeoTIFF |
|---|---|---|
| BQ31 Wellington | 13.1 s | 9.1 MB |
| BX24 Christchurch | 17.8 s | 15.5 MB |
| CA11 Aspiring Flats | 50.1 s | 24.4 MB |
| AT24 Cape Reinga (mostly sea) | 4.0 s | 4.9 MB |

- `gdalinfo` shows EPSG:2193, origin at the sheet's north-west corner, and
  8.466 m pixels. The pixels are not quite square (8.4656 × 8.4666 m)
  because each side rounds to a whole pixel.
- The styling holds on the coast and in the Alps. The sea, the urban fill,
  ice, braided rivers and the grid draw as on BX24. We saw no new defect.
- Projected run: about 25–30 s a sheet on average, so 3–4 hours for 445
  sheets. About 15 MB a sheet, so about 6–7 GB. The disk had 107 GB free.
- The uncommitted urban-halo work in the tree (an `overlay_intersects()`
  buffer colour) hangs the render. The label thread waits for the main
  thread. The main thread waits in `waitForFinished()`. So this run uses
  the project applied from `6eda74b`, not the working tree.

## What changed

- `tools/render_sheets.py`, `src/nzat/qgis/render_sheets_main.py`.
- `open_map.py` and `render_image.py`, taken out of
  `render_square_main.py` with no change in behaviour.
- Pure helpers `sheet_pixel_size`, `sheet_geotransform` and
  `sheet_file_name`, with tests.
- Output (not committed):
  `~/Projects/github.com/linz/topo50-bx24/sheets/accessible-150/`.
  One `.tif` per sheet, `progress.tsv` (code, name, size, seconds, bytes),
  `render.log`, and `run.sh`.
- To resume, run `run.sh` again. It skips each sheet whose `.tif` exists.
  A file is written as `.tif.part` and renamed when it is complete.

## Confidence & gaps

Grade B for the size and the georeference. Grade C for the time and disk
total: it comes from four sheets.

- There is no `carto_fit.json` for any sheet but BX24. Flat names on the
  other sheets render where QGIS places them, not pinned (logs 0086–0088).
- No hillshade. There is no `dem.tif` beside the project.
- Each sheet is drawn alone. A name near a sheet edge can be dropped or
  placed differently on the two neighbours. A tile set (B-27) needs a
  buffer or one drawing per region.
- Contour numbers can read upside down (B-37 is still open).
- The `pt` sheets overlap their neighbours, so some ground is drawn twice.
