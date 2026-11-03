# 0055 — Thinner index contours

**Date:** 2026-11-03

## Question

Can the index line be finer than 0.45 mm without losing the step against the 0.2 mm intermediate casing, and without changing colour contrast?

## What we did

Set `contours.index.width_mm` to 0.35. Intermediate casing stays 0.2 mm. Fill stays 0.12 mm. Alphas stay 0.85 / 0.5. Hexes unchanged.

The vector index width stops scale from the 0.45 mm calibration by 0.35/0.45. Pair contrast does not change. The outer-width step is 1.75× (was 2.25×). That is still above the 1.4× step that failed on Port Hills at 0.28 mm vs 0.2 mm (log 0038).

Drew the BX24 composite and the Port Hills square.

## What we found

Colour floors do not depend on millimetres. 0.28 mm is still too close to the casing. 0.35 mm is the first step down from 0.45 mm that keeps a clear index.

## What changed

- `tools/style-topo50.json` index width.
- Vector index width reads that millimetre.
- The BX24 compare image.

## Confidence & gaps

Josh accepted 0.35 mm index on BX24, with intermediate unchanged. Index vs paper is still 4.60:1 grey and 3.28:1 red. Contour numbers stay opaque at 6.55:1 grey and 4.29:1 red. ΔE vs road and highway stays ≥10. Intermediate vs paper stays below 3:1, which was already allowed. C1–C6 pass. Do not return to 0.28 mm while the casing is 0.2 mm.
