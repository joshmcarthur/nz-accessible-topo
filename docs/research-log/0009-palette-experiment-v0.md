# 0009 — Palette experiment v0

**Date:** 2026-11-01

## Question
Can the measured problems W1–W8 be fixed by changing colours, or do they
need pattern/shape changes too?

## What we did
- Tried several candidate contour browns, water-label blues and scrub
  greens in a scratch script, keeping the candidates that met: contour ≥3:1
  on white (WCAG 1.4.11), ΔE ≥10 against highways for all dichromacies;
  water label ≥4.5:1 on its halo.
- Recorded chosen candidates as `tools/pairs-proposed-v0.json`.
- Added a "historic site label vs paper" pair to the baseline — the earlier
  pairs only compared symbols to each other, not to the paper, which hid the
  red-light problem (baseline result: 1.62:1).
- Extended `palette_audit.py` so `STYLE` can be `-` to audit a pairs file
  alone.

## What we found
- Contours, contour/highway and water-label contrast: fixable with colour.
- Vegetation classes and water vs scrub: **not** fixable with colour alone
  within the light range fills must occupy → need patterns/edges.
- Closed tracks and historic sites: fix by moving meaning into shape.

## What changed
- `docs/palette-experiments/`, `tools/pairs-proposed-v0.json`, regenerated
  baseline audit, tool tweak.

## Confidence & gaps
- Model-only (grade D). Visual weight of darker contours is untested.
