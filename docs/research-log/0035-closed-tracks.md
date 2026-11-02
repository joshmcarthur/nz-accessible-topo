# 0035 — Closed tracks and hazards in shape

**Date:** 2026-11-02

## Question

Do closed tracks and safety marks carry meaning in shape, and do they meet 3:1 under the red-light model?

## What we did

`tracks.closed_foot.casing_colour` is `#1A1A1A`. `tracks.closed_foot.casing_alpha` is 0.55. `label_contrast.red_light_min` is 3.0. Those numbers live in `tools/style-topo50.json`.

The vector build reads the casing colour. Closed-track shadow layers are `rgba(26, 26, 26, 0.55)`. The cross-bar sprite stays. The build does not keep `closed_track_shadow` in `P`.

The QGIS apply step does not paint that casing. Closed foot tracks keep the heavier line and the black cross-bars. Map labels use the same red-light floor as the vector build. Hue is kept. `warm_red` is `color_rgb(145,0,0)`. Historic labels are not switched to `rgba(73, 68, 68)`. No historic glyph was added.

The four squares were drawn again at 600 dpi. The closed-track square shows the heavier dashed line and the cross-bars. The stock square still uses gap length only. The estuary word is `Estuary of`. The square has no black question marks.

## What we found

Closed-track cross-bar versus paper is 21.00:1 under red light. Vector casing versus paper is 3.89:1. Historic label `rgb(145, 0, 0)` versus paper is 3.15:1. Hot spring versus paper is 18.42:1. All four meet the 3:1 red-light floor.

Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/style-topo50.json` holds the casing colour and the red-light floor.
- `tools/build_style.py` reads those numbers.
- `tools/override_topo50_project.py` darkens map labels that miss the red-light floor.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

R-11 is met for this list. The next step is R-17.
