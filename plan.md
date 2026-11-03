# Plan

## Objective

Render Topo50 sheet BX24 with LINZ's map container, then change QML labels and symbology and render that sheet again. Leave the Nimbus Sans LINZ files unchanged. The accessible sheet uses Atkinson Hyperlegible Next with Ō/ō added.

## Scope

In scope: B-28, B-22, B-23, B-25, B-11, B-24.

Out of scope: B-01, B-02, B-03, B-26, B-29, tile serving, and site work beyond the evidence-graph refresh that a recommendation edit requires. B-11 is in scope: it is the Atkinson swap on the accessible sheet.

## Approach

Use the pinned STAC project for topographic-qgis @ c0edcfc:

https://d1jzh93b1t1cv.cloudfront.net/qgis/nztopo50/commit_prefix=c/commit=c0edcfc8c8b4321359cd9dbc2f66cd8d0e539a78/nztopo50.json

Clone linz/topographic-system outside this repo, record the commit, and build packages/map with its container script. Start Colima first. Mount the cache on the host.

map prepare and map export download the national GeoParquet layers the project links. QGIS clips to BX24 at export. The cache, the upstream checkouts, and full-resolution exports stay out of git. Commit a review PNG. Commit the PDF when it is under 20 MB.

B-25, B-11, and B-24 are QML transforms on a pinned checkout, then map deploy, then the same container. Italic style names map to upright faces of Atkinson Hyperlegible Next. The face is built at render time by tools/patch_atkinson_omacron.py from the OFL sources. The family name is NZAT Legible Test. There is no Narrow master, so stock Narrow labels use the regular width. The size floor is 7 pt, and 6 pt for spot heights. Symbology follows R-04, R-10, R-11, and R-17. Colours go through palette_audit.py in pair mode.

## Next steps

1. Log the B-28 decision. Done in the working tree. Not committed yet.
2. Stock BX24 render (B-22, B-23). Done. Layout name is tiff-50. topographic-system pin is 3b6ec60. Not committed yet.
3. Upright labels, size floor, and the Atkinson swap (B-25, B-11). The transform is `tools/override_topo50_project.py`. It edits map-layer labels only. The print layout stays on Nimbus.
4. Symbology (B-24) is the same transform, one layer at a time. See the decision on the sheet image. The accessible render is in output-accessible/. It is not accepted. Along-line water names are black question marks (log 0026). B-25, B-11, and B-24 stay open.

## Constraints

Free disk was about 38 GB when this plan was approved, and Colima was stopped. Stop a render if free space would fall below 8 GB. The national contour parquet is 1.75 GB. BX24 is the print-legend sheet and is flat. A steep sheet is later work (OQ-09).

The exported PNG is the full `tiff-50` layout. It includes the legend, the sheet index, the scale, and the title block. Do not judge a symbology change from that composite alone. Change the map layer. Leave the layout items alone. The legend swatch updates because it is drawn from the layer.

## Style loop

**Status:** current work
**Date:** 2026-11-02

The full-page PNG is the wrong comparison. One style file drives the raster project, the vector style, and the site pictures.

Dispatch prompt: `docs/plans/2026-11-02-style-loop-prompt.md`. One paste does one step. The status file is `docs/plans/style-loop-status.md`.

Next step is Step A: create `tools/style-topo50.json` from the current override values. Do not invent colours. Then one recommendation per later paste.

The proof renders are four 1 km squares at 600 dpi, map face only:

- 1577000 E, 5178000 N — estuary water names
- 1577000 E, 5172000 N — Port Hills contours
- 1569000 E, 5165000 N — the cold spring
- 1584000 E, 5173000 N — the closed foot track

The old line that put site work out of scope does not cover these comparison images. They are outputs of the style, built by `tools/build_site_assets.py` under the six conditions in `site/src/data/conditions.json`. B-01, B-02, push, tile serving, and user testing stay out of this loop.

R-04, R-05, and R-06 are settled for the style loop. See the decision of the same date. The question marks stay a render defect on the first estuary square.


The square renderer draws the Map5View layers. That is the tiff-50 map theme. It does not draw layers that theme hides. Along-line labels keep the official `charplace` value. Do not set CurvedLabelMode to 0.

Square draws use the Mac QGIS app. The sheet export stays on the map image.

Square draws use `/Applications/QGIS-final-4_2_3.app` (QGIS 4.2.3). The sheet export stays on the map image. Set `PROJ_DATA` or the square is white.
R-09 place ranks: Suburb and Locality are 11 px. Town is 14 px. City is 17 px. Island layers stay zoom bands.

