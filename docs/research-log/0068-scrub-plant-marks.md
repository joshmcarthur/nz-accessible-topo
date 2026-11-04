# 0068 — Scrub plant marks

**Date:** 2026-11-05

## Question

Do dark circles on pale scrub read as a vegetation class?

## What we did

Log 0067 replaced the 45° hatch with 0.5 mm `#3F6B32` circles at 2.5 mm. Josh found those dots made scrub hard to see.

Locked: keep pale fill alpha 26. Use the stock scattered plant mark `third_arc` at 1.2 mm, spacing 3 mm, in stock plant green `#B2DF8A`. Scattered stays at 5 mm with no fill.

## What we found

Dark circles on a near-white fill read as speckle, not as an area of scrub. The stock plant mark is the same language as scattered scrub. Denser spacing plus the pale fill is the class cue. Native versus scrub grey is still 1.11:1, so the pattern still carries R-10.

G5 stays open until the new cells are reviewed.

## What changed

- `tools/style-topo50.json`: `scrub_dots.marker` `third_arc`, size 1.2 mm, distance 3 mm, colour `#B2DF8A`.
- This log. B-34 stays on review.

## Confidence & gaps

Review G5 on `1568000-5166000`. A steep sheet is not in this grid.
