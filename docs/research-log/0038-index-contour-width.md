# 0038 — Heavier index contours

**Date:** 2026-11-02

## Question

After the intermediate casing, can index and intermediate contours still be told apart?

## What we did

The casing uses the same ink as the index. Index was 0.28 mm. Intermediate outer width was 0.2 mm. That step was 1.4×. Port Hills did not show a clear step.

`contours.index.width_mm` is now 0.45. That number is already the closed-foot-track width. Intermediate fill stays 0.12 mm. Intermediate casing stays 0.2 mm in `#8A4F1C`. Vector index width stops scale by 0.45/0.28.

The Port Hills square was drawn again at 600 dpi. Index lines are heavier. Intermediate lines stay thinner. The estuary word is `Estuary of`. The square has no black question marks.

## What we found

The outer-width step is 0.45 mm versus 0.2 mm, which is 2.25×. Pair contrast did not change. Casing versus paper is still 6.53:1 grey and 3.45:1 red.

## What changed

- `tools/style-topo50.json` holds index width 0.45 mm.
- Vector index width stops in `tools/build_style.py`.
- The four accessible square pictures in `docs/visuals/squares`.

## Confidence & gaps

R-01 stays open until the Port Hills square is accepted as showing a clear index versus intermediate step.
