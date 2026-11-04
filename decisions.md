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

## R-01 intermediate contours use an index-ink casing

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-01 requires every must-distinguish pair to meet ≥3:1 greyscale or a pattern/shape, and the same under red light. Intermediate fill `#C4814B` versus paper is 3.19:1 grey and 1.74:1 red. Weight does not change that measured pair. Darkening `#C4814B` is forbidden (R-04).

Index ink `#8A4F1C` versus paper is 6.53:1 grey and 3.45:1 red. Closed tracks already use a 0.2 mm outline.

### Decision

Keep index `#8A4F1C` at 0.28 mm, one solid line.

Keep intermediate fill `#C4814B` at 0.12 mm.

Add `contours.intermediate.casing_colour` `#8A4F1C` and `casing_width_mm` 0.2 to `tools/style-topo50.json`.

The QGIS apply step inserts a second SimpleLine under the fill. The casing is enabled only when the line is not an index contour.

The vector build inserts `NZAT-Contours-All-Casing` behind `Contours-All`. Casing colour is the JSON value. Casing width is the intermediate width stops scaled by 0.2/0.12.

Do not add a new brown. Do not darken the fill. The Port Hills square must still read as contours before R-01 is met.

### Rationale

The surviving ink under red light is the index brown already on the sheet. A casing is shape, so R-04 can keep the recessive fill. A heavier fill of `#C4814B` would not pass 3:1 red. A darker fill would reopen R-04.

### Consequences

The pair audit judges the intermediate line against paper as the casing ink. Index outer width stays 0.28 mm. Intermediate outer width stays 0.2 mm. If the Port Hills square no longer reads as contours, revert the casing.

## R-01 index contour is 0.45 mm

**Status:** Accepted
**Date:** 2026-11-02

### Context

The intermediate casing uses index ink `#8A4F1C` at 0.2 mm. Index was 0.28 mm in the same ink. The outer-width step was 1.4×. Port Hills no longer showed a clear index versus intermediate step.

Darkening `#C4814B` is forbidden. Removing the casing would drop red-light contrast versus paper to 1.74:1. Dashed intermediates would collide with indefinite contours. Ticks and a double index line would change what a contour looks like.

Closed foot tracks already use 0.45 mm.

### Decision

`contours.index.width_mm` is 0.45. Intermediate fill stays 0.12 mm. Intermediate casing stays 0.2 mm in `#8A4F1C`.

Scale the vector index width stops by 0.45/0.28. Do not add ticks. Do not draw a double index line.

### Rationale

0.45 mm versus 0.2 mm is a 2.25× outer-width step. That is the same order as the pre-casing 0.28 mm versus 0.12 mm step. The number is already in the style file on closed foot tracks. The tan fill still marks an intermediate in normal light. The casing still carries the line under red light.

### Consequences

Index lines read heavier on dense slopes. If Port Hills still cannot separate index from intermediate, the next choice is a shape channel on index, not a new brown.

## R-01 is met on the Port Hills square

**Status:** Accepted
**Date:** 2026-11-02

### Context

Intermediate contours use a 0.2 mm `#8A4F1C` casing under a `#C4814B` fill. Index is 0.45 mm in `#8A4F1C`. Josh accepted the index versus intermediate step on the Port Hills square and the BX24 compare.

### Decision

R-01 is met for this loop. Casing versus paper is 6.53:1 grey and 3.45:1 red. The tan fill stays `#C4814B`. Do not darken it. Do not add ticks or a double index line.

### Rationale

The Met when text allows ≥3:1 grey or a pattern/shape, and the same under red light. The casing carries the line under red light. Weight carries index versus intermediate.

### Consequences

R-13 may run later. Do not reopen the contour inks in this loop.

## R-08 one attempt stays provisional

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-08 asks for +0.04–0.08 em tracking on point/area labels. Met when is an A/B test with dyslexic readers. This loop skips user testing. Vector already paints 0.05 em from `P`. Raster along-line labels keep normal spacing so type is not squeezed onto the stock line.

