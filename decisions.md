# Decisions

## B-28: Leave Nimbus Sans LINZ unchanged

**Status:** Superseded by the decision below
**Date:** 2026-11

### Context

Topo50 labels use Nimbus Sans LINZ, the faces in `linz/topographic-qgis` `fonts/` at `c0edcfc`. `fonts/LICENSE` distributes them under AGPL-3.0 with this extra term: the font programs may be included in a PostScript or PDF document, whatever licence that document uses. B-25 changes which face and size the QML requests. B-11, later, may point the QML at another family. Either path can be done by editing the QML or by editing the font files.

### Decision

Leave the Nimbus Sans LINZ files unchanged. Do not copy the OTF files into this repo.

QML may select an upright face of that family and a larger size. A later swap uses an OFL face. This project does not modify Nimbus and does not publish a modified Nimbus.

### Rationale

The exemption covers embedding the stock font programs in a PDF. A QML change that asks for Regular or Narrow, or for a larger size, uses those stock programs. It does not create a derivative font.

A modified Nimbus would be an AGPL-3.0 font. Shipping it would mean shipping the AGPL text and the font source. This slice does not need glyph edits. Nimbus already contains the macron vowels (F-30).

An OFL face (Open Sans, or Atkinson Hyperlegible Next under F-26) is the path when a different family is wanted. That swap replaces the family name in the QML. It does not fork Nimbus.

This is a plain reading of `fonts/LICENSE` and of AGPL-3.0 as it applies to a font program. It is not legal advice.

### Consequences

B-25 and B-24 stay in the QML. Rendered PDFs may embed the stock faces. B-11 stays a QML family change to an OFL face. A future glyph change belongs on an OFL font, and needs a new decision if someone proposes editing Nimbus instead.


## B-28 revised: accessible sheet uses Atkinson Hyperlegible Next

**Status:** Accepted
**Date:** 2026-11
**Supersedes:** B-28: Leave Nimbus Sans LINZ unchanged

### Context

The first B-28 decision left a family swap for later. The accessible map is meant to replace Nimbus Sans LINZ with Atkinson Hyperlegible Next, including the macron vowels that the official Next files do not contain as precomposed glyphs (F-29).

### Decision

The stock BX24 render uses the stock QGIS project and therefore unmodified Nimbus Sans LINZ. Do not modify those font files and do not copy the OTF files into this repo. PDF embedding of that stock render is the exemption in `fonts/LICENSE`.

The accessible render sets label family to Atkinson Hyperlegible Next, built at render time by `tools/patch_atkinson_omacron.py` from the OFL sources. The patch adds U+014C and U+014D and renames the family to `NZAT Legible Test`. Labels are upright. The size floor is unchanged (7 pt, 6 pt for spot heights). B-11 is this swap, done with the label override, not a later trial.

### Rationale

A modified Nimbus would be an AGPL-3.0 font. A swap to the OFL face does not create that derivative. The stock sheet still needs the exemption, because it is the unmodified LINZ project. QGIS can shape Ō/ō without the composites (F-28). The composites are still added so the glyphs are in the font file. The patch is upright statics only, which matches the no-italic rule.

Atkinson Hyperlegible Next has no Narrow master. Stock Narrow labels become the regular width on the accessible sheet. A condensed Atkinson cut would be a new decision.

This is a plain reading of the licences. It is not legal advice.

### Consequences

B-22 stays a Nimbus baseline. The accessible label render installs the patched face in the container and points the QML at `NZAT Legible Test`. The web vector style stays on Open Sans until glyph PBFs exist (R-06). B-10 (upstream Ō/ō report) stays open. The patched binary is not committed. A public family name can replace `NZAT Legible Test` later without changing this decision.


## Judge accessibility on the map layer, not the sheet image

**Status:** Accepted
**Date:** 2026-11

### Context

`map export` with layout `tiff-50` writes one PNG of the whole print page. That page holds the map, the legend, the sheet index, the scale, and the title block. A change read off that image can be a legend swatch or a margin note, not a map symbol.

### Decision

Accessibility edits touch the map layers named by the research. They do not restyle layout text. Layout text stays Nimbus Sans LINZ, including its italic.

