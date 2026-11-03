# 0051 — Darker orange roads and index-ink contour numbers

**Date:** 2026-11-03

## Question

Is PMS151 road fill accessible? Are contour numbers on the pair list?

## What we did

Named every Map5View class a navigator must tell apart. Contour-number FontMarkers on `nztopo50_carto_symbol` (`type = contour_number`) painted PMS151 `#FF7F00` with no casing. That pair was missing.

Road fill `#FF7F00` is 2.53:1 grey and 1.00:1 under red light. The `#232323` casing is 15.72:1. Josh chose to own the fill, not leave it to the casing. Pale orange is not a landmark.

`reference_inks.project_road` is `#EC7000`. Same hue as PMS151. Grey vs paper is 3.06:1. ΔE vs taupe contours and vs highway `#E31A1C` stays ≥10. The apply step paints that ink on two-lane and sealed fills. Highway fills stay red.

Contour-number FontMarkers now use index `#7A5542`. Shape tells a number from a contour line.

## What we found

Same-hue orange has one window that still reads as a road, meets 3:1 grey, and stays off both taupe contours and the red highway: L* 61 `#EC7000`. Darker than that becomes maroon or collides with the highway. Red-light fill is still 1.16. Orange reflects like paper under a headtorch. The casing still carries the line then.

## What changed

- `tools/style-topo50.json` `reference_inks.project_road`.
- The QGIS apply step paints that fill and the contour-number marker.
- `tools/pairs-topo50-accessible.json` includes contour-number pairs and road vs highway.
- The four accessible square pictures in `docs/visuals/squares`.

## Confidence & gaps

Vector layers the style file does not name still keep LINZ road paint. Ice contours and pipelines are not on Map5View. A steep sheet still answers OQ-09.
