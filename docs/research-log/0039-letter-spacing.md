# 0039 — Letter-spacing, one attempt

**Date:** 2026-11-02

## Question

Can modest letter-spacing go into the shared style file without changing along-line raster labels?

## What we did

Josh accepted the Port Hills contour step. R-01 is met. Casing versus paper is 3.45:1 under red light. Index is 0.45 mm.

`labels.letter_spacing_em` is 0.05. That number lives in `tools/style-topo50.json`. The vector build reads it. `P` no longer holds it. 79 vector label layers keep `text-letter-spacing` 0.05.

The QGIS apply step does not add that tracking. Along-line labels keep normal letter spacing. The four squares were not drawn again. The raster face did not change.

## What we found

R-08 Met when is an A/B test with dyslexic readers. This loop does not run that test. The evidence is still weak. R-08 stays provisional.

## What changed

- `tools/style-topo50.json` holds `letter_spacing_em`.
- `tools/build_style.py` reads that number.

## Confidence & gaps

This was the one R-08 attempt. Leave it provisional. The next step is R-12.
