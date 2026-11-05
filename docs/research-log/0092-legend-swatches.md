# 0092 — The sheet legend shows the accessible swatches

**Date:** 2026-11-05

## Question

The `tiff-50` layout holds the sheet legend. How is that legend built?
Can the accessible sheet show our symbols and inks in it?

## What we did

- Read the `tiff-50` layout XML in the stock project.
- Rendered each legend swatch from the applied map layers with QGIS 4.2.3.
- Drew those swatches over the stock legend image.
- Exported the whole `tiff-50` page of the applied BX24 project at 150 dpi.
- Compared the legend crops before and after.

## What we found

### How the stock legend is built

- The layout has no `QgsLayoutItemLegend`. No layout item is linked to the map layers.
- The legend is one picture item. Its file is `./topo-legend-1.tif`.
- The item is 98.05 × 476.46 mm at (97.36, 73.96) mm on the page.
- The image is 2323 × 11247 px at 600 dpi, RGB, WEBP-compressed.
- The labels, leader dots, headings and the "Important information" box are pixels in that image.
- So a map style change never reaches the legend.
- The file is not in the project item. The `squares/` projects do not have it. Their page exports draw a red cross where the legend goes.
- The image is in `linz/topographic-system` at `e2e/assets/topo-legend-1.tif` (log 0019).

### The approach

- The legend labels stay. They are the stock image.
- `tools/render_legend.py` reads the stock image with GDAL. Qt does not read the WEBP TIFF.
- For each swatch it clears a box in the swatch column and draws the applied map there.
- Each swatch is one or more features in legend pixels. `src/nzat/qgis/legend_swatches.py` lists them.
- Each feature has the attributes of a real feature of its class, for example `lane_count` 2, `surface` sealed, `highway_number` 1.
- The tool copies every Map5View layer that reads that table onto a memory layer. The copy keeps the layer filter and the whole layer style. Map order stays.
- The swatch draws at 600 dpi and 1:50,000. So the swatch is the sheet size of the symbol.
- A renderer clone drew no state highway number. A full style copy (`exportNamedStyle`, `importNamedStyle`) does.
- The output is `topo-legend-accessible.png` beside the project.
- The apply step points the legend picture at `./topo-legend-accessible.png`.
- Layout text is not changed. It stays Nimbus.

### Swatches redrawn (18 rows)

- State highway: `#E31A1C` fill, dark casing, white shield, `#940000` number.
- Four lanes, two lanes, narrow road, sealed: `#EC7000` fill with casing.
- Metalled: `#EC7000` with white dashes. Unmetalled: the double line.
- Vehicle track, foot track: thin black dashes.
- Closed track: foot dash with the `cross2` mark.
- Poled route and track connector: both draw as a foot track.
- Index contour `#7A5542` 0.35 mm with the upright "100" number and its halo.
- Intermediate contours `#B08872` with index-ink casing.
- Ice contours: `#004C99`, the 100 m line heavier. The map labels it. The swatch does not, like the stock row.
- Supplementary contour: a solid intermediate line.
- Watercourse 0.25 mm and drain 0.15 mm in `#004C99`.
- Native, exotic (two rows), scrub with plant marks, scattered scrub.
- Shelter belt `#1D9D00`.

### The page export

- QGIS 4.2.3 exported the whole `tiff-50` page of the applied project at 150 dpi (4500 × 6300 px) in 47 s.
- The map item extent was set to the BX24 sheet bbox, as the LINZ `qgis_export.py` does.
- The legend draws in its place. The red cross is gone.
- The page title still says BW15 Ōkārito. This export did not set the other layout variables the LINZ exporter sets. The two logo pictures are missing in `squares/`.
- `tools/render_legend.py` takes about 7 s for 18 swatches.

### Map findings from the swatches

- Open foot tracks drew the closed-track cross. Status is NULL on open tracks. QGIS 4.2.3 reads a NULL `enabled` value as on. Fixed in commit `7325b52` with `coalesce("status", '') = 'closed'`.
- The sheet rasters of log 0091 were applied from `6eda74b`, before that fix. Every foot track in them has the cross.
- The map does not tell poled route and track connector from a foot track. Stock print draws dots.
- The map does not dash supplementary contours. Stock print does.
- The map draws coniferous marks on non-coniferous exotic forest.
- Scattered scrub marks are very pale at sheet size. They draw only where a whole 5 mm grid cell fits.
- Springs are on `water_point`. Map5View hides that layer, so the sheet draws no spring.
- Map symbols are thinner than the stock print legend. The two-lane fill is about 0.5 mm on the map and 0.85 mm in the stock legend.

### Rows that still show stock looks

Stock looks stay in these rows. They use stock inks or symbols the map no longer uses, or the map has no simple class for them.

1. Tunnel, bridge, ford, gate and footbridge rows: stock orange `#F29400`-like road fills and stock `#009EFF`-like blue.
2. Railway rows: black. Check them against `railway_line map`.
3. Level crossing, road over railway, railway over road: stock road fill.
4. Residential area, buildings, homestead: the stock urban picture.
5. Depression contours and shallow depressions: stock `#FF7F00`-like orange.
6. Elevation in metres: italic stock spot heights. The map draws them upright, black, 6 pt.
7. Trig, cliff, rock, stopbank, embankment, saddle, cave: black symbols. Check them against `relief_line map` and `relief_point map`.
8. Water features picture (coast, shoal, sand, swamp, wharf, marine farm): stock blue.
9. Canal, dam, waterfall, stream disappearing: stock blue.
10. Cold and hot spring: stock blue and orange. The sheet draws no spring.
11. Fumarole, geothermal bore: stock orange.
12. Trees, orchard, mangroves: stock green.
13. Buried gas pipeline: stock orange.
14. Moraine, scree: black stipple.

## What changed

- `src/nzat/qgis/patch_tracks.py`: the closed cross reads `coalesce("status", '') = 'closed'` (commit `7325b52`).
- New `tools/render_legend.py` and `src/nzat/qgis/render_legend_main.py`.
- New `src/nzat/qgis/legend_swatches.py`: the swatch table.
- New `legend_wkt.py`, `legend_box_extent.py`, `legend_metres_per_px.py`: pixel to ground.
- New `patch_legend_picture.py`. `apply.py` calls it.
- Tests: `tests/qgis/test_legend_swatches.py`.
- `docs/style-topo50.md`: the legend step.
- Before and after crops: `docs/visuals/12-legend-before-after.png`. Stock legend on the left, accessible legend on the right, at 300 dpi.

## Confidence & gaps

- The swatch boxes come from the ink rows of the stock image. A different legend image needs new boxes. The tool stops when the image size is not 2323 × 11247.
- Swatches are straight lines. Stock swatches have bends. The symbol is the same.
- The swatches draw at sheet size. Josh to decide: keep sheet size, or draw at the stock print size.
- The legend labels say what stock print draws, for example "Poled route". The map does not draw all of those classes.
- A new legend row, for example the closed-track cross note, needs new label text. That is layout text. Not done. Josh to decide.
- The plan for the stock rows is the numbered list above. Rows 1, 3, 5 and 9 need only an ink match and a table. Rows 4 and 8 are pictures and need new sample geometry.
