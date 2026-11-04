# 0058 — Wider "Met when" tests for R-01, R-09 and R-11

**Date:** 2026-11-04

## Question

Which "Met when" tests let the grid regressions in log 0057 pass, and what must they also test?

## What we did

Read the "Met when" text of R-01, R-09 and R-11 against the grid findings G1, G2, G4 and G5. Read `tools/pairs-topo50-accessible.json`. Measured the index and intermediate contour inks as painted on the grid against the scrub fill.

## What we found

- **R-01 tests against paper only.** The pair file has 26 pairs. Two are fill against fill (native vs scrub, scrub vs water). None is a line or label on a fill. Painted index contour `#8E6E5E` on scrub `#B7D7A8` is 2.93:1. Painted intermediate `#B59888` on scrub is 1.7:1. Both pass against paper. (G5)
- **R-11 tests contrast only.** The cross-bar is 21:1 against paper. No test asks whether the symbol looks like another legend symbol. Log 0056 named the railway risk. Where closed tracks run close together on the Port Hills, the bars read as a railway, an embankment or a cliff. (G1)
- **R-09 had no "Met when".** It set floors and a 20 % step. Log 0028 says it did not decide which layers form one hierarchy. Spot heights were not given a rank. Nothing tested collisions or how far a name sits from its feature. Log 0052 says the fit tool ignores point symbols. (G2, G4)

## What changed

- R-01 "Met when": lines, glyphs and labels on a fill are measured against that fill.
- R-09 gains a rank for spot heights and a "Met when" with a placement test.
- R-11 "Met when": no symbol may read as another legend symbol on the full grid.
- The implementation status reopens R-01, R-09 and R-11.

## Confidence & gaps

The pair file does not yet hold line-on-fill pairs. That is backlog work. "Reads as another symbol" and "nearer its own feature" are judged on the grid (grade D) until user testing (R-16).