The layers and the changes:

- `nztopo50_carto_text`: family, style, and size are data-defined fields. The override replaces those fields with expressions. Upright `NZAT Legible Test`. Size at least 7 pt. `relief_point` labels may stay at 6 pt.
- `contour`: one line symbol. Index is `round(elevation) % 100 = 0`, ink `#8A4F1C`, width 0.28 mm. Other contours are `#C4814B`, width 0.12 mm. `definition` is null on every national row, so indefinite contours are not dashed.
- `track_line map`: categories are cycle, foot, and vehicle. Closed is `status = 'closed'` (153 national rows, almost all foot). Closed foot tracks get a heavier dash and cross-bars.
- `water_point`: the renderer category field was `feature_type`. The column is `type`. Hot and cold are `temperature_indicator` (`hot` 85, `cold` 70). The spring marker is a black × when hot and a `#005C8F` circle when cold.
- `vegetation map`: native and scrub were the same green at two alphas. Native fill is `#E1EAC3`. Scrub fill is `#A3CC90` plus a line hatch. Scattered scrub keeps its dot pattern. Alpha stays below 255 because this layer draws above the contours.

This project's road ink is `#D5B43C`, not the print highway `#EA6300`.

### Rationale

The research already names the layers and the inks. The sheet image cannot separate a map symbol from the legend that repeats it. Layout text is sheet chrome. It is not a map label under R-05 or R-09.

### Consequences

A later pass still has to look at each changed layer on the map face. The pair audit in `tools/pairs-topo50-accessible.json` is the colour check. It is not a substitute for the sheet. Intermediate `#C4814B` does not meet ΔE ≥10 against print highway `#EA6300` for protan and deutan. That miss is recorded as an open question. The starting value from R-04 is still the one rendered.


## One style file drives raster, vector, and the site pictures

**Status:** Accepted
**Date:** 2026-11-02

### Context

The accessible BX24 page is a full `tiff-50` sheet at 150 dpi. A 1 km square on that image is about 118 px. The override values live in `tools/override_topo50_project.py`. The vector style keeps a second palette in `tools/build_style.py`. The site can already show six vision and light conditions from one source image.

### Decision

Accessible colour, type size, font family, and symbol rules live in `tools/style-topo50.json`. The file has no sheet code. The QGIS apply step and the MapLibre build both read it.

Checks use four 1 km squares, redrawn at 600 dpi, map face only. The site shows stock and accessible for each square. `tools/build_site_assets.py` makes the six conditions in `site/src/data/conditions.json`. Those pictures are renders of the style, then the existing simulators.

Work proceeds by pasting `docs/plans/2026-11-02-style-loop-prompt.md`. One paste changes one recommendation, or creates the config if it does not exist. The loop does not render every NZ sheet. It does not start user testing.

### Rationale

A second copy of the research would drift from `docs/recommendations.md`. A token file is what a renderer can apply. The same file is what keeps the vector style on the raster style. The site already knows the six conditions, so a new vision model is not required. Squares are large enough to compare. The national file is what makes a later full-country render possible.

### Consequences

`tools/override_topo50_project.py` and `tools/build_style.py` become readers of the JSON. The vector face may stay Open Sans until macron glyph PBFs exist. Colours and symbol meaning still match. R-04 stays open while `#C4814B` misses ΔE ≥10 against `#EA6300`. R-05 and R-06 stay open while along-line labels are question marks. Tile serving stays later.


## R-04, R-05, and R-06 stay settled in the style loop

**Status:** Accepted
**Date:** 2026-11-02

### Context

The style-loop prompt told the next session to keep three recommendations open. R-04 was open because `#C4814B` misses ΔE ≥10 against print orange `#EA6300`. R-05 and R-06 were open because along-line water names render as black question marks.

### Decision

R-06 stays the patched face `NZAT Legible Test` on the accessible sheet. `font_check` reports all ten macron vowels. The stock sheet keeps Nimbus. The vector style keeps Open Sans until macron glyph PBFs exist. The broken labels do not contain Ō or ō.

