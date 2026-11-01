# Styles

**Generated — do not hand-edit.** Built by `tools/build_style.py` from
`upstream/linz-topographic-v2.json`; CI fails if these drift from the build.

| File | What |
|---|---|
| `accessible-v0.json` | R-03 (NNW single light), R-04, R-05, R-07–R-11 applied |
| `accessible-v0-multidir.json` | as above, with multidirectional hillshade (R-03 full); needs MapLibre with style spec ≥ 23.2 |
| `sprites/nzat*.{png,json}` | patterns for R-10 (stipple) and R-11 (cross-bar), from `tools/make_sprites.py` |

What changed and why, line by line: `docs/styles/accessible-*-changes.md`.

These styles use LINZ's host-relative URLs (`/v1/...`) and need a LINZ
Basemaps API key. See `preview/README.md` to view them.

Derived from `linz/basemaps-config` (MIT, Crown copyright LINZ) — keep
`upstream/LICENSE-linz-basemaps-config` with any redistribution. Map data
© Toitū Te Whenua LINZ, CC BY 4.0.