### Decision

`labels.letter_spacing_em` is 0.05 in `tools/style-topo50.json`. The vector build reads that number. Do not add tracking on QGIS along-line labels. Do not run an A/B test. Leave R-08 provisional.

### Rationale

The dispatch allows one attempt and says to leave it provisional if the evidence is still weak. The Met when text is user testing, which this loop skips. Tracking on curved names would undo the normal-spacing decision.

### Consequences

Raster map labels do not gain 0.05 em tracking. A later A/B test is a new choice.

## R-12 reserves an unpainted casing/colour channel

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-12 asks to leave a casing/colour channel unused for track access status. Access (public/private, DOC, walkway) is not in the Topo50 layers (F-25). R-11 already encodes closed tracks with cross-bars. Closed is not access.

### Decision

`tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false.

Do not pick an access ink. Do not overlay Walking Access or DOC data. Do not paint a casing for access on the QGIS apply step or the vector build.

Closed-track casing stays for R-11 on the vector style. That casing is closed status, not access.

### Rationale

The recommendation is to reserve a channel, not to show access. Showing access needs data we do not have. A new hex would be a guess. R-11 did not cover this: it encodes closed tracks, not public versus private access.

### Consequences

A later step that paints access is a new choice. It needs an access attribute or an overlay source.

## Flat carto text uses cartographic placement

**Status:** Accepted
**Date:** 2026-11-02

### Context

The larger accessible type and the halo make `nztopo50_carto_text` names collide in busy areas. Each row has one hand-drawn baseline for 6–7 pt Nimbus. Curved placement on that one baseline gives QGIS no other position, so `AllowOverlapIfRequired` draws names on top of each other. No row links to the feature it labels (`example_point_id` is null).

### Decision

On the accessible project, `nztopo50_carto_text` labeling is rule-based with two rules. Rows with `text_placement = 1`, `text_orientation = 0`, and no line break use placement 6 (cartographic). The anchor is a point geometry generator at the stock label centre. The order comes from `labels.carto_point` in `tools/style-topo50.json`: `O, T, B, TSR, TSL, BSR, BSL, TR, TL, BR, BL`, 0.3 mm. `PreferPositionOrdering`. `AllowOverlapIfRequired` stays. All other rows keep the curved settings and the fold split. The point rule drops the line-only data-defined fields (`LabelDistance` from `offset`, line placement flags, line anchor, curved mode).

### Rationale

QGIS already has an ordered-position solver. `O` first keeps the LINZ position when it is free. `PreventOverlap` would remove names from a topo map. A line flag change (above and below) only flips a label across its baseline. An offline solver would duplicate PAL.

### Consequences

`@map_scale` is null in a label geometry generator. The anchor lift uses the fixed 1:50,000 scale. A point label whose anchor is outside the drawn extent is not drawn, so a 1 km square can drop a name that crosses its edge. A name that moves sideways can land far from its feature: `Ōmawete / Coopers Knob` moves about 500 m east on the cold spring square. The slightly positions do not limit the move: QGIS aligns `TSR` to the anchor, so with the anchor at the label centre `TSR` moves a label by half its width, like `TR`. A nearest-feature anchor or a real move limit is a later choice. The `map` container runs QGIS 4.2.2, which has `OverPoint`.

## Flat carto text slides on a bounded line

**Status:** Accepted. Supersedes "Flat carto text uses cartographic placement".
**Date:** 2026-11-02

### Context

Cartographic point placement around the stock label centre moved `Ōmawete / Coopers Knob` about 500 m east. QGIS aligns every point position, including the "slightly" ones, to the anchor. A centred anchor therefore moves a label by half its width on any sideways step. A point label with its anchor outside the drawn extent is not drawn.

### Decision

The flat one-line rule (`text_placement = 1`, `text_orientation = 0`, no line break) uses parallel line placement (mode 2) with above and below map-oriented flags (14). A geometry generator draws a horizontal line at the stock baseline, centred on the stock label. Its half-length is characters × max(size floor, size) × `advance_em` × points-to-metres / 2 + `allowance_mm`. `overrun_mm` absorbs estimate error. Values in `labels.carto_point`: allowance 1 mm, advance 0.6 em, overrun 0.5 mm. The stock `LabelDistance` from `offset` stays. Curved-only fields are dropped. `AllowOverlapIfRequired` stays.

### Rationale

QGIS prefers the middle of a line, so the stock position wins when free. The allowance caps the sideways move at about 1.5 mm. Below-line gives one vertical step. Line labels draw where the line crosses the extent. Atkinson measures 0.45–0.63 em per character on sample names.

### Consequences

A long all-caps name can exceed its estimated line. Tune `advance_em` or `allowance_mm` if names go missing on the full sheet. A nearest-feature anchor is not needed for the cold spring case.

## Flat dual names draw on two lines; the strict anchor stays

**Status:** Accepted
**Date:** 2026-11-02

### Context

On the full BX24 face, long flat dual names such as `Ōmawete / Coopers Knob` still collided on the bounded line. The flat rule copies the stock strict line anchor at 50 %. That anchor holds the label at the middle of its line, so the allowance gives no sideways move.

### Decision

The flat rule's label text is `replace("text_string", ' / ', ' /\n')`, centred, with `multipartBehavior` `LabelLargestPartOnly`. The line length uses the longest text line. The strict anchor stays. Squares and crops are not used to judge placement; the full face is.

### Rationale

Four of six BX24 dual names clear. `Ōmawete /` and `Te Upoko-o-Kurī /` still overlap; with `PreventOverlap` they are not drawn, so no free position exists. A hint anchor lets labels slide but moves `Godley Head` onto `Gun emplacements` and `Ōrongomai` onto `505`. A 2 mm allowance, the on-line position, a lower spot-height priority, rule priority 5, and label engine version 2 gave no gain. The copied `SplitLabelTextLinesOverParts` drew only the first text line on a one-part line. A crop moves labels to fit its extent.

### Consequences

Two overlaps stay on BX24. A later fix needs more positions for fixed curved labels or a different split rule, not a longer line.

## Long flat names wrap; fitted names come from carto_fit.json

**Status:** Accepted
**Date:** 2026-11-03

### Context

QGIS tests label boxes as yes or no. A one-line box is font ascent plus descent, 1.3 em for NZAT Legible Test. On the spring, `Ōmawete / Coopers Knob` fits on one line in ink, but its box collides with `Rhodes Spring` and `A579`, so QGIS puts it below on `A579`. Tight metrics, size priority, obstacles off, and `IgnoreWhitespaceCollisions` did not change that. QGIS cannot pick between two texts for one label.

### Decision

Flat single names longer than `labels.carto_point.wrap_chars` (16) wrap at that length. Dual names keep the slash break. A leading `Te ` gets a no-break space. The flat rule line height is `line_height` (0.85).

The apply step reads an optional `carto_fit.json` beside the `.qgs`: `{row id: {x, y, lines}}`. A listed row gets data-defined `PositionX`/`PositionY` with `Hali 'Center'` and `Vali 'Bottom'`, and `lines: 1` drops the slash break and the wrap. Unlisted rows return NULL and keep normal placement. The fit file is per sheet and is not in the style file.

### Rationale

QGIS's own wrap breaks dual names and `Te` names badly. A hand fit at the spring (x 1570014, y 5165748, one line) draws clear between both neighbours. Data-defined position overrides placement only where a value exists.

### Consequences

The wrap applies to every long single name, even where there was room. At 0.85, `Ōmawete /` sits fully under `Rhodes Spring` until a fit moves it. `tools/fit_carto_labels.py` will write the fit file from ink overlap.

## Vegetation map draws below contour

**Status:** Accepted
**Date:** 2026-11-02

### Context

Stock Topo50 draws `vegetation map` above `contour`. The stock fill is pale, so the brown lines still read. The accessible native and scrub fills are darker and scrub is hatched, so those fills hide the contours on the cold-spring square. `landcover map` is already under `contour`. `vegetation_line map` is line vegetation. The vector style already paints contours after vegetation fills.

### Decision

The QGIS apply step moves `vegetation map` in the layer tree so it sits immediately under `contour`. Custom-order stays off. Tree order is draw order. `vegetation_line map` stays above contours. Vegetation alpha stays 180 native and 200 scrub. Vector style does not change.

The constraint is `draw_order` in `tools/style-topo50.json`: `vegetation map` below `contour`. The apply step reads that pair. It is not a general order engine.

### Rationale

R-04 needs contours that stay visible. R-10 and R-17 need a larger forest versus scrub step. Lowering vegetation alpha would weaken that step. Reordering keeps both. A one-off .qgs edit would be undone by the next apply. Turning on custom-order would rewrite the full draw list.

### Consequences

Accessible sheets diverge from LINZ layer order on this one pair. Stock order stays. Opaque vegetation fills are a later choice. The old note that alpha stays below 255 because vegetation draws above contours is no longer the reason for that alpha.


## R-03 hillshade is an optional overlay

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-03 asks for NNW 337.5° shading with a soft multidirectional component. Printed Topo50 uses NW. This QGIS project has elevation shading off and a flat terrain. Served raster tiles may already bake NW relief (B-26). Baking a second light into the accessible pixels would lock a grey wash onto labels and contours. Josh asked that raster shading be as simple as dropping a DEM beside the project, and that shipped tiles keep shade optional.

### Decision

Hillshade is an overlay. Do not bake it into Topo50 pixels.

`tools/style-topo50.json` holds `hillshade`: azimuth 337.5°, altitude 45°, QGIS multidirectional true, `raster_file` `dem.tif`, `painted` true.

The QGIS apply step writes those numbers onto the existing `elevation-shading-renderer`. It turns the shader on only when `painted` is true and `dem.tif` sits beside the `.qgs`. A missing file is not an error. Dropping a GeoTIFF at that name is enough to rasterise with shade. Set `painted` to false to disable even if the file is present.

The square renderer copies that shader. If the file is present at draw time, it loads the DEM even if apply ran without it.

The vector build reads the same azimuth and fill lights. It does not keep `hillshade_direction` in `P`. When `painted` is false, the MapLibre hillshade layer is not visible.

Do not add a DEM to this repo. Do not fetch LINZ elevation in this step. R-03 stays open until shading is evaluated on an Alpine sheet and a lowland sheet.

### Rationale

Contours already carry relief. A baked grey wash cannot be turned off on paper and can hide the R-01 contour work. A MapLibre hillshade layer is already a separate overlay. The QGIS project already has an elevation-shading switch. A fixed relative GeoTIFF path matches the parquet drop-in pattern.

### Consequences

The four squares stay unshaded until a DEM is dropped. QGIS multidirectional is the project boolean, not the three MapLibre fill azimuths. Those fill azimuths stay for the vector variant. A later print variant that wants shade uses the same flag.


## R-14 pair colours resolve from the style file

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-14 asks the pair audit to run on every style change and fail on new ❌ rows. Pair files still copied hex that already lived in `tools/style-topo50.json`. A colour change in the style file would not change the audit.

### Decision

Pair files keep names, floors, and why. A colour that lives in `tools/style-topo50.json` is a dotted path. `palette_audit.py` resolves that path before it measures. Closed-track casing may also name `tracks.closed_foot.casing_alpha`.

Literal hex stays for paper and for LINZ inks the style file does not own. Historic label ink stays a literal: it is a darkened result, not a configured colour.

`check.py` C6 still reads `tools/pairs-accessible-v0.json`. It resolves those pairs first. Do not add `pairs-topo50-accessible.json` to C6. Do not fail C6 against `#EA6300`. This project does not paint that ink.