R-05 stays upright map labels. The accessible project already has italic count 0 on those styles. Layout italic stays Nimbus.

R-04 keeps index `#8A4F1C` and intermediate `#C4814B`. Judge the contour against the road ink the project paints, `#D5B43C`. That pair is 3.19:1 on white and worst dichromacy ΔE 12.3. The project has no `#EA6300` layer and no pipeline layer. Do not change the intermediate to clear the print-legend orange. `#A8703C` also fails against that orange.

The question marks stay a render defect. On the first render of square 1577000 E, 5178000 N, load the `.ttf` with QFontDatabase. If the marks remain, change `StretchWordSpacingToFit` and render that square again. That defect does not reopen R-05 or R-06.

### Rationale

`#EA6300` is the print-legend orange. Highway layers in this QGIS project use `#D5B43C`. A same-hue brown cannot clear the print orange under protan or deutan simulation, including the older `#A8703C` (protan ΔE 7.2). Offset water names already render as blue letters in the new face, so the font choice and the upright rule are already in the file. The marks are black and limited to one placement mode.

### Consequences

The style loop starts at R-09. The prompt is `docs/plans/2026-11-02-style-loop-prompt.md`. The two questions below are closed by this decision.


## The square draws the sheet map layers

**Status:** Accepted
**Date:** 2026-11-02

### Context

The tiff-50 map item follows the Map5View theme. The square renderer drew every layer in the project order. That set includes `landcover_line` and `building_point`. Map5View hides those layers. `landcover_line` categorises on `feature_type`. The column is `type`. Unmatched rows use the empty symbol. That symbol is a 0.66 mm line in `255,0,159`. `building_point` draws a square outline in `229,100,163`. The sheet draws `building_point map` instead.

### Decision

The square draws the layers that are visible in Map5View. It keeps the project draw order. It does not draw a layer that theme hides.

### Rationale

The official style is the starting point. A hidden layer is not part of the sheet. Drawing it adds symbols the sheet does not paint. The pink lines are that extra set.

### Consequences

A later square render uses Map5View. A change to which layers the sheet draws belongs in that theme, not in a second layer list.


## Along-line labels keep the official placement

**Status:** Accepted
**Date:** 2026-11-02

### Context

The accessible patch set CurvedLabelMode to 0 when `charplace` was `StretchWordSpacingToFit`. That mode draws "Heathcote" upside down on the estuary square. The stock project leaves the field. "Estuary" sits upright. The black question marks were missing landcover SVGs.

### Decision

Do not replace CurvedLabelMode. The data field `charplace` stays. `StretchWordSpacingToFit` stays the along-line placement.

### Rationale

The official placement already draws the words upright. Replacing it made the label wrong. The question marks were a missing symbol file, not this placement mode.

### Consequences

The accessible project and the stock project use the same along-line placement. This does not reopen R-05 or R-06.


## Square draws use the Mac QGIS app

**Status:** Superseded by the decision below
**Date:** 2026-11-02

### Context

The `map` image is linux/amd64. This Mac is arm64. Docker emulates the image. Eight 472 px squares took 46 minutes. The Mac has QGIS 3.36.3-Maidenhead at `/Applications/QGIS.app`. The sheet export still uses the flatpak image `ghcr.io/linz/qgis-flatpak:linz-qgis_v4.2.2_f1431d-297752_build-48`.

### Decision

Square draws use `/Applications/QGIS.app`. The QGIS prefix comes from `QGIS_PREFIX_PATH`. The container prefix stays `/usr` when that variable is empty. The sheet export stays on the `map` image. Do not build an arm64 image of the flatpak.

### Rationale

An arm64 image means a new build of the LINZ QGIS flatpak. The Mac app is already here. The national GeoParquet read stays. The emulation cost does not. The Mac app is not the flatpak build, so a native square can differ a little from the sheet export.

### Consequences

The style loop does not restart. R-09 stays the open recommendation. A square command sets `QGIS_PREFIX_PATH=/Applications/QGIS.app/Contents/MacOS` and runs `tools/render_square.py` with the app Python.


## This Mac QGIS cannot open the square project

