# 0102 — Darker stream versus index contour

**Date:** 2026-11-06

## Question

N-1 made streams and index contours both 0.35 mm. Grey contrast for stream
`#004C99` versus painted index was 1.83:1. Josh closed that pair in log 0093
with a width step that is now gone. Josh asked to darken the stream and keep
0.35 mm.

## What we did

Kept hue with `darken_for_text` until grey contrast versus the **painted**
index (`#7A5542` at alpha 0.85 on paper) reached 3:1. That is the same
composite log 0083 used.

## What we found

| Pair | `#004C99` | `#00276D` |
|------|-----------|-----------|
| vs painted index (grey) | 1.83 | **3.01** |
| vs painted index (red) | 6.41 | 6.41 |
| vs paper (grey) | 8.42 | 13.87 |
| vs opaque index (grey) | 1.29 | 2.12 |

A 3:1 floor against the opaque index hex needs `#000046`. That mark is almost
black. We did not use it.

## What changed

- `reference_inks.stream` `#00276D`
- swamp fill reads that ink
- tests, `docs/style-topo50.md`, `/symbols/` stream hex

## Confidence & gaps

Pair numbers are models. Grid review on steep `1580000-5154000` still has to
show that streams do not read as black tracks.
