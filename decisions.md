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
