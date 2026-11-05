# 0095 — A definition table for every legend symbol

**Date:** 2026-11-06

## Question

The stock Topo50 legend lists about 90 rows. What does the accessible sheet draw for each symbol? Which symbols fail the project floors? What accessible form keeps the LINZ shape?

## What we did

- Read every row of the stock legend image `topo-legend-1.tif`. Split rows with two to four symbols by x. The result is 124 legend symbols, plus bivouac and hut, which the sheet draws but the legend does not list.
- Found the layer and rule for each symbol in the stock project, Map5View theme. Read the applied BX24 project for the inks and sizes the sheet draws.
- Read the SVG files for marker strokes and fixed colours.
- Sampled the legend image for symbols the sheet does not draw.
- Tested each symbol with the `nzat.colour` models (`pair_audit`): contrast on paper and on the fill under it, red light, worst dichromacy ΔE.
- Floors: 3:1 for the ink that draws the shape (R-01, F-20). 3:1 under red light (R-01, R-11). Lines and strokes 0.15 mm or more (F-31). Marks 1.4 mm or more (F-31). No meaning by colour alone (R-17). A symbol the sheet draws as another symbol fails "own symbol".
- Wrote a proposal for each symbol that fails or that the sheet does not draw. Each proposal keeps the LINZ shape. Inks are owned inks or a stock hue darkened with `darken_for_text`.
- Built `/symbols/` on the site beside `/inks/`.

## What we found

### Counts

- 126 symbols. 38 done. 34 proposed. 54 blocked.
- Blocked means the sheet does not draw the symbol. Map5View hides `structure_line`, `structure`, `tunnel_line`, `water_point`, `landcover_point`, `landuse` and `marine`. All `relief_line map` rules are switched off. Some classes are not in the data (tramway, orchard, mangrove).
- Each blocked symbol still has a proposal.
- Track rows are done. They take the log 0094 symbols.

### Main fails on the sheet

- Stroke width, 14 symbols. Many SVGs draw strokes under 0.15 mm at sheet size: church 0.04 mm, shipwreck 0.06 mm, bivouac 0.09 mm, tower 0.09 mm, redoubt 0.10 mm, mast 0.10 mm, beacon 0.11 mm, shingle texture 0.05 mm.
- Mark size, 9 symbols. Trees draw as a 0.05 mm dot. Hut is 0.8 mm. Church is 1.0 mm tall. Tank and floodgate are 1.0 mm.
- Own symbol, 9 symbols. Double track draws as single track. Depression contours have no ticks. Supplementary contours are not dashed. Saddle draws as a spot-height dot. Moraine, scree and shingle draw the same texture. Exotic non-coniferous draws conifer marks.
- Contrast and red light: the vegetation outline `#A7C05E` is 2.03:1. Exotic marks are `#9DCE69`, 1.83:1. Scattered scrub `#B2DF8A` is 1.52:1. Moraine wall `#F000EC` is 1.14:1 under red light.
- Colour alone: a locked gate is a gate bar in `#FF4500`. Red light is 1.0:1.
- Line width: fence 0.05 mm. Two-lane bridge casings 0.1 mm.

### Colours that do not draw

- An SVG with fixed colours ignores the colour set in QGIS.
- So bivouac `#D5B43C`, beacon `#BEB297`, redoubt `#987DB7`, mast `#FF9E17`, tower `#E5B636`, golf `#A47158` and opencast mine `#729B6F` draw near-black.
- Exotic forest marks draw `#9DCE69` from `exotic_con.svg`, not the set `#E748A2`.
- A QGIS `line` marker draws its stroke only. The `#FF0000` fills on bridge ticks and church do not draw.
- So the quick-scan fails for these inks are not on the sheet. Their real fails are stroke width.

### Excluded

- Rules that never draw a real class: `relief_line map` ELSE `#F000EC`, `vegetation map` NULL `#FF85F9`, `vegetation_line map` empty class `#FF009F`, hidden `bridge_line` `#FF85F9`.

### Proposals that need Josh

- Locked gate: a black bar with a filled 0.6 mm square at its middle. A second bar would read as a cattlestop.
- Fumarole: a black 2 mm ×. The hot spring is a black ×, so the two differ by size only.
- Trees: the LINZ tree mark at 1.4 mm in `#1D9D00`. The data has many trees, so this may crowd.
- Scattered scrub: `#6A9A50` arcs at 1.4 mm on a 5 mm grid. Scrub and scattered scrub then differ by spacing and fill.
- Vegetation outline: darken `#A7C05E` to `#859E3E` (3.02:1) on every vegetation polygon.
- Buried gas pipeline: darken `#EA6300` to `#951600` for red light, with a long dash.
- Bivouac uses the LINZ cave glyph. Keep it or draw the LINZ bivouac.
- Blocked layers: show `water_point`, `structure_line` and the `relief_line` rules on the sheet, or leave them off.

## What changed

- New `src/nzat/site/symbol_rows.py`: one entry per symbol, with box, layer, measured form, proposal and status.
- New `src/nzat/site/symbol_checks.py`: the floor checks. Pure, no QGIS.
- New `src/nzat/site/export_symbol_table.py` and `tools/export_symbol_table.py`: write `site/src/data/symbols.json` and the crops in `site/public/symbols/`.
- New page `site/src/pages/symbols.astro`, linked in the nav and from the overview.
- Tests: `tests/site/test_symbol_table.py`.
- The generator reads the stock legend TIFF and the accessible legend PNG outside the repo. CI does not run it. Its outputs are committed.
- No map style change. Josh reviews the table first.

## Confidence & gaps

- Sheet inks and sizes come from the project XML and the SVG files. No new render was made.
- Legend widths for blocked symbols are pixel runs at 600 dpi. They are within about 0.05 mm.
- The 0.15 mm line floor is the thinnest step the sheet accepts (log 0071). The 0.35 mm figure in F-31 is the thin end of a same-colour family, not a floor for every line. Josh to confirm.
- Building squares, spot-height dots, track dots, polygon outlines and contour steps are exempt from the size floor. The table names the reason for each.
- "Ours today" crops exist only for the 18 rows the accessible legend redraws.
- Splits of a row by x are by eye. Some crops show a part of the next symbol.
