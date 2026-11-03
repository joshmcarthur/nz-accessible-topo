# Styles

**Generated — do not hand-edit.** Built by `tools/build_style.py` from
`tools/style-topo50.json` onto the Shortbread catalog
`upstream/linz-topographic-v2.json`. CI fails if these drift from the build.

| File | What |
|---|---|
| `accessible-v0.json` | Vector form of the raster style. Owned paint from the style file. Unowned layers keep LINZ paint. |
| `accessible-v0-multidir.json` | as above, with multidirectional hillshade (R-03 full); needs MapLibre with style spec ≥ 23.2 |
| `sprites/nzat*.{png,json}` | patterns for R-10 (stipple) and R-11 (cross-bar), from `tools/make_sprites.py` |

What changed and why, line by line: `docs/styles/accessible-*-changes.md`.

These styles use LINZ's host-relative URLs (`/v1/...`) and need a LINZ
Basemaps API key. See `preview/README.md` to view them.

Catalog from `linz/basemaps-config` (MIT, Crown copyright LINZ) — keep
`upstream/LICENSE-linz-basemaps-config` with any redistribution. Map data
© Toitū Te Whenua LINZ, CC BY 4.0.
