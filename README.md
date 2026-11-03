# nz-accessible-topo

Research and (eventually) open-source styles for New Zealand topographic map
layers — print and web — that are easier to read for more people.

**Target:** LINZ Basemaps' `topo-raster-gridded` layer — Topo50 itself. Because
that layer is pre-rendered imagery, the primary deliverable is a fork of LINZ's
MIT-licensed Topo50 QGIS symbology (`linz/topographic-qgis`), re-rendered with
LINZ's own production pipeline, giving accessible raster tiles **and** print
(R-18, log 0023). A secondary web-vector track (`styles/accessible-v0*.json`,
from `topographic-v2`) is kept and gated. The data never changes — only how
it's drawn.

## Goals

1. Readable by people with colour vision deficiency (CVD) without relying on a
   legend lookup for safety-critical distinctions.
2. Typography informed by legibility research, including research on dyslexia
   and low vision, and correct rendering of te reo Māori place names (macrons).
3. Terrain depiction (contours + relief shading) that minimises known
   perceptual illusions.
4. Works in the field: in rain, under a headtorch, folded in a map case, read by
   someone tired, cold, older, or stressed.
5. Traceable: every recommendation links to the findings and sources it came
   from, so it can be challenged and improved.

## Handoff

New here or picking this up locally? Start with [HANDOFF.md](HANDOFF.md) and [BACKLOG.md](BACKLOG.md).

## Where to start reading

- [`docs/README.md`](docs/README.md) — index of the research
- [`docs/research-log/`](docs/research-log/) — chronological log; one entry per
  commit, explaining what was investigated and why
- [`docs/recommendations.md`](docs/recommendations.md) — the current set of
  recommendations, each traced to evidence
- [`docs/sources.md`](docs/sources.md) — bibliography with evidence grades

## Status

- Research: findings F-01–F-25, recommendations R-01–R-16 (`docs/`).
- **Styles:** `styles/accessible-v0.json` and `-multidir.json`, generated from
  LINZ's `topographic-v2` by `tools/build_style.py` (R-03–R-11 applied).
- **CI:** `tools/check.py` gates (no italics, label contrast, NNW light,
  macron-safe fonts, CVD/greyscale/red-light pair floors) + MapLibre validation.
- **Preview:** `preview/` — side-by-side with CVD / greyscale / red-light simulation.
- **Site:** `site/` — Astro site with the evidence Sankey and vision comparisons (see `site/README.md`).
- Not yet: print output, user testing, live-tile visual check.

## Quick start

```sh
uv sync
uv run python tools/build_style.py   # regenerate styles/ from upstream/
uv run python tools/check.py         # accessibility gates
uv run pytest                        # package tests
python3 -m http.server 8000          # then open http://localhost:8000/preview/
```

## Tools

- `tools/build_style.py` — upstream LINZ style → accessible styles, with a per-change log
- `tools/check.py` — CI gates C1–C6
- `tools/palette_audit.py` — WCAG contrast + CVD / greyscale / red-light separability
- `tools/font_check.py` — macron coverage and x-height for candidate fonts
- `tools/make_sprites.py` — stipple and cross-bar patterns

## Licensing (to be decided by the maintainer)

Not yet chosen. Notes for that decision:
- LINZ data and basemaps are published under CC BY 4.0 and require attribution.
- LINZ's `basemaps-config` repo (which contains the `topographic-v2` style
  this project audits) is MIT-licensed, Crown copyright LINZ — so a derived
  style is permissible with the licence notice retained.