R-07 draws the label buffer the text style already has. It sets that buffer opaque. It darkens a label ink that is below 4.8:1 against that buffer. It does not use the hand-picked #005C8F.
R-10: vector vegetation colours come from the style file. Scrub is #A3CC90. Scattered is #E0EDD8 plus nzat:scattered_stipple. Raster keeps the stock scattered dots and the scrub hatch. Do not add a fill under those dots. Native forest stays for R-17.
R-17: vector native fill and spring inks come from the style file. LINZ spring icons stay.
R-01 is met. Intermediate casing 0.2 mm `#8A4F1C`, fill `#C4814B`, index 0.45 mm. Josh accepted the Port Hills step.
R-08: one attempt. `labels.letter_spacing_em` is 0.05. Vector reads it. Raster along-line labels stay at normal spacing. Leave provisional. Next is R-12.
R-12: `tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false. Do not pick an access ink. Do not overlay access data.
R-03: hillshade is an optional overlay. Azimuth 337.5°. `painted` true. Raster file `dem.tif` beside the `.qgs`. Missing file is not an error. Do not bake shade. Vector reads the same numbers.
R-14: pair colours that live in `tools/style-topo50.json` are dotted paths. `palette_audit.py` resolves them. C6 stays on `pairs-accessible-v0.json`. Do not fail C6 against `#EA6300`.
R-13 stays open. Do not invent greyscale or high-contrast inks. The site grey condition is a simulation, not a second painted style.
R-15: the vector style is the raster style on Shortbread tiles. `topographic-v2` is the catalog only. Owned paint comes from `tools/style-topo50.json`. Unowned layers keep LINZ paint. `P` holds no colour hex. Next is Step C.

Carto text placement: flat one-line names slide on a bounded horizontal line at the stock baseline, or flip below it (log 0042). The `map` container runs QGIS 4.2.2, which has `OverPoint`.

Vegetation map draws below contour. The apply step moves that layer in the layer tree. Custom-order stays off. Vegetation alpha stays 180/200. `vegetation_line map` stays above contours. Vector style already paints contours after vegetation fills.

Carto text fit (approved 2026-11-03, in progress). QGIS tests label boxes yes or no and cannot minimise ink overlap. Plan:

1. Apply step reads an optional `carto_fit.json` beside the `.qgs` (drop-in, like `dem.tif`). Each entry: row `id`, `x`, `y`, `lines` (1 or 2). Those rows get a data-defined position and text form on the flat rule. Missing file changes nothing. Fit data stays out of the style file.
2. `tools/fit_carto_labels.py` (QGIS Python, no new packages): render the face, read `QgsLabelingResults`, cluster flat names whose boxes collide, try one/two lines, above/below, and 0.25 mm sideways steps within the allowance. Score on glyph outlines with halo, plus a small move cost. Neighbours: flat names as glyph outlines, curved names as QGIS per-letter boxes. Point symbols are not neighbours in v1; stop and ask if a name lands on one. Write `carto_fit.json` in topo50-bx24.
3. BX24 fit run, renders, research log, lore decision.

Step 1 and the long-name wrap and 0.85 line height are committed (ab4af71). Step 2 is committed (5d11a61). Weights: ink on ink 10, ink in a halo 3, halo on halo 1, move 40 per mm. The step grid includes 0. Step 3 is done in eaa82bf.

Carto text spread (approved 2026-11-03). Stock stretches words or letters to fill the baseline. b9f78d2 set every stretch mode to default, so names lost their spread. The flat filter also took curved area names (Banks Peninsula) onto a short line.
A. Curved rule: keep the stock stretch mode when the name is one line and the baseline is longer than the estimated text width (chars x size x advance_em). Else default. One shared width helper with the flat line.
B. Flat filter adds `num_points($geometry) <= 2`. 30 curved one-line rows on BX24 go back to the curved rule. Use point count, not text_bend: 20 bent rows have a straight 2-point line.
Done in eaa82bf with the fit re-run and log 0052 (564 flat names, 97 fitted). Flat straight names (Waipuna Saddle) stay compact for the fit tool. Open: names whose stock line is shorter than the 7 pt type (Te Ara Pātaka Walkway, 1.4 km line, about 1.7 km of text) cannot spread without a longer baseline. Line 61 above (keep the official charplace) now holds only where the line has room.


Painted-ink inventory (log 0048). Map5View road fill is PMS151 `#FF7F00`, not gold `#D5B43C`. Highway fill is `#E31A1C`. Road casing is `#232323`. Water fill is `#D1E7F5`. Pipeline is not on Map5View.

R-04 owns the contour inks. Index is `#7A5542`. Intermediate is `#B08872`. Casing is the index ink.

Road fill is owned `#EC7000`. Highway stays `#E31A1C`. Contour-number FontMarkers use the index ink. Pair list covers those painted classes. Log 0051. Next is Step C after that paint is on the squares.

Contour stroke alpha (accepted 2026-11-03). Index 0.85. Intermediate 0.5. Index width is 0.35 mm (log 0055). Intermediate casing stays 0.2 mm. Hexes unchanged. Contour numbers stay opaque. Index vs paper still 3:1 grey and red. Intermediate vs paper is not a 3:1 gate. Josh accepted this paint on the BX24 composite (log 0054). A steeper Alpine sheet still answers OQ-09.

Closed foot track (accepted 2026-11-03, log 0056). Same weight and dash as an open foot track. One 1 mm bar at 45° sits in each gap. The web sprite is still a perpendicular bar.
