# 0113 — Thicker point marks and thin lines; the halo stays 0.4 mm

**Date:** 2026-11-10

## Question

Josh wants every symbol to pass the test tiles before the tile and vector
work starts. After the score rules (ink beside visible ink counts; area
fills, hidden classes and accepted contours are not gated), 77 tiles and 15
symbols still failed. Which marks need more ink, and does a thinner name
halo help?

## What we did

- Drew each failing mark at trial widths on a scratch copy of the project,
  and took the smallest width that passed every tile.
- Drew the name tiles at halo 0.4, 0.2 and 0.1 mm, and three BX24 areas at
  0.4 and 0.2 mm (Port Hills, Cashmere, the estuary).

## What we found

| Symbol | Before | Now |
|---|---|---|
| Hot spring cross | stock hairline | 0.35 mm stroke |
| Tank ring | 0.15 mm | 0.25 mm (0.35 mm closes a 1.4 mm ring) |
| Embankment, stopbank | 0.06 mm line, 0.1 mm ticks | 0.15 mm line, 0.2 mm ticks |
| Unmetalled road | white centre 0.35 mm | white centre 0.25 mm (stock) |
| Fence | 0.15 mm | 0.2 mm |
| Ice contours | 0.12 mm | 0.2 mm (0.15 mm failed under a grid line) |

- **Unmetalled road.** Two dark edges carry this road. N-1 (log 0097)
  raised the white centre to the 0.35 mm navigation floor. That thinned
  each edge to 0.125 mm, and reduced acuity lost the road. With the stock
  0.25 mm centre on the 0.6 mm casing, each edge is 0.175 mm.
- **Halo.** At 0.2 mm the spot height under a name still fails. At 0.1 mm
  every name tile passes, but the mark runs into the letters. On the map,
  0.2 mm helps black names in towns (a smaller grey blob) and hurts brown
  names on contours and blue names on stipple, where the ink behind is the
  same colour. Log 0041 had already rejected 0.25 mm as too thin.
  **Decision (Josh):** keep 0.4 mm. A name on a point mark is not gated:
  the name wins. A name across a line is gated.
- 17 tiles and 7 symbols fail now: cemetery and training track
  (protanopia), depression contours under a name, ice contours on native
  forest, floodgate on water and urban, and unmetalled road and one-lane
  bridge on urban fill under reduced acuity. No tile got worse.

## What changed

- `tools/style-topo50.json`: `springs.hot.stroke_mm`,
  `structures.tank_water.stroke_mm`, `relief.embankment`,
  `sizes.fence_line_mm`, `sizes.ice_contour_mm`.
- `patch_springs.py`, `patch_thin_lines.py`, `patch_road_widths.py`, the
  tank SVG.
- `symbol_tile_scenes.py`: a name on a point mark is not gated.
- `site/src/data/symbol-tiles.json`, the tile strips, the page text.

## Confidence & gaps

Grade D. The widths are the smallest that pass our own score.

- The BX24 face and grid are not redrawn for these changes yet.
- The halo could differ by name colour (black 0.2 mm, others 0.4 mm). Not
  done.
- The fumarole still draws as a default disc (log 0096 waits for Josh).
