# 0034 — Vegetation pattern

**Date:** 2026-11-02

## Question

Do vegetation classes that affect travel have a pattern as well as a tint?

## What we did

`vegetation.scrub.colour` is `#A3CC90`. `vegetation.scattered.colour` is `#E0EDD8`. Both numbers live in `tools/style-topo50.json`.

The vector build reads those colours. Scrub fill is `rgba(163, 204, 144, 1)`. Scattered fill is `rgba(224, 237, 216, 1)`. The stipple layer stays. The build does not keep those two colours in `P`.

The QGIS apply step paints the scrub fill and the line hatch. It keeps the stock scattered-scrub dots. It does not add a fill under those dots. Native forest stays `#E1EAC3`. The water shoreline stays blue.

The four squares were drawn again at 600 dpi. The cold-spring square shows a hatch on the darker green. The paler green has no hatch. The estuary word is `Estuary`. The square has no black question marks.

## What we found

Scrub versus scattered scrub on the vector pair list is ΔE 15.3 normal, 13.8 protan, 13.4 deutan, 13.4 tritan. Grey contrast is 1.49:1. The stipple carries that pair in greyscale.

Native forest versus scrub on the raster pair list is grey 1.45:1. That is why scrub also has a hatch. That pair is also R-17. This step does not change the native fill.

The pair audit is otherwise unchanged. Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/style-topo50.json` holds the scattered fill colour.
- `tools/build_style.py` reads the vegetation fills from that file.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

R-10 is met for this list. The next step is R-11.