Do not put the pair list in the style file.

### Rationale

The style file is the paint source. The pair file is the must-distinguish list. Path references keep one paint source. C6 already gates the vector pairs that the built style paints.

### Consequences

A colour change in the style file changes the audit. Paper and LINZ highway, pipeline, and water fills stay as hex until those inks live in the style file.


## R-13 stays open until the variant inks are named

**Status:** Accepted
**Date:** 2026-11-02

### Context

R-13 asks for three products from one source: full colour, greyscale-safe print, and a high-contrast web variant. The dispatch, the recommendations, and lore do not name those inks. R-13 has no Met when text.

### Decision

Do not invent palettes. Do not add a greyscale style or a high-contrast style in this loop. R-13 stays open.

The main style remains the full-colour product. The site grey condition stays a simulation of that product. R-01 already requires greyscale or shape on the main style.

A later step that paints the other two products must name the inks first.

### Rationale

The loop must not guess values that are missing from the dispatch, the recommendations, and lore.

### Consequences

B-14 stays later. Next in the loop is R-15.


## R-15 vector style is the raster style on Shortbread

**Status:** Accepted
**Date:** 2026-11-02
**Supersedes:** the R-15 line that the vector style is a fork of `topographic-v2`

### Context

Josh rejected a vector style that is a fork of LINZ `topographic-v2`. The vector style must be a vector form of the raster style in `tools/style-topo50.json`. That file does not name a tile source. Josh chose LINZ Basemaps Shortbread tiles. For layers the style file does not name, keep LINZ paint, as the QGIS apply step keeps stock paint.

