# 0082 — Contour numbers get a halo and their real face

**Date:** 2026-11-05

## Question

Josh asked for a small halo on contour labels.

## What we did

Contour numbers are not labels. The `contour_number` label rule on
`nztopo50_carto_symbol` is inactive. Each digit is a point feature drawn by
a FontMarker, with data-defined `char` and `angle`. Read the applied
FontMarker options. Rendered a 700 × 600 m area at 1200 dpi to test each
halo method.

## What we found

- The FontMarker still said `Nimbus Sans LINZ`, `Narrow Italic`. Log 0063
  wrote `fontFamily` and `fontStyle`. FontMarker reads `font` and
  `font_style`. The test fixture used the same wrong names, so it passed.
  The accessible render loads no Nimbus file, so Qt drew a fallback face.
- A white stroke on the digit itself covers the digit. The stems are about
  as thin as a 0.3 mm stroke.
- A white copy of the digit drawn first, with a stroke, also hid the digit.
  The stock layer uses `featureBlendMode` 1 (DestinationOver), which puts
  each new paint behind what is already there.
- With normal blending (0), the white copy draws first and the brown digit
  draws over it. The halo also breaks the contour line behind the number.

## What changed

- `patch_contour_numbers` writes `font` and `font_style`, adds a
  paper-coloured FontMarker copy with a `contours.number_halo.width_mm`
  (0.3 mm) stroke before the digit, and sets the layer blend to normal.
- `contours.number_halo` in `tools/style-topo50.json`.
- The test fixture uses the stock option names.
- `docs/style-topo50.md`, B-37.

## Confidence & gaps

Grade D. Normal blending also applies to shields, golf courses, and
opencast symbols on the same layer. Later features now draw on top of
earlier ones. No overlap was seen on the grid cells checked. The real NZAT
face is lighter than the fallback face.
