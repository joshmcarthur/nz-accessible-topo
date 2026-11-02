# 0041 — A little more label buffer

**Date:** 2026-11-02

## Question

Is 0.25 mm enough buffer once the full sheet is in view?

## What we did

The 0.25 mm cap was reviewed on the BX24 compare. The edge was too thin. `label_contrast.halo_max_mm` is now 0.4. The buffer stays opaque. Label ink stays. Vector `text-halo-width` stays.

## What we found

0.4 mm is still well under the stock 1 mm buffer. It gives a slightly wider white edge. A line can still cross an open counter.

## What changed

- `tools/style-topo50.json` holds the 0.4 mm cap.
- The four accessible square pictures in `docs/visuals/squares`.
- `docs/visuals/10-bx24-compare.png`.

## Confidence & gaps

This is a review adjustment. It does not change the contrast floor.
