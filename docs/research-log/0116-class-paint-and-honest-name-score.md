# 0116 — Legend symbols for landuse and structure lines; the score stops counting a name as the mark

**Date:** 2026-11-11

## Question

Thirteen legend rows on `landuse` and `structure_line` drew as the LINZ
default paint (a thick purple-blue bar or a cyan slab), and eleven of them
passed the test tiles. Can the map draw the printed legend symbol for each
class? And why did a wrong symbol pass?

## What we did

- New apply patch `patch_class_paint.py`. It sets both renderers to read
  `type`. Each class in `class_paint` in the style file gets a symbol built
  from a small spec: lines, markers along or at the ends of a line, and a
  point pattern. Every other class gets a copy of the NULL symbol, so no
  class takes a QGIS random colour (log 0114). A type with no stock
  category gets one.
- Drew the 13 classes from the printed legend, at the widths from log 0113.
- Added swatch samples for water race, orchard and walkwire. The stock
  walkwire row prints the word "Walkwire" inside the swatch box, so that
  sample is for the test tiles only and the legend keeps the stock picture.
- Looked at why a mark that a name hides completely still scored as
  visible.

## What we found

| Class | Printed legend | Now |
|---|---|---|
| Cableway | black line, dot at each end | 0.2 mm line, 0.8 mm dots |
| Industrial cableway | black line with open squares | 0.2 mm line, 0.9 mm squares every 3 mm |
| Walkwire | black line, forked ends | 0.25 mm line, 1.4 mm forks |
| Water race | black line with arrow heads | 0.2 mm line, 1 mm arrow heads every 5 mm |
| Boat ramp | white bar, black outline | 0.8 mm black with a 0.4 mm white centre |
| Breakwater, wharf | thick black line | 0.5 mm (wharf edge 0.25 mm) |
| Slipway | black line with cross ticks | 0.25 mm line, 1.2 mm ticks |
| Marine farm | rows of blue dashes | stream blue 0.35 mm dashes |
| Dam | thick black bar | 0.6 mm |
| Weir | black bar across the river | 0.35 mm |
| Cemetery | dashed outline with crosses | 0.2 mm dashes, 1.4 mm crosses |
| Training track | dashed outline | 0.25 mm dashes |
| Orchard, vineyard | rows of green dashes | shelterbelt green dashes and outline |

- **The gate does not test that a symbol is the right symbol.** It tests
  that the ink is visible. `/symbols/` had these rows as "done" with the
  LINZ description. The rows now describe what draws.
- **A black name over a black mark scored as the mark.** The conflict test
  kept a pixel when it matched the paper tile. Name ink and mark ink are
  both black. The tile tool now also draws each conflict with no symbol,
  and the score drops every pixel that the other class inks.
- With that fixed, 12 tiles failed: a name across a line under reduced
  acuity, and the spot-height dot exactly under a grid line or a stream.
- **Name across a line.** A name owns the ground under its letters and
  halo, plus 0.2 mm. The score now measures the line outside that
  footprint: the line must still show on both sides. When the name covers
  80% or more of a mark, the name wins and the tile is not gated. This
  replaces the point-mark rule from log 0113 and covers short line marks
  (weir, dam, cableway).
- **Spot-height dot.** Stock and the apply step drew a 0.3 mm dot. A
  0.35 mm stream or a grid line hides it. It is now 0.6 mm.
- 1182 tiles, 0 fail, 145 not gated with a written reason.

## What changed

- `src/nzat/qgis/patch_class_paint.py`, `tools/style-topo50.json`
  (`class_paint`, `relief.spot_height.dot_mm`), `apply.py`,
  `patch_relief_point.py`.
- `legend_swatches.py` (three samples, `tiles_only`), `render_legend_main.py`.
- `symbol_tile_scenes.py`, `symbol_tiles_main.py`, `tile_visibility.py`,
  `export_symbol_tiles.py`: conflict-alone tiles, the name footprint, the
  walkwire reason.
- `src/nzat/site/symbol_rows.py`: 13 rows.
- The BX24 project and the sheets project are applied again. Tiles, legend,
  crops, face and grid are drawn again.

## Confidence & gaps

Grade D. The symbols are our reading of a 600 dpi legend picture.

- Classes with no legend row (quarry, gravel pit, golf course, landfill,
  mine, rifle range, showground, sportsfield, vehicle track; boom, flume,
  ladder, ski lift, ski tow, spillway edge) keep the LINZ default paint.
  They are cyan slabs or blue bars on `Map5View-all`.
- Both layers stay hidden on the default `Map5View` sheet, as in stock.
- The boat ramp is an open double line, not a closed box.
- The fumarole still draws as a default disc (log 0096 waits for Josh).
- The "right symbol" check is still by eye. No tool compares a tile with
  the legend crop.