### Decision

`styles/accessible-v0.json` is the vector form of `tools/style-topo50.json`. It is not a LINZ `topographic-v2` fork.

`upstream/linz-topographic-v2.json` is the layer catalog: sources, glyphs, layer ids, filters, source-layers, minzoom, and paint for unowned layers.

Owned paint (contours, vegetation, springs, closed tracks, label size, upright faces, halo, tracking, contrast darken, hillshade) comes from the style file. `P` in `tools/build_style.py` holds no colour hex. Vector zoom width stops stay in the builder. They are not a palette.

The vector face stays Open Sans until macron glyph PBFs exist.

### Rationale

The raster apply step starts from stock Topo50 and writes only the rules the style file owns. The vector build does the same on Shortbread. A new tile pipeline is out of this loop.

### Consequences

CI still rebuilds from the catalog and the style file. Layers the JSON does not name can still change when upstream LINZ paint changes. Next is Step C.



## Painted road ink is PMS151, not gold

**Status:** Accepted
**Date:** 2026-11-03
**Supersedes:** the road-ink fact in "R-04, R-05, and R-06 stay settled in the style loop"

### Context

The style loop judged contours against `#D5B43C` and treated that as the project road, including highways. Map5View does not paint that gold as a road fill. Pixel counts on the accessible squares and SimpleLine `line_color` on the map layers both show PMS151.

