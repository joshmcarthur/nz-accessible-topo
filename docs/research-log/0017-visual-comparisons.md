# 0017 — Visual comparisons

**Date:** 2026-11-01

## Question
What do the measured differences between LINZ `topographic-v2` and
`accessible-v0` look like — under normal vision and the five simulations?

## What we did
- `tools/render_comparison.py`: one synthetic terrain scene (ridge, summit,
  spurs, lake basin, stream, highway, pipeline, open and closed tracks, scrub
  and scattered scrub, labels with macrons), drawn twice with every visual
  property read from each style JSON at z14. Same simulations as the audit
  tool (Machado 2009 in linear RGB, greyscale, red-light).
- `tools/render_fonts.py`: specimens of Open Sans, Atkinson Next, and a
  patched build.

## Bugs found and fixed while doing this (recorded because they'd have produced wrong pictures)
1. **Hillshade was inverted.** The first formula lit slopes from the opposite
   side, so the panel labelled "315° NW" was actually lit from the SE. Caught
   by testing a single hill. Replaced with an explicit normal·light-vector
   calculation and added `tools/test_tools.py::test_hillshade_direction`
   (N, E and NW all verified).
2. **Wrong font weight.** Open Sans's variable axes are ordered
   `[Weight, Width]`; I'd passed them reversed, rendering everything Light.
3. **Halo over text.** Drawing text over its halo in a single Pillow layer
   blended edges wrongly; halo and text are now separate layers.

## What we found
See observations in `docs/visuals/README.md`. Headline: greyscale and
red-light are where LINZ's style fails visibly; v0 survives all six
conditions. Also a new cost: v0's darker contours make steep terrain busy
(OQ-09 is now a priority, not a hypothetical).

## Confidence & gaps
- Synthetic scene + non-MapLibre renderer. Real-tile screenshots via
  `preview/` remain the next step.
