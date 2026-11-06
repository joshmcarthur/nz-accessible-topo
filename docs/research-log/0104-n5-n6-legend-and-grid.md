# 0104 — N-5 themes applied, N-6 legend rows, BX24 grid redrawn

**Date:** 2026-11-06

## Question

Can apply write `Map5View-paper` and `Map5View-all`, and can the legend redraw
the remaining stock-look rows from the map without wiping rows that have no
class?

## What we did

- Re-applied `$W/accessible/nztopo50.qgs` from stock. The project now has
  `Map5View`, `Map5View-paper` (39 visible layers), and `Map5View-all` (47
  visible layers, including `water_point`, `structure_line`, `tunnel_line`,
  `landcover_point`, `landuse`, `marine`, `structure`, `structure_point`).
- Rendered the BX24 4 km face on `Map5View` and cropped the 27-cell grid.
- Rendered a 1 km `--theme Map5View-all` square at Rhodes Spring
  (`1569000,5165000`).
- Added legend swatches for drawable N-6 rows. A swatch box does not cover a
  blocked row. `render_legend.py --theme Map5View-all` drew the PNG.
- Exported `/symbols/` (91 done, 4 proposed, 31 blocked).

## What we found

- Stream `#00276D` on steep `1580000-5154000` still reads as water, not as a
  black track. Contours stay brown. Closed × on G1 cells still reads as a
  track mark, not a railway.
- The all-theme spring square draws the cold-spring circle at Rhodes Spring.
  `structure_line` is on. This BX24 project has no power-pylon class, so the
  square has no power line. Cliff ticks show in the legend cliff swatch.
- Tunnel, cableway, cemetery, springs, and other `all_layers` classes move
  off blocked when Map5View-all can draw them. Ford, orchard, mangroves,
  pipelines, power, telephone, gas, and bore stay blocked: no class.
- Fumarole, marine farm, and waterfall stay proposed. Fumarole still waits
  on log 0096.
- Some new swatches are empty or still stock-wrong at sheet size (gate
  glyphs, several relief lines, fumarole). Spot-height numbers cannot use a
  point on `nztopo50_carto_text` (that layer is a line). A hex colour on that
  layer drew magenta, so the number was dropped.

## What changed

- `src/nzat/qgis/legend_swatches.py`
- `src/nzat/qgis/render_legend_main.py` (`known_swatch_attrs`)
- `src/nzat/site/symbol_rows.py`
- `tests/qgis/test_legend_swatches.py`, `tests/site/test_symbol_table.py`
- `site/src/data/symbols.json`, `site/public/symbols/*.png`

## Confidence & gaps

N-7 (445 sheets) and N-8 (vector parity) are not done. Josh still reviews
`render/bx24-4km/*-accessible.png` and `/symbols/`. Power lines on `-all`
need a sheet that has that class.
