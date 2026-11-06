# 0099 — Darker shelterbelt and tree ink

**Date:** 2026-11-06

## Question

Shelterbelt lines and tree points share `#1D9D00`. They pass R-01 (3.57:1 on
paper) but look low contrast on native fill, especially at 0.2 mm stroke width.

## What we did

Lowered CIELAB L* on the same hue with `darken_for_text` to **4.5:1** grey on
paper and **3:1** red light. New `reference_inks.shelterbelt`: **`#008A00`**.

Apply still rewrites Map5View `(148,255,59)` on shelterbelt lines and tree
SvgMarkers. Trees and shelterbelts stay one ink.

## What we found

| Pair | `#1D9D00` | `#008A00` |
|------|-----------|-----------|
| vs paper (grey) | 3.57:1 | **4.52:1** |
| vs native fill (composited) | 3.05:1 | **~3.86:1** |
| vs paper (red light) | 16.9:1 | 21.0:1 |

## Confidence & gaps

Grid review on dense and urban cells after re-apply. Orchard/mangrove legend
proposals still name `#1D9D00` in text until those rows are applied.
