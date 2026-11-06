# 0105 — Stream ink back to `#004C99`

**Date:** 2026-11-06

## Question

Does stream `#00276D` still read as water where it runs beside a black track?

## What we did

Josh reviewed the 0104 grid. He preferred the older stream ink. We restored
`reference_inks.stream` to `#004C99` (log 0083). Swamp marks use the same ink.
Widths stay 0.35 mm rivers and canals, 0.15 mm drains.

## What we found

`#00276D` is too dark. Next to a foot track it reads as another black line.
Hue still separates stream from index contour (red 6.41:1). Grey contrast
versus the painted index is 1.83:1 again. Josh accepts that. The cue against
a track is more important on the grid than a 3:1 grey step versus index.

## What changed

- `tools/style-topo50.json` `reference_inks.stream` and swamp mark colour
- tests, `docs/style-topo50.md`, `BACKLOG.md`, `/symbols/` stream hex

## Confidence & gaps

Confirm on steep `1580000-5154000` and a cell where a stream runs beside a
track. Index versus stream in grey stays a known fail.
