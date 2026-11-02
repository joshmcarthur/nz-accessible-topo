# 0037 — Intermediate contour casing

**Date:** 2026-11-02

## Question

Can an intermediate contour meet 3:1 on paper and under red light without darkening `#C4814B`?

## What we did

`contours.intermediate.casing_colour` is `#8A4F1C`. `casing_width_mm` is 0.2. Those numbers live in `tools/style-topo50.json`. Index stays `#8A4F1C` at 0.28 mm. Intermediate fill stays `#C4814B` at 0.12 mm.

The QGIS apply step inserts a second SimpleLine under the fill. The casing is on when the line is not an index contour. The vector build inserts `NZAT-Contours-All-Casing` behind `Contours-All`. Casing width is the fill stops scaled by 0.2/0.12.

The four squares were drawn again at 600 dpi. The Port Hills square still shows brown contour lines. Index lines stay thicker. Intermediate lines stay thinner. The estuary word is `Estuary of`. The square has no black question marks.

## What we found

Intermediate casing versus paper is 6.53:1 grey and 3.45:1 red. That is the same pair as index versus paper. The fill is still `#C4814B`.

Intermediate fill versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate fill versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/style-topo50.json` holds the casing colour and the casing width.
- `tools/override_topo50_project.py` paints that casing under an intermediate contour.
- `tools/build_style.py` reads those numbers and adds the vector casing layer.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

The paper pair now meets 3:1 under red light. R-01 stays open until the Port Hills square is accepted as still reading as contours.