### Decision

`reference_inks.project_road` is `#FF7F00`. `reference_inks.project_highway` is `#E31A1C`. `reference_inks.project_road_casing` is `#232323`. `reference_inks.water_fill` is `#D1E7F5`. Print highway `#EA6300` stays a reference the style does not paint.

Judge R-04 against those painted inks. Keep contour fills `#8A4F1C` and `#C4814B`. Do not change an intermediate to clear orange.

Gold `#D5B43C` is the bivouac marker colour.

### Rationale

R-04 Met when is ΔE ≥10 versus the highway the map paints. Scoring against a legend colour that is not on the line hid three failing pairs (log 0048).

### Consequences

R-04 is open. Road and highway fills stay unowned until a later step paints them. Dark casing already carries R-01 and R-17 P7 for those classes under red light.


## Olive-brown contours close painted R-04

**Status:** Accepted
**Date:** 2026-11
**Supersedes:** the contour-ink instruction in "Painted road ink is PMS151, not gold"

### Context

R-04 Met when is ΔE ≥10 versus the highway and road the map paints. Those fills are PMS151 `#FF7F00` and highway `#E31A1C`. Index `#8A4F1C` versus the highway is protan ΔE 0.9. Intermediate `#C4814B` versus the road fails protan and tritan. A same-hue lightness sweep of those oranges cannot meet the bar without a pale fill or a non-orange. Pale orange is not a landmark.

