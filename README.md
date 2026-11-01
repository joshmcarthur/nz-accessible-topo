# nz-accessible-topo

Research and (eventually) open-source styles for New Zealand topographic map
layers — print and web — that are easier to read for more people.

The underlying data is LINZ's published topographic data (Topo50 / NZ Topo
Data Model, and the LINZ Basemaps `topographic-v2` vector tiles). This project
does **not** change the data. It changes *how the data is drawn*.

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

## Where to start reading

- [`docs/README.md`](docs/README.md) — index of the research
- [`docs/research-log/`](docs/research-log/) — chronological log; one entry per
  commit, explaining what was investigated and why
- [`docs/recommendations.md`](docs/recommendations.md) — the current set of
  recommendations, each traced to evidence
- [`docs/sources.md`](docs/sources.md) — bibliography with evidence grades

## Status

Research phase. No styles yet.

## Licensing (to be decided by the maintainer)

Not yet chosen. Notes for that decision:
- LINZ data and basemaps are published under CC BY 4.0 and require attribution.
- LINZ's `basemaps-config` repo (which contains the `topographic-v2` style
  this project audits) is MIT-licensed, Crown copyright LINZ — so a derived
  style is permissible with the licence notice retained.
