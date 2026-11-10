# 0110 — Symbol test tiles, and contours draw solid again

**Date:** 2026-11-10

## Question

Does each legend symbol stay readable on each fill, and when another class
crosses it? The pair file tests two inks at a time. The 4 km grid shows only
the combinations that BX24 holds.

## What we did

New tool `tools/render_symbol_tiles.py`. It draws each legend swatch sample
in 10 mm tiles at sheet size, 600 dpi, through the applied map layers
(`Map5View-all`). Ten tiles put a fill under the symbol: paper, native,
exotic, scrub, scattered scrub, water, urban, sand, swamp, ice. Five tiles
put another class across it on paper: a 1 mm contour mesh, a grid line, a
stream, a two-lane road, and a flat black name. An area symbol gets the
paper tile and the five conflicts only.

86 swatch keys give 1146 tiles in about 60 s. The output is
`render/symbol-tiles/` (not committed).

## What we found

- **Every contour on the accessible face was dashed, 5 mm on and 2 mm off.**
  The contour mesh tile showed it. The BX24 face showed the same against
  stock. It started in commit `8bf7282` (log 0101). The apply step sets a
  data-defined `customDash` of `if(supplementary, '3;1', '5;2')`. QGIS
  applies a data-defined dash even when `useCustomDash` is false. A NULL
  dash does not turn it off: QGIS falls back to the stock `5;2`. One very
  long dash (`10000;0`) draws a solid line. Supplementary contours stay
  dashed.
- The face that Josh signed off in log 0107 had the dashed contours. The
  4 km review did not catch it. Index contours looked like short thick
  marks, and intermediate contours looked broken.
- Urban and water fills hide contours, streams, trig points, fences and
  spot heights under them. The stock face does the same. This is the LINZ
  layer order, not our change.
- The accessible road casing is a hairline. Stock shows a clear dark
  casing. This is not measured yet.
- The name halo hides a trig point or a track under the name.

## What changed

- `tools/render_symbol_tiles.py`, `src/nzat/qgis/symbol_tiles_main.py`,
  `src/nzat/qgis/symbol_tile_scenes.py`.
- `src/nzat/qgis/swatch_layers.py`: the swatch-layer code, moved out of
  `render_legend_main.py` so the legend and the tiles share it.
- `src/nzat/qgis/patch_contour.py`: a normal contour takes `10000;0`, not
  `5;2`. Test in `tests/qgis/test_patch_contour.py`.
- The BX24 project is applied again and the 4 km grid is drawn again.

## Confidence & gaps

Grade D: our own review of our own render. The solid-line fix is checked on
the contour tile and on the BX24 face.

- The tiles are not scored yet. The next step measures each symbol against
  the pixels around it under each vision condition.
- The in-situ crops on `/symbols/`, the legend picture and the 445 sheet
  rasters were drawn before this fix. They still show dashed contours.
- The conflicts draw on paper only. A conflict on a fill is not drawn.