Identifiability beats the old Topo50 orange-brown contour grammar. Roads must stay strong landmarks.

### Decision

Keep road fill `#FF7F00` and highway fill `#E31A1C`. Do not lighten them.

Index contour is `#7A5542`. Intermediate fill is `#B08872`. Intermediate casing stays the index ink. Lightness of both contour fills stays the same as `#8A4F1C` / `#C4814B`.

Do not return to `#8A4F1C` / `#C4814B`. Do not invent R-13 palettes in this step.

### Rationale

Protanopia collapses a*. An olive shift of a* alone cannot separate index from highway. Reducing b* by about 22 moves the contour off the yellow-red axis protans still see. Reducing a* by 8 takes remaining redness out of the brown. The pair is olive-taupe, not orange. L* is unchanged, so the fill mass on dense slopes does not darken (OQ-09).

The smallest same-L* pair that is clearly less red and still meets ΔE ≥10 against both painted fills is this one. A mauve shift that keeps a* fails the "less red" choice. A paler road fails the landmark choice.

### Consequences

The style-loop settled contour hexes are superseded. The next loop paste must keep `#7A5542` / `#B08872`. Road and highway fills stay unowned. Pipeline is still not on Map5View. A steep sheet still answers OQ-09.


## Darker orange road fill and index-ink contour numbers

**Status:** Accepted
**Date:** 2026-11
**Supersedes:** the unowned-road instruction in "Olive-brown contours close painted R-04"

### Context

PMS151 `#FF7F00` road fill is 2.53:1 grey and 1.00:1 under red light. A dark casing `#232323` still carries the line. Contour-number FontMarkers on `nztopo50_carto_symbol` (`type = contour_number`) use that same orange with no casing. That pair was missing from the list. Josh chose identifiability over leaving the fill unowned, and rejected pale orange.

### Decision

`reference_inks.project_road` is `#EC7000`. That is the same hue as PMS151, darkened to 3.06:1 grey vs paper. Highway fill stays `#E31A1C`. Do not go paler. Do not go darker: the next steps collide with the highway or become maroon.

Contour-number FontMarkers paint `contours.index.colour`. Shape tells a number from a contour line.

The QGIS apply step paints those two inks. The pair list includes contour-number vs paper, vs road, vs highway, vs index, vs intermediate, and vs the contour label, and road vs highway. Ice contours and pipelines stay out of Map5View.

Red-light road fill stays about 1.16. The casing still carries the line under a headtorch. Orange cannot survive red light and stay orange.

### Rationale

Same-hue orange has one window that still reads as a road, meets 3:1 grey, and stays ΔE ≥10 from taupe contours and from the red highway: L* 61 `#EC7000`. Contour numbers in road orange fail R-17 P7. Putting them on the index ink keeps relief as one family.

### Consequences

The apply step now paints a reference ink. Vector layers the style file does not name still keep LINZ road paint until a later R-15 pass owns those layer ids.

## Contour stroke alpha recedes the 20 m mesh

**Status:** Accepted
**Date:** 2026-11

### Context

Olive-taupe hexes kept L* so dense slopes would not darken (OQ-09). The 0.2 mm index-ink casing on every 20 m line still reads as a solid dark mesh on BX24. Josh asked for a quieter middle ground. Index contours must still meet contrast. Intermediate contours may fail some conditions, including red light.

Opaque index #7A5542 vs paper is 6.55:1 grey and 4.29:1 red. Alpha composites that ink toward paper.

