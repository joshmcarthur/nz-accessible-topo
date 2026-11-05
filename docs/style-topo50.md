# Apply the accessible Topo50 style

`tools/style-topo50.json` sets colour, type size, font family, and symbol rules for the accessible Topo50 style.

The file has no sheet code. The same file can style any NZ Topo50 sheet.

## Apply the file

Run this command:

```
python3 tools/override_topo50_project.py IN.qgs OUT.qgs
```

The script reads `tools/style-topo50.json`. The script writes `OUT.qgs`.

The script changes map layers only. Layout text stays Nimbus Sans LINZ. Layout text keeps its italic.

An along-line label keeps its stretch `charplace` when it is one line and its baseline is longer than the estimated text width. Other stretch labels use default spacing, so the larger type is not squeezed. A one-line name on a curved baseline stays on the curved rule. A flat name (placement 1 on a straight baseline, or a multi-line placement 34 name) can move a short way. Stock stores some straight names as one segment per letter. Such a name is flat too when its baseline is level and shorter than the estimated text width (log 0086). A level baseline longer than the name, such as Pegasus Bay, keeps its stock spread. `tools/fit_carto_labels.py` writes those moves. A name with its own line break keeps it and does not wrap again. A flat name drops leading blanks, spaces after a line break, and runs of spaces. Stock uses those to align a name on its curved baseline (log 0085).

An along-line name whose estimated width is longer than its baseline abbreviates its road suffix. `labels.road_abbreviations` lists the words: ROAD is RD, STREET is ST, AVENUE is AVE, DRIVE is DR, TERRACE is TCE, CRESCENT is CRES, PLACE is PL. Topo50 already uses these forms where a name is tight. A name that fits keeps its full text.

The script draws the buffer that is already on a map text style. It caps that buffer at `label_contrast.halo_max_mm`. It keeps that buffer colour, except on a layer whose name contains `relief_point`. That halo uses `reference_inks.urban_fill`. It sets the buffer alpha to 1. It darkens a label ink that is below `label_contrast.min_ratio` against that buffer.

A carto_text `style` value that contains italic becomes `fonts.raster_natural_style`. That style is Regular: colour carries the natural cue. A style that contains bold becomes Bold (the stock Narrow Bold town names). A narrow or empty style becomes Regular. Named styles stay upright.

