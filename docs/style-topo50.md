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

The script does not change `charplace`. Along-line labels keep `StretchWordSpacingToFit`.

The script draws the buffer that is already on a map text style. It caps that buffer at `label_contrast.halo_max_mm`. It keeps that buffer colour. It sets the buffer alpha to 1. It darkens a label ink that is below `label_contrast.min_ratio` against that buffer.

A square render draws the `Map5View` layers. That is the layer set on the `tiff-50` map. The render does not draw a layer that theme hides.

The square script reads `QGIS_PREFIX_PATH`. An empty value keeps the container prefix `/usr`.

A square draw on this Mac uses `/Applications/QGIS-final-4_2_3.app`. That app is QGIS 4.2.3. The interpreter is `Contents/MacOS/python3.12`.

Set these before the process starts. `PYTHONHOME` is `Contents/Frameworks`. `PYTHONPATH` is `Contents/Resources/python3.12/site-packages`. `DYLD_LIBRARY_PATH` includes `Contents/MacOS` and `Contents/Frameworks`. `PROJ_DATA` and `PROJ_LIB` are `Contents/Resources/qgis/proj`. `GDAL_DATA` is `Contents/Resources/qgis/gdal`. `QT_QPA_PLATFORM` is `offscreen`.

A draw with no `PROJ_DATA` writes a white square. Do not set `HOME` to `/tmp` on the Mac. The sheet export stays on the `map` image. Do not draw squares with QGIS 3.36.3.

Map labels in `OUT.qgs` use the family `NZAT Legible Test`.

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

`vegetation.native.colour` is `#E1EAC3`. `vegetation.scrub.colour` is `#A3CC90`. `vegetation.scattered.colour` is `#E0EDD8`.

The QGIS apply step paints the scrub fill and a line hatch. It keeps the stock scattered-scrub dots. It does not add a fill under those dots.

The QGIS apply step moves `vegetation map` so it sits immediately under `contour`. Custom-order stays off. Vegetation alpha stays 180 native and 200 scrub. `vegetation_line map` stays above contours. The vector style already paints contours after vegetation fills.

The vector build paints those three fills. It adds a stipple on scattered scrub.

The vector build reads `springs.hot.colour` and `springs.cold.colour` from this file.

`springs.hot.colour` is `#141414`. `springs.cold.colour` is `#005C8F`.

The vector style keeps `spring_hot_pnt` and `spring_cold_pnt`. The QGIS apply step paints hot as `cross2` and cold as `circle`.

The vector build reads `tracks.closed_foot.casing_colour` and `tracks.closed_foot.casing_alpha` from this file.

`tracks.closed_foot.casing_colour` is `#1A1A1A`. `tracks.closed_foot.casing_alpha` is 0.55.

The QGIS apply step does not paint that casing. Closed foot tracks keep the heavier line and the cross-bars.

`tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false.

The QGIS apply step does not paint track access. The vector build does not paint track access. Access data is not in the Topo50 layers.

The vector build reads `hillshade.azimuth_deg` and `hillshade.fill_azimuths_deg` from this file.

`hillshade.azimuth_deg` is 337.5. `hillshade.painted` is true. `hillshade.raster_file` is `dem.tif`.

Hillshade is an overlay. It is not baked into the map inks.

The QGIS apply step writes those lights onto the project elevation shader. The shader turns on only when `painted` is true and `dem.tif` sits beside the `.qgs`. A missing file is not an error. Drop a GeoTIFF at that name to rasterise with shade. Set `painted` to false to disable the overlay.

The vector hillshade layer stays visible while `painted` is true. Set `painted` to false to hide that layer.

The vector build reads `contours.index.width_mm`, `contours.intermediate.casing_colour`, and `contours.intermediate.casing_width_mm` from this file.

`contours.index.width_mm` is 0.45. `contours.intermediate.casing_colour` is `#8A4F1C`. `contours.intermediate.casing_width_mm` is 0.2.

The QGIS apply step paints that casing under an intermediate contour. The index contour stays one heavier line.

The vector build still keeps other colours in `tools/build_style.py`.

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

`reference_inks.project_road` is `#D5B43C`. The apply step does not paint that ink. Judge a contour against that ink.

`reference_inks.print_legend_highway` is `#EA6300`. The apply step does not paint that ink.

`fonts.vector_family` is Open Sans. The QGIS apply step does not use that family.

`fonts.stock_family` is Nimbus Sans LINZ. The QGIS apply step does not use that family on map labels.
