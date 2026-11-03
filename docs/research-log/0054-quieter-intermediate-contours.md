# 0054 — Quieter intermediate contours

**Date:** 2026-11-03

## Question

Is intermediate alpha 0.65 still too heavy on the BX24 sheet?

## What we did

Lowered `contours.intermediate.alpha` from 0.65 to 0.5. Index stayed 0.85, because 0.75 fails 3:1 red vs paper. Hexes unchanged. Contour numbers stay opaque.

Intermediate casing vs paper is 2.23:1 grey and 1.89:1 red. That still sits above the 1.5 C6 floor. Index vs paper is still 4.60:1 grey and 3.28:1 red.

Drew the BX24 composite and the Port Hills square.

## What we found

Index cannot go lower without dropping the red-light paper floor. The 20 m mesh can.

## What changed

- `tools/style-topo50.json` intermediate alpha.
- Tests, pair docs, and the BX24 compare image.

## Confidence & gaps

Josh accepted this paint on the BX24 composite. Index 0.85 and intermediate 0.5 are settled for this sheet. A steeper Alpine sheet still answers OQ-09. Do not lower index unless the red 3:1 gate drops.
