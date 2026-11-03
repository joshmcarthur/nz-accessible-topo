# 0053 — Contour stroke alpha recedes the 20 m mesh

**Date:** 2026-11-03

## Question

Can a little transparency quiet the contour mesh on steep ground without dropping index contours below 3:1 vs paper?

## What we did

Kept the olive-taupe hexes. Set `contours.index.alpha` to 0.85 and `contours.intermediate.alpha` to 0.65 in `tools/style-topo50.json`. The QGIS apply step paints those alphas with `color_rgba`. The vector build sets `line-opacity` from the same numbers. Contour-number FontMarkers stay opaque.

Index vs paper after composite is 4.60:1 grey and 3.28:1 red. Intermediate casing vs paper is 2.99:1 grey and 2.36:1 red. Intermediate vs paper is no longer a 3:1 fail gate. C6 uses a 1.5 floor on that pair so a line that nearly vanishes still fails.

Drew the Port Hills square at 600 dpi.

## What we found

Opaque index-ink casing on every 20 m line was the busy mass (OQ-09). Alpha lowers that mass without a new brown. Index still meets both paper floors. Intermediates recede and may fail red light.

## What changed

- `tools/style-topo50.json` contour alphas.
- QGIS apply, vector build, pair files, and tests.
- The Port Hills accessible square.

## Confidence & gaps

This is a first play. If the mesh is still too heavy, lower intermediate alpha next. Do not darken the hexes. Do not redraw the BX24 composite until this square is accepted.
