# 0040 — Thinner label halo

**Date:** 2026-11-02

## Question

Can the opaque label buffer stay thin enough that it does not hide the map under the letters?

## What we did

Drawn map-label buffers were 1 mm, or 0.5 mm on three layers. The buffer is opaque. That width covers contours, roads, and vegetation.

`label_contrast.halo_max_mm` is 0.25. The QGIS apply step caps a drawn buffer at that width. A buffer that is already thinner stays. The buffer colour stays. The buffer alpha stays 1. Label ink stays. Vector `text-halo-width` stays.

## What we found

A 0.25 mm buffer is a thin edge around the letters. The contrast floor does not depend on the width. R-07 stays met on the same ink and the same opaque buffer colour.

## What changed

- `tools/style-topo50.json` holds the 0.25 mm cap.
- `tools/override_topo50_project.py` caps `bufferSize`.
- The four accessible square pictures in `docs/visuals/squares`.
- `docs/visuals/10-bx24-compare.png` is the BX24 map face again. Stock is on the left. Accessible is on the right.

## Confidence & gaps

0.25 mm is the smallest width that still separates the letter edge from the map at this render. A line can still cross an open counter. That is the point of the thinner buffer.
