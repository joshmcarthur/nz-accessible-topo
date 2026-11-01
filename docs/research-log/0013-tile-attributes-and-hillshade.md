# 0013 — What can a style actually use? (OQ-12)

**Date:** 2026-11-01

## Question
Do the vector tiles carry the attributes our recommendations need, and how is
relief shading produced on the web?

## What we did
- Walked every filter expression in `topographic-v2.json` to list
  source-layers, attributes and values the style relies on.
- Inspected the hillshade layer.
- Searched MapLibre docs for multidirectional hillshade support.
- Hand-measured the index-contour colours the audit tool skipped.

## What we found
- Closed tracks, scattered scrub, index contours: all available as
  attributes → R-04, R-10, R-11 are implementable as pure style changes.
- Contour `definition` (indefinite) isn't used by the style; unknown whether
  it's in the tiles.
- Hillshade is client-side at 315°, overriding MapLibre's 335° default.
  Multidirectional shading is supported natively since style spec 23.2.0.
- Index contours are paler (1.71–2.27:1) than intermediates. The audit tool
  has a blind spot for interpolated colours — noted for a future fix.

## What changed
- `docs/current-state/tile-attributes.md`; sources added; OQ-12 partly
  answered.
