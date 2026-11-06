# 0097 — Navigation line floor 0.35 mm

**Date:** 2026-11-06

## Question

Josh asked for a 0.35 mm floor on primary navigation lines only: roads,
tracks, and streams (not every line on the sheet). How do we apply that from
the style file, and what happens when streams and index contours share the
same width?

## What we did

Added `sizes.navigation_line_mm` 0.35 to `tools/style-topo50.json`. Wired
apply:

- `patch_road_widths.py` raises painted road fills, sealed lane-count
  expressions, and unmetalled white centre lines to the floor.
- `patch_tracks.py` sets foot and vehicle track weights and scaled dashes;
  closed × size 1.25 mm.
- `water.stream_width_mm` 0.35; drains stay 0.15 mm.

Added tests. Applied the BX24 accessible project. Rendered G1 cell
`1576000-5166000` (55 s). CI: ruff, 68 pytest, C1–C6.

## What we found

### Stream versus index contour (R-01)

Both lines are now **0.35 mm** on the sheet. Greyscale ink contrast for
stream `#004C99` versus index `#7A5542` is still **1.83:1** (unchanged).
Josh closed the pair in log 0093 with a **width step** (0.25 mm stream vs
0.35 mm index) plus hue and red light. That width step is **gone**.

**Needs Josh:** a new shape or ink cue for stream vs index, or an explicit
exception. Do not decide in code.

### Grid review

Full BX24 4 km grid stock review (method.md) is **not** run in this log.
G1 spot render only.

## Files

- `tools/style-topo50.json`, `patch_road_widths.py`, `patch_tracks.py`,
  `navigation_line_mm.py`, tests, `docs/style-topo50.md`.