**Status:** Superseded by the decision below
**Date:** 2026-11-02
**Supersedes:** Square draws use the Mac QGIS app

### Context

`/Applications/QGIS.app` is QGIS 3.36.3-Maidenhead. The square project was saved by QGIS 4.0.3-Norrköping. A native estuary draw prints that warning. `Map5View` then has no valid layers. The run stops in about 8 seconds and writes no picture.

### Decision

Square draws stay on the `map` image. Do not draw squares with QGIS 3.36.3. `QGIS_PREFIX_PATH` remains the way a newer app would point the same script at itself. An empty value stays `/usr`.

### Rationale

The Mac app is older than the project. It does not reach the national file read. An arm64 flatpak build is still a new QGIS build. The working draw is the current image.

### Consequences

The style loop does not restart. R-09 stays open. A later Mac app that can open a QGIS 4.0.3 project can use `QGIS_PREFIX_PATH` without a new script.

## Square draws use QGIS 4.2.3

**Status:** Accepted
**Date:** 2026-11-02
**Supersedes:** This Mac QGIS cannot open the square project

### Context

The cask app is `/Applications/QGIS-final-4_2_3.app`. It is QGIS 4.2.3-Belém do Pará. The square project was saved by QGIS 4.0.3-Norrköping. QGIS 3.36.3-Maidenhead loaded no Map5View layers.

The app Python does not start unless `PYTHONHOME` is `Contents/Frameworks`. A draw with no `PROJ_DATA` writes a white square. `proj.db` is at `Contents/Resources/qgis/proj`.

### Decision

Square draws use this app. The interpreter is `Contents/MacOS/python3.12`. Set these before the process starts:

- `QGIS_PREFIX_PATH` = `Contents/MacOS`
- `PYTHONHOME` = `Contents/Frameworks`
- `PYTHONPATH` = `Contents/Resources/python3.12/site-packages`
- `DYLD_LIBRARY_PATH` includes `Contents/MacOS` and `Contents/Frameworks`
- `PROJ_DATA` and `PROJ_LIB` = `Contents/Resources/qgis/proj`
- `GDAL_DATA` = `Contents/Resources/qgis/gdal`
- `QT_QPA_PLATFORM` = `offscreen`

Do not set `HOME` to `/tmp` on the Mac. An empty `QGIS_PREFIX_PATH` still means `/usr` inside the map image. The sheet export stays on the map image. Do not build an arm64 image.

### Rationale

Eight 472 px squares took about 130 seconds. The same eight squares on the emulated map image took 46 minutes. The estuary name is upright. The hot-pink pixel count is 0. The pictures match the container squares. The national GeoParquet read stays. The emulation cost does not.

### Consequences

Do not draw squares with QGIS 3.36.3. R-09 stays open. The hierarchy list is still not named. Do not start R-07.

## Place label ranks for R-09

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-09 says adjacent hierarchy levels differ by at least 20%. It does not name the layers. Josh named the list on 2026-11-02.

### Decision

Suburb and Locality are one rank, at 11 px. Town is the next rank, at 14 px. City is the rank after Town, at 17 px. `Place-Label-City-14` and `Place-Label-City-7` are the city rank.

Island labels are a second ladder. `Place-Label-Island-12`, `Place-Label-Island-8`, `Place-Label-Island-6`, and `Place-Label-Island-4` are zoom bands. The number in the id is the max zoom. This decision does not name adjacent island ranks. This step does not change those sizes.

### Rationale

11 px to 12 px is 9%. 13/11 is 18%. 14 is the smallest integer px that is at least 20% above 11. 17 is the smallest integer px that is at least 20% above 14. The island layers do not share one zoom, so they are not one adjacent pair.

### Consequences

Print size floors stay. A later island rank list is a new choice. Do not invent that list in this step.


## R-07 draws the configured label buffer

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-07 says label text is at least 4.5:1 against an opaque halo. The vector build sets an existing halo alpha to 1. It does not add a halo.

In this QGIS project, 36 of 37 map text styles have a buffer colour and a buffer size. bufferDraw is 0 on those styles. One road label draws its buffer. That buffer is already opaque.

Water names use process_blue (0,158,255). That ink is 2.86:1 on white. The names sit on the water fill.

