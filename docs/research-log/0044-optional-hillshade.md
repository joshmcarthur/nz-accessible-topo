# 0044 — Optional hillshade overlay

**Date:** 2026-11-02

## Question

Can R-03 live in the shared style file as an overlay that turns on when a DEM is dropped beside the project?

## What we did

Hillshade is not baked into the map inks. `hillshade` in `tools/style-topo50.json` holds azimuth 337.5°, altitude 45°, QGIS multidirectional true, `raster_file` `dem.tif`, and `painted` true.

The QGIS apply step writes those lights onto the project elevation shader. The shader stays off while `dem.tif` is missing. A missing file is not an error. Set `painted` to false to disable the overlay even if the file is present.

The square renderer copies that shader. If `dem.tif` is present at draw time, it loads the DEM.

The vector build reads the same azimuth and fill lights. `hillshade_direction` is no longer in `P`.

No DEM was added. The four accessible squares were drawn again. The log says `hillshade off: no dem.tif`. Stock squares were not redrawn.

## What we found

R-03 Met when needs shade generated at 337.5° and checked on an Alpine sheet and a lowland sheet. This step has no DEM. R-03 stays open.

## What changed

- `tools/style-topo50.json` holds `hillshade`.
- `tools/override_topo50_project.py` turns the shader on only when `dem.tif` sits beside the `.qgs`.
- `tools/build_style.py` reads the azimuth and fill lights.
- `tools/render_square.py` copies the shader and loads a present DEM.
- The four accessible square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

Drop a GeoTIFF named `dem.tif` beside the project to rasterise with shade. QGIS multidirectional is the project boolean, not the three MapLibre fill azimuths. B-26 is still unanswered. The next step is R-14.
