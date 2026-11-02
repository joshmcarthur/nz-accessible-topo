# 0033 — Label contrast and halo

**Date:** 2026-11-02

## Question

Do the label colours meet the R-07 floor against an opaque halo?

## What we did

`label_contrast.min_ratio` is 4.8. `label_contrast.halo_alpha` is 1. Both numbers live in `tools/style-topo50.json`.

The vector build reads that floor. It still darkens a failing label along L*. It does not use `#005C8F`.

The QGIS apply step draws the buffer that is already on a map text style. It keeps the buffer size. It keeps the buffer colour. It sets the buffer alpha to 1. It darkens a label ink that is below 4.8:1 against that buffer.

`process_blue` becomes `color_rgb(0,111,202)`. That ink is 4.88:1 on the buffer `250,250,250`. The contour label `255,180,29` becomes `156,98,0`. That ink is 4.84:1 on the same buffer.

Layout text stays Nimbus. Layout buffers stay off. Legend `text-on-symbol` buffers stay off. Those three buffers are not map labels.

The four squares were drawn again at 600 dpi. The estuary word is `Estuary`. The letters are dark blue. The halo is white. The square has no black question marks. `StretchWordSpacingToFit` stays.

## What we found

The text-contrast table has 63 label layers. Two layers are below 4.5:1. Both are the documented highway shields. `All-Highway-Labels-three` is 1.00. `All-Highway-Labels-standard` is 1.00. No other layer is below 4.5:1.

The pair audit is unchanged. Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/style-topo50.json` holds the contrast floor and the halo alpha.
- `tools/build_style.py` reads that floor.
- `tools/override_topo50_project.py` draws the map label buffer and darkens the ink.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

R-07 is met for this list. The next step is R-10.
