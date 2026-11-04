# 0063 — One topographic style pass

**Date:** 2026-11-04

## Question

Can one apply pass close the pair floors for the locked style updates (scrub, stream, shelterbelt, grid, closed-track ×, natural-name Bold, contour-number FontMarkers, spot-height urban halo, native tree marker) without a new hue?

## What we did

Lightened scrub first. Kept hex `#A3CC90`. Set alpha to 26 (QGIS byte). The hatch still carries the class (R-10).

Darkened stream, shelterbelt, and grid along CIELAB L* and kept hue. New hexes: stream `#0064BD`, shelterbelt `#1D9D00`, grid `#269FD2`. Apply rewrites Map5View RGB `(0,158,255)`, `(148,255,59)`, and `(41,160,211)` on every layer, including `water_line map`, coastline, water outlines, shelterbelt lines, green dots, and grid lines.

Closed-track gap marks use SimpleMarker `cross2` at 0°. Interval and offset stay one mark per gap.

Natural italic/narrow carto_text styles map to Atkinson Bold. Empty style stays Regular. Italic is still forbidden.

Contour-number FontMarkers are Regular, not italic, at least 6 pt, in the index ink. The existing text-mask still breaks the contour casing under the number.

Spot-height layers that contain `relief_point` use urban fill `#BCBAB6` as the halo colour.

Native tree markers: `vegetation.native.marker` is `#3F6B32`. Apply paints PointPatternFill, SimpleMarker, FontMarker, and SvgMarker colour under the native symbol when that layer is already in the project. It does not add a glyph.

Re-exported `/inks/`. 51 pairs, 30 fail R-01 grey or red 3:1.

## What we found

Index versus scrub is 4.35:1 grey and 3.02:1 red. Stream versus paper is 5.90:1. Stream versus urban is 3.05:1 grey (the binding fill). Shelterbelt versus paper is 3.57:1. Shelterbelt versus native is 3.05:1. Grid versus paper is 3.01:1.

Worst CVD ΔE for darkened stream versus index contour is 35.9. Shelterbelt versus index is above 10. Hue did not change.

The BX24 accessible project native symbol is SimpleFill only. There is no tree marker to paint. Exotic forest already has an SVGFill. This pass does not copy that SVG onto native.

Remaining pair fails are the rows that this pass left on purpose: intermediate-on-fill (casing is the shape cue), index versus urban and versus native/water under red light, vegetation outline versus paper, exotic fill versus paper, contour-versus-stream grey (ΔE still 35.9; weight still differs), and older road/highway/contour-number pairs.

QGIS 4.2.3 and the BX24 project are on this machine. Grid review G1, G3, G4, G5, and G6 is not in this log. Next step is apply, render the 4 km square, crop, and compare.

## What changed

- `tools/style-topo50.json` holds the new hexes, scrub alpha 26, native marker colour, closed-track `cross2`, and Bold for natural names.
- Apply owns those inks: `patch_owned_lines`, `patch_vegetation` marker paint, `patch_tracks` ×, `patch_labels` Bold, `patch_contour_numbers` upright size floor, urban halo on `relief_point`.
- `site/src/data/ink-matrix.json` matches the new config.
- This log. Pair floors match the locked choices. B-34, B-35, B-36, B-30, B-32, B-37, B-33, and B-38 stay open until grid review. R-01 is not met.

## Confidence & gaps

The audit measures configured inks. Anti-aliased stream pixels on the face will be lighter than `#0064BD`. Native has no tree glyph on BX24, so B-38 still needs a marker in the project or a later choice. Vegetation outline `#A7C05E` still fails versus paper. Island outline already passed and was not darkened.
