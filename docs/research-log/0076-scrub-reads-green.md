# 0076 — Scrub reads green again

**Date:** 2026-11-05

## Question

Log 0071 left the scrub class cue weak at sheet size. The fill was
`#A3CC90` at alpha 26. On paper that is `#F6FAF4`, ΔE 4.2 from white. Can
the fill read as vegetation again and still keep index contours ≥3:1 in
red light (B-34)?

## What we did

Red light reads only the red channel (`palette_audit` model). So the fill
can gain green and lose blue, while its red channel stays near the current
value. Scored composite fills against paper, native forest, and the index
contour with the `nzat.colour` models. Ran the pair audit. Rendered the
grid and compared `1576000-5174000` (Mount Pleasant scrub slopes).

## What we found

| Fill on paper | ΔE vs paper | ΔE vs native | Index red CR |
|---|---|---|---|
| Stock `#EDF7DF` | 11.6 | 2.2 | 2.90 |
| Log 0071 `#F6FAF4` | 4.2 | 8.7 | 3.02 |
| Greenest tried `#F6FFE1` | 12.8 | 3.1 | 3.09 |
| Chosen `#F4FFEC` (`#D6FFAA` at 55) | ~10 | 4.5 | 3.04 |

The chosen fill is about as visible on paper as stock scrub, and twice as
far from native forest as stock. Index on scrub is 4.48:1 grey and 3.04:1
red. Native versus scrub is still 1.12:1 in grey. The plant marks carry
that split (R-10), as before.

On the render, the Mount Pleasant and Heathcote slopes read as pale green
again, with the green arcs on top. Contours stay visible.

## What changed

- `vegetation.scrub` `#D6FFAA`, alpha 55 in `tools/style-topo50.json`.
- Tests and `docs/style-topo50.md`, B-34.

## Confidence & gaps

Grade D for the visual judgement, C for the contrast numbers. Red-light
headroom is small (3.04). G5 still needs a full-grid review.
