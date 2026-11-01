# 0014 — Build `accessible-v0` from LINZ's style

**Date:** 2026-11-01

## Question
Can R-03 – R-11 be implemented as a reproducible transform of LINZ's own
style, rather than a hand-maintained fork?

## What we did
- Vendored `topographic-v2.json` and LINZ's MIT licence into `upstream/`.
- Wrote `tools/build_style.py`: each recommendation is a transform; every
  change is logged with its R-id → `docs/styles/accessible-*-changes.md`.
- Wrote `tools/make_sprites.py`: procedurally drawn stipple (R-10) and
  cross-bar (R-11) patterns, wired in as a MapLibre multi-sprite alongside
  LINZ's sprite.
- Two outputs: single NNW light, and multidirectional hillshade.
- Validated both against `@maplibre/maplibre-gl-style-spec` 26.5.0 (and
  confirmed the validator rejects a deliberately broken style).

## Design decisions
- **Label colours are derived, not hand-picked.** Each failing label is
  darkened along CIELAB L\* (hue and chroma kept) until it reaches 4.8:1 on
  its halo *and* 3:1 under the red-light model. One rule, applied uniformly,
  is easier to defend than 35 individual colour choices. Example: historic
  sites stay red but become `rgba(149,0,0)`, readable under a red headtorch.
- **Only map fonts onto glyph stacks LINZ already serves**, so the style
  works against LINZ's glyph endpoint without new fonts.
- **Letter-spacing (+0.05 em) is applied but marked provisional** (R-08).

## Correction to earlier logs
The audit counted two icon-only layers (`Poi-Showground-Symbol`,
`Waterway-Waterfall-Pt-Ln`, both with an empty `text-field`) as labels.
Corrected counts: **33 of 63** label layers italic (was 36/68); **26 of 63**
below 4.5:1, of which **24 are real** (was 28/68 and 26). Both tools now skip
empty `text-field` layers; current-state docs updated.

## Result
| Measure | LINZ topographic-v2 | accessible-v0 |
|---|---:|---:|
| Italic label layers | 33 / 63 | 0 |
| Labels < 4.5:1 (excl. shield false positives) | 24 | 0 |
| Hillshade light | 315° | 337.5° (± 292.5°/22.5° fill in multidir) |
| Index contour vs paper | 1.71–2.27:1 | 6.53:1 |
| Closed-track signal | 40% red shadow | dark casing + cross-bars |

## Confidence & gaps
- Valid and measurable, but **not yet seen rendered** — the sandbox can't
  reach LINZ tiles. Visual weight of darker contours (OQ-09) and the
  multidirectional colours (OQ-07) need eyes on real terrain.
- The glyph PBFs LINZ serves for Open Sans/Roboto haven't been checked for
  macrons (OQ-13).
