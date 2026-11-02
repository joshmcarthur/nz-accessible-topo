# 0030 — Mac QGIS cannot draw the square

**Date:** 2026-11-02

## Question

Can the QGIS app on this Mac draw a 1 km square faster than the `map` image?

## What we did

Pointed `tools/render_square.py` at `QGIS_PREFIX_PATH`. An empty value stays `/usr`. Ran one stock estuary square with `/Applications/QGIS.app`.

## What we found

The app is QGIS 3.36.3-Maidenhead. The project was saved by QGIS 4.0.3-Norrköping. The app prints that warning. `Map5View` then has no valid layers. The run stops in about 8 seconds. It writes no picture.

The national file read is still there. This app does not reach that read. Square draws stay on the `map` image.

## What changed

- `tools/render_square.py` reads `QGIS_PREFIX_PATH`.
- `docs/style-topo50.md` records the version gap.

## Confidence & gaps

R-09 stays open. The hierarchy list is still not named. Do not start R-07.