The recommendations note says the build darkens along L* to 4.8:1. The shipped water blue is not the hand-picked #005C8F.

### Decision

Draw the buffer the text style already has. Set bufferDraw to 1. Set buffer opacity to 1. Set the buffer colour alpha to 255. Keep the buffer size. Keep the buffer colour.

Darken a label ink that is below label_contrast.min_ratio (4.8) against that buffer. Use the same L* step as the vector build. Do not switch water names to #005C8F.

Do not draw a buffer on layout text.

### Rationale

A buffer with draw off is not a halo. The size and the colour are already in the project. This step does not invent them.

#005C8F passes the floor. The vector build does not use it. The raster uses the same 4.8 darken.

### Consequences

Map labels gain the halo already described in the text style. Layout text does not. A later step does not turn those buffers off.


## R-10 raster keeps stock scattered dots

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-10 sets scrub to `#A3CC90` and scattered scrub to `#E0EDD8` plus stipple. Print already draws scattered scrub as a PointPatternFill (P6). The stock fill under those dots is not `#E0EDD8`. A raster alpha for a new fill is not in the recommendation.

### Decision

Keep the stock scattered-scrub dots. Do not add a `#E0EDD8` fill under those dots. Do not invent a scattered alpha.

The vector style paints `#E0EDD8` plus `nzat:scattered_stipple`. Raster scrub stays `#A3CC90` plus the existing line hatch. Native forest stays `#E1EAC3` for R-17.

### Rationale

Print already carries scattered scrub by pattern. Adding a fill would need an alpha, and this layer sits above the contours. The web style lost the pattern, so it needs the tint and the stipple.

### Consequences

Raster and vector match on scrub colour and on meaning in shape. They do not match on scattered fill colour. A later step that paints a scattered fill on the raster is a new choice.

## Multiline label folds keep the forward passes

**Status:** Accepted
**Date:** 2026-11-02

### Context

Along-line labels keep `charplace` `StretchWordSpacingToFit`. Setting CurvedLabelMode to 0 draws Heathcote upside down.

A multiline `nztopo50_carto_text` row stores one linestring that folds back on itself. The estuary name is `Estuary of the Heathcote`, then a line break, then `and Avon Rivers / Ihutai`. The line runs east, back west, then east. The passes are 195 m apart. QGIS stretches the whole string along every pass, so the words land on top of each other. 7279 multiline names have one forward pass per text line, with a reverse connector between them. The layer already sets multipart behavior to `SplitLabelTextLinesOverParts`. That setting needs one geometry part per text line.

### Decision

On `nztopo50_carto_text`, a label geometry generator splits a multiline baseline where the turn is sharper than 90 degrees. It keeps the passes that head within 45 degrees of the first pass, when there are at least as many of those as text lines. Each text line is placed on one of those passes. `charplace` stays `StretchWordSpacingToFit`. A label with one text line is not split. The stock project is not changed.

### Rationale

The fold is the baseline used for stacked text. The reverse segment is the connector between two baselines that read the same way. Stretch-to-fit on the whole fold stacks the words. Splitting the geometry uses the multipart setting the project already has. Changing `charplace` would reopen the upside-down Heathcote result.

### Consequences

The accessible project draws stacked names on separate passes. 17 multiline names do not match this fold. Those keep every pass, including a reverse pass. Single-line names on a real bend are unchanged. The stock LINZ project still draws the fold as one line. Revert the source commit that adds the generator to restore the old placement. That commit is marked high risk for that reason.



## R-11 keeps hue and the existing casing

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-11 says closed tracks get a dark casing with cross-bars, and historic sites get a distinct glyph with dark-ink labels. Met when: red-light model ≥3:1 vs paper for all safety-relevant marks.

The raster project already draws a heavier closed foot track and black cross-bars. The vector style already draws `rgba(26, 26, 26, 0.55)` plus `nzat:closed_crossbar`. That casing on white is 3.89:1 under red light. Palette experiment v0 used `rgba(73, 68, 68, 1)` for historic labels. The vector build already darkens a failing label along L* until red-light 3:1 and keeps hue. Raster `warm_red` after the R-07 contrast step is `218,28,0`, which is 1.40:1 under red light.