### Decision

contours.index.alpha is 0.85. contours.intermediate.alpha is 0.5. Hexes stay #7A5542 / #B08872. Contour-number FontMarkers stay opaque.

Index vs paper stays a 3:1 grey and red gate after composite (4.60 / 3.28). Intermediate vs paper is measured, not a 3:1 fail gate.

The QGIS apply step paints those alphas with color_rgba. The vector build sets line-opacity from the same numbers. Do not drop the intermediate casing in this step. Do not invent R-13 palettes.

### Rationale

Transparency lowers ink mass without a new brown. Index at 0.85 still meets both paper floors. The busy mesh is the intermediate casing in that same ink. Alpha 0.5 on that casing (and the taupe fill) recedes the 20 m lines. 0.65 was still too heavy on BX24 (log 0054). Dropping the casing was rejected for this play so red-light shape on intermediates remains, weaker.

### Consequences

C6 must not treat intermediate vs paper as a 3:1 gate once pairs include that alpha. Josh accepted index 0.85 and intermediate 0.5 on the BX24 composite (log 0054). Do not keep lowering alpha on this sheet. A steeper Alpine sheet still answers OQ-09. Do not darken the hexes.

## Index contour is 0.35 mm

**Status:** Accepted
**Date:** 2026-11

### Context

Josh accepted contour alphas 0.85 / 0.5 on BX24. The 0.45 mm index then looked too thick. Intermediate 0.2 mm casing was OK. Colour contrast does not depend on millimetres. 0.28 mm vs 0.2 mm was only 1.4x and failed the Port Hills step (log 0038).

### Decision

contours.index.width_mm is 0.35. Intermediate casing stays 0.2 mm. Fill stays 0.12 mm. Alphas stay 0.85 / 0.5.

### Rationale

0.35 vs 0.2 is 1.75x. That is below the 2.25x step at 0.45 mm and above the failed 1.4x step. Vector index stops scale from the 0.45 mm calibration.

### Consequences

Josh accepted 0.35 mm index on BX24 (log 0055), provided contrast still holds. Index vs paper remains 4.60:1 grey and 3.28:1 red. Do not return to 0.28 mm while the casing is 0.2 mm. Do not keep thinning the index on this sheet.

## Closed foot track is a 45° slash in each gap

**Status:** Accepted
**Date:** 2026-11

### Context

The closed foot track was 0.45 mm and nearly solid, with bars at 90°. That line hid contours and read as a railway. Printed Topo50 only changes the gap length. R-11 needs the closed state in shape.

### Decision

The closed line uses the open foot-track weight and dash (0.15 mm, dash 1 mm, gap 0.5 mm). One bar, 1 mm long, sits in each gap at 45° to the line. Log 0056.

### Rationale

90° and 75° read as sleepers. 60° was not a clear cross-out. A bar every 4 mm left most of the line looking open. The 45° slash in every gap crosses the track out without a heavier stroke.

### Consequences

Do not return to the 0.45 mm closed line. The web sprite is still a perpendicular bar. A second apply must write the angle and the gap position onto an existing marker.


## A full-grid stock review gates "met"

**Status:** Accepted
**Date:** 2026-11

### Context

Every "Met when" is a fixed threshold. The loop judged each recommendation on one 1 km square chosen for it. The 4 km BX24 grid then showed label pile-ups, a lost natural-feature cue, dark scrub under contours, and closed-track bars that read as a railway. Each passed its own gate.

### Decision

A recommendation is met only when its threshold holds and a stock-versus-accessible review of the full 4 km grid (`render/bx24-4km`) finds no regression that the change causes. Recorded in `docs/method.md` (log 0057).

### Rationale

Thresholds check one pair at a time. Regressions come from interaction with dense data and neighbouring classes, which only the grid shows. The grid is cheap: one face draw per style, then crops.

### Consequences

Status can go back from met to open after a grid review. The review is a judgement (grade D) until user testing (R-16).
