# 0067 — Wider streams and scrub dots

**Date:** 2026-11-05

## Question

Do streams stay lost in the contour mesh after the L* darken, and does the 45° scrub hatch still read as vegetation?

## What we did

Josh reviewed G5 and G6 on the 4 km grid. Streams still sat at stock width 0.1 mm. The 45° hatch on pale scrub read as slope hachures.

Locked: keep stream `#0064BD`. Widen `water_line map` SimpleLines in that ink to 0.25 mm. Do not widen coastline. Swap the scrub line hatch for a circle-dot grid at 2.5 mm. Scattered scrub stays on stock `third_arc` at 5 mm. Pale fill alpha 26 stays so index-on-scrub still passes 3:1.

## What we found

Pair floors did not need a new hex. Width and pattern were the remaining levers. G5 and G6 stay open until the new cells are reviewed.

## What changed

- `tools/style-topo50.json`: `water.stream_width_mm` 0.25. `vegetation.scrub_dots` replaces `scrub_hatch`.
- Apply widens stream strokes on `water_line map` only. Apply paints scrub dots and removes a leftover hatch.
- This log. B-34 and B-35 stay on review.

## Confidence & gaps

A steep sheet is not in this grid. Anti-aliased stream pixels are still lighter than `#0064BD`. Review G5 on `1568000-5166000` and G6 on `1580000-5154000`.
