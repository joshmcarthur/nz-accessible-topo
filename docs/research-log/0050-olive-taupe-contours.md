# 0050 — Olive-taupe contours leave the orange/red axis

**Date:** 2026-11-03

## Question

Can contour inks meet R-04 ΔE ≥10 against painted PMS151 roads and red highways without making those roads pale?

## What we did

Kept road fill `#FF7F00` and highway fill `#E31A1C`. Shifted both contour fills by the same CIELAB offset: L* unchanged, a* −8, b* −22. Index is `#7A5542`. Intermediate is `#B08872`. Casing stays the index ink. Owned those values in `tools/style-topo50.json`. Applied the QGIS project. Rebuilt the vector style. Drew the four accessible squares.

## What we found

Same-hue orange cannot close the pairs without a pale landmark (log 0049). Protanopia collapses a*, so a green-olive shift alone cannot separate index from highway. Reducing b* moves the contour off the yellow-red axis protans still see. Reducing a* takes remaining redness out of the brown.

Painted pairs now meet ΔE ≥10. Index versus paper is 6.53:1 grey and 4.30:1 red. Intermediate fill stays lighter, so dense 20 m lines stay recessive. Pipeline is not on Map5View.

## What changed

- `tools/style-topo50.json` contour fills and casing.
- Pair why-text, tests, vector styles, and tokens.
- The four accessible square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

R-04 is met on the painted Map5View inks. A steep sheet still answers OQ-09. R-13 stays unnamed.