The render loads every `.ttf` in the font folder. The folder holds `AtkinsonHyperlegibleNextMacron-Regular.ttf` and `AtkinsonHyperlegibleNextMacron-Bold.ttf`. They come from release `v2.001-1` of [atkinson-hyperlegible-next-macrons](https://github.com/joshmcarthur/atkinson-hyperlegible-next-macrons). That repo adds Ō/ō to the OFL release at `7925f50` (log 0080). Get them and check them with these commands:

```bash
gh release download v2.001-1 -R joshmcarthur/atkinson-hyperlegible-next-macrons -D accessible/fonts -p AtkinsonHyperlegibleNextMacron-Regular.ttf -p AtkinsonHyperlegibleNextMacron-Bold.ttf -p fonts.sha256
(cd accessible/fonts && shasum -a 256 --ignore-missing -c fonts.sha256)
```

Topo50 sets natural-feature names and spot heights in black italic. Natural-feature names take `labels.natural_colour`. Spot heights (a number, with an optional m) stay black, so they do not look like contour numbers (log 0081). On carto_text they also keep `labels.spot_height_floor_pt` (6 pt), one step under the 7 pt name floor (log 0084). That colour is `#7A5542`, the index ink. It is 6.55:1 on paper and 4.29:1 in red light. Water names stay blue. Settlement names stay black.

A square render draws the `Map5View` layers. That is the layer set on the `tiff-50` map. The render does not draw a layer that theme hides.

The square script reads `QGIS_PREFIX_PATH`. An empty value keeps the container prefix `/usr`.

A square draw on this Mac uses `/Applications/QGIS-final-4_2_3.app`. That app is QGIS 4.2.3. The interpreter is `Contents/MacOS/python3.12`.

Set these before the process starts. `PYTHONHOME` is `Contents/Frameworks`. `PYTHONPATH` is `Contents/Resources/python3.12/site-packages`. `DYLD_LIBRARY_PATH` includes `Contents/MacOS` and `Contents/Frameworks`. `PROJ_DATA` and `PROJ_LIB` are `Contents/Resources/qgis/proj`. `GDAL_DATA` is `Contents/Resources/qgis/gdal`. `QT_QPA_PLATFORM` is `offscreen`.

A draw with no `PROJ_DATA` writes a white square. Do not set `HOME` to `/tmp` on the Mac. The sheet export stays on the `map` image. Do not draw squares with QGIS 3.36.3.

Map labels in `OUT.qgs` use the family `Atkinson Hyperlegible Next Macron`.

The stock sheet does not use this file. The stock sheet keeps Nimbus Sans LINZ.

## Vector style

`tools/build_style.py` reads the label size floors from this file.

`labels.web_floor_px` is 10. `labels.place_name_floor_px` is 11.

Suburb and Locality are one rank, at 11 px. Town is the next rank, at 14 px. City is the next rank, at 17 px. Island label layers are zoom bands. This file does not set a size spread for them.

The vector build reads `label_contrast` from this file.

`label_contrast.min_ratio` is 4.8. `label_contrast.halo_alpha` is 1. `label_contrast.halo_max_mm` is 0.4. `label_contrast.red_light_min` is 3.0.

The vector build reads `labels.letter_spacing_em` from this file.

`labels.letter_spacing_em` is 0.05. That tracking is provisional (R-08).

The QGIS apply step does not add that tracking. Along-line labels keep normal letter spacing.

The QGIS apply step uses `halo_max_mm`. The vector build does not change `text-halo-width`.

The QGIS apply step darkens a label ink that is below that red-light floor. It keeps the hue.

The vector build reads `vegetation.native`, `vegetation.scrub`, and `vegetation.scattered` from this file.

`vegetation.native.colour` is `#E1EAC3`. `vegetation.native.marker.colour` is `#3F6B32`. `vegetation.scrub.colour` is `#A3CC90`. `vegetation.scrub.alpha` is 26. `vegetation.scattered.colour` is `#E0EDD8`.

The QGIS apply step paints the scrub fill and a plant-mark grid. The marks carry the class. The marker name is `vegetation.scrub_dots.marker`. That name is `third_arc`, the same mark as scattered scrub. Size is `vegetation.scrub_dots.size_mm`. That size is 1.4 mm. Distance is `vegetation.scrub_dots.distance_mm`. That distance is 3 mm. Colour is `vegetation.scrub_dots.colour`. That colour is `#6A9A50`, a mid green. The stroke is `vegetation.scrub_dots.stroke_mm`, 0.18 mm. A stock hairline arc in `#B2DF8A` did not show on the pale fill (log 0071). A mark draws whole when its centre is inside the polygon. Scattered scrub stays on its stock `third_arc` pattern at 5 mm with no fill. A second apply removes a leftover line hatch and writes the marker, size, colour, and spacing onto the pattern that is already in the project. It paints a native tree marker when that marker layer is already in the project. It does not add a fill under the scattered dots.

The QGIS apply step moves `vegetation map` so it sits immediately under `contour`. Custom-order stays off. Vegetation alpha stays 180 native and 26 scrub. `vegetation_line map` stays above contours. The vector style already paints contours after vegetation fills.

The vector build paints those three fills. It adds a stipple on scattered scrub.

The vector build reads `springs.hot.colour` and `springs.cold.colour` from this file.

`springs.hot.colour` is `#141414`. `springs.cold.colour` is `#005C8F`.

The vector style keeps `spring_hot_pnt` and `spring_cold_pnt`. The QGIS apply step paints hot as `cross2` and cold as `circle`.

The vector build reads `tracks.closed_foot.casing_colour` and `tracks.closed_foot.casing_alpha` from this file.

`tracks.closed_foot.casing_colour` is `#1A1A1A`. `tracks.closed_foot.casing_alpha` is 0.55.

The QGIS apply step does not paint that casing. A closed foot track uses the same line weight and the same dash as an open foot track. The marker name is `tracks.closed_foot.marker`. That name is `cross2`. Size is `tracks.closed_foot.crossbar_size_mm`. That size is 0.5 mm. Interval is `tracks.closed_foot.marker_interval_mm`. That interval is 3 mm, every second dash gap. The first mark sits in a gap. The angle is `tracks.closed_foot.crossbar_angle_deg`. That angle is 0. A second apply writes the marker, the size, the interval, and the gap position onto the marker that is already in the project.

`tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false.

The QGIS apply step does not paint track access. The vector build does not paint track access. Access data is not in the Topo50 layers.

The vector build reads `hillshade.azimuth_deg` and `hillshade.fill_azimuths_deg` from this file.

`hillshade.azimuth_deg` is 337.5. `hillshade.painted` is true. `hillshade.raster_file` is `dem.tif`.

Hillshade is an overlay. It is not baked into the map inks.

The QGIS apply step writes those lights onto the project elevation shader. The shader turns on only when `painted` is true and `dem.tif` sits beside the `.qgs`. A missing file is not an error. Drop a GeoTIFF at that name to rasterise with shade. Set `painted` to false to disable the overlay.

The vector hillshade layer stays visible while `painted` is true. Set `painted` to false to hide that layer.

The vector build reads `contours.index.width_mm`, `contours.intermediate.casing_colour`, `contours.intermediate.casing_width_mm`, and the contour `alpha` values from this file.

`contours.index.colour` is `#7A5542`. `contours.index.alpha` is 0.85. `contours.intermediate.colour` is `#B08872`. `contours.intermediate.alpha` is 0.5. `contours.index.width_mm` is 0.35. `contours.intermediate.casing_colour` is `#7A5542`. `contours.intermediate.casing_width_mm` is 0.2.

The QGIS apply step paints that casing under an intermediate contour. It paints those alphas with `color_rgba`. The index contour stays one heavier line. Contour-number FontMarkers stay opaque.

The pair audit reads this file. Pair colours that live here are dotted paths in `tools/pairs-accessible-v0.json` and `tools/pairs-topo50-accessible.json`. Paper and LINZ inks that this file does not own stay as hex.

The vector style is this file on Shortbread tiles. `tools/build_style.py` writes owned paint from this file onto the catalog in `upstream/linz-topographic-v2.json`. Layers this file does not name keep LINZ paint. The builder holds no second colour palette.

The vector style keeps Open Sans until macron glyph PBFs exist.

The vector face is not the same face as the raster face until those glyphs exist.

Colours and symbol meaning in this file are the values that vector build must copy.

## Change a value

Edit `tools/style-topo50.json`. Then run the apply command again.

For a label size or for `label_contrast`, also run:

```
python3 tools/build_style.py
```

Do not put a sheet code in the file.

`reference_inks.project_road` is `#EC7000`. The QGIS apply step paints two-lane and sealed PMS151 fills in that ink. Highway fills stay `#E31A1C`. Gold `#D5B43C` is the bivouac marker, not the road fill.

Contour-number FontMarkers on `nztopo50_carto_symbol` use `contours.index.colour`. They are `Atkinson Hyperlegible Next Macron` Regular, not italic (the FontMarker options are `font` and `font_style`). Size is at least 6 pt. A paper-coloured copy of each digit draws first with a `contours.number_halo.width_mm` stroke (0.3 mm), so the digit has a halo. The layer blends normally, not DestinationOver, so the digit draws over its halo.

`reference_inks.project_highway` is `#E31A1C`. Map5View paints highway fills in that ink. The apply step does not paint that ink.

`reference_inks.project_road_casing` is `#232323`. Road and highway background layers paint that casing. The apply step does not paint that ink.

`reference_inks.water_fill` is `#D1E7F5`. Map5View paints water fills in that ink. The apply step does not paint that ink.

`reference_inks.print_legend_highway` is `#EA6300`. Map5View does not paint that ink.

`water.stream_width_mm` is 0.25. `water.drain_width_mm` is 0.15. The apply step sets a data-defined width on `water_line map`: drains take the drain width, rivers and canals take the stream width. Coastline, water outlines, shelterbelt, and grid keep stock widths. Only their ink changes.

`reference_inks.stream` is `#004C99`. That hex keeps the process-blue hue. It is dark enough that a stream and an index contour differ in greyscale (1.83:1, log 0083), and it passes 3:1 on paper, scrub, native, water, and urban. Map5View paints streams, drains, coastline, ice contours, landcover water outlines, and water outlines as `#009EFF`. The apply step rewrites that RGB on every map layer.

`reference_inks.shelterbelt` is `#1D9D00`. Map5View paints shelterbelts and green vegetation dots as `#94FF3B`. The apply step rewrites that RGB.

`reference_inks.grid` is `#269FD2`. Map5View paints grid lines as `#29A0D3`. The apply step rewrites that RGB.

`reference_inks.urban_fill` is `#BCBAB6`. Map5View paints residential fill in that ink. The apply step does not paint that ink.

`reference_inks.island_outline` is `#0083BB`. Map5View paints island outlines in that ink. The apply step does not paint that ink.

`reference_inks.vegetation_outline` is `#A7C05E`. Map5View paints vegetation outlines in that ink. The apply step does not paint that ink.

`vegetation.exotic.colour` is `#A4D65E`. `vegetation.exotic.alpha` is `0.2`. Map5View paints exotic forest in that fill. The apply step does not paint that fill.

`fonts.vector_family` is Open Sans. The QGIS apply step does not use that family.

`fonts.stock_family` is Nimbus Sans LINZ. The QGIS apply step does not use that family on map labels.