### Decision

`tracks.closed_foot.casing_colour` is `#1A1A1A`. `tracks.closed_foot.casing_alpha` is `0.55`. `label_contrast.red_light_min` is `3.0`. Those numbers live in `tools/style-topo50.json`.

The vector closed-track casing reads those numbers. The raster apply step does not paint that casing. Raster closed tracks keep the heavier line and the cross-bars.

Raster map labels use the same red-light floor as the vector build. Hue is kept. Historic labels are not switched to `rgba(73, 68, 68)`. Do not add a historic glyph. The raster project already has the historic SVG. The vector style already has `historic_site_pnt`.

### Rationale

The Met when text is the 3:1 red-light floor. The casing already meets it. The vector darken already meets it. `rgba(73, 68, 68)` is not in the dispatch prompt, the recommendation hex, or an earlier lore decision. A new historic glyph would be a new choice.

### Consequences

`warm_red` becomes about `145,0,0`. That ink is 3.02:1 under red light. A later step that paints a grey-brown historic label is a new choice.


## R-17 copies native fill and spring inks

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-17 asks for different hot and cold spring glyphs, a native versus scrub lightness step or texture, scattered scrub as a pattern, upright contour and spot labels, and no meaning that exists only as red-orange.

The raster project already paints those values from `tools/style-topo50.json`. Hot is `cross2` in `#141414`. Cold is `circle` in `#005C8F`. Native fill is `#E1EAC3`. Scrub keeps the R-10 hatch. Vector native fill still uses LINZ zoom greens. Vector spring inks still come from `topographic-v2`. The LINZ icons already differ: `spring_hot_pnt` and `spring_cold_pnt`.

### Decision

`Vegetation-Native` fill is `vegetation.native.colour` (`#E1EAC3`). One colour. Drop the zoom stops.

`Water-Spring-Hot` text is `springs.hot.colour` (`#141414`). `Water-Spring-Cold` icon and text are `springs.cold.colour` (`#005C8F`). Keep `spring_hot_pnt` and `spring_cold_pnt`. Do not add a sprite.

Do not add a native hatch on the vector. Raster scrub already has the hatch. Do not pick new colours.

### Rationale

The JSON already holds the R-17 values. The vector build must copy them. The LINZ icons already carry hot versus cold in shape. A native hatch on the vector would be a new pattern.

### Consequences

Native versus scrub on the vector list is the lightness step `#E1EAC3` versus `#A3CC90`. Grey contrast stays 1.45:1. The raster hatch carries that pair in greyscale. A later native vector pattern is a new choice.

## Curved names keep normal letter spacing

**Status:** Accepted
**Date:** 2026-11-02

### Context

Along-line labels kept `charplace` `StretchWordSpacingToFit`. That mode fits the text to the baseline. The accessible type is larger than the stock type those baselines were drawn for, and the halo adds width. Stretch-to-fit shrinks the gaps. `Gun emplacements`, `Mt Cavendish`, and `SUMMIT ROAD` stay readable on the stock face and overlap on the accessible face.

A stacked name is a separate gap. `Richmond Hill` and `Farm` are 2 mm apart. A 7 pt letter is taller than that gap.

Setting CurvedLabelMode to the integer 0 drew Heathcote upside down before the fold split. The fold split now gives each text line its own forward pass.

### Decision

On `nztopo50_carto_text`, map `StretchWordSpacingToFit` and `StretchCharacterSpacingToFit` to `default`. Letters keep their normal width. A short line may run past its end. The size floor and the halo stay. The fold split stays. Other `charplace` values stay on the field.

Do not move the stacked passes apart in this step.

### Rationale

The baseline length is the stock length. Forcing the larger type onto that length is what overlaps the words. Default curved placement keeps the spacing and can use the existing overrun. The upside-down Heathcote result was the folded line, which the split already removes.

### Consequences

A long name no longer stretches to fill its line. Stacked lines that are 2 mm apart still touch. Moving those passes apart is a later choice. Revert the source commit to put the stretch modes back.

