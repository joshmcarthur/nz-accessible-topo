# 0020 — Revisions from real-map evidence, and real-scenario tooling

**Date:** 2026-11-01

## Question
What should change now that we've seen real Topo50 output, and how do we
test the new style on realistic scenes rather than synthetic ones?

## Revisions
- **R-04 intermediate contours** `#A8703C` → `#C4814B`, width
  0.8–1.2 → 0.6–0.9 px. Method: lighten the index contour's CIELAB L\* until
  the colour is just above 3.2:1 on white. Rationale: on the real Kawarau
  render, 20 m intermediates on steep slopes are dense even in pale orange;
  darkening them all (v0) would turn slopes into dark masses (OQ-09).
  Trade-off accepted and recorded: intermediates drop to 1.75:1 under red
  light; index contours (3.45:1) carry relief there. Gate floors updated.
- **R-11** now cites print evidence (P2).
- **R-17 (new)**: print-specific fixes from the legend audit.

## Real-scenario tooling
- `tools/screenshots/scenarios.json`: seven real NZ locations, each chosen
  to stress specific findings (dense alpine relief, geothermal springs,
  flat plains, forest/scrub boundaries, macron-heavy towns, and the same
  Kawarau area as LINZ's real render, for a direct print-vs-web check).
- `tools/screenshots/compare.mjs`: Playwright script that drives
  `preview/` with a LINZ API key and captures LINZ vs accessible side by
  side under all six conditions.
- `preview/index.html` now accepts `?key=&variant=&sim=`, aligns the right
  map to the URL location, and exposes an idle counter for the script.

## Why not done here
The build sandbox can't reach LINZ's tile servers or topomap.co.nz. The
script is syntax-checked but **not yet run**.

## Next
Run the script; commit the useful screenshots under `docs/visuals/real/`
with a log entry; re-tune R-04 and R-03 against them.
