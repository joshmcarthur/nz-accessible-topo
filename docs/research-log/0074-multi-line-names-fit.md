# 0074 — Multi-line names join the fit

**Date:** 2026-11-05

## Question

Log 0073 found that 59 of 134 new collisions involve multi-line names that
the fit tool skips. Can the fit move them too?

## What we did

Placement 34 names store one joined 4-point baseline (two straight lines).
The flat rule needed `num_points <= 2`, so it never matched them. Changed
`CARTO_POINT_FILTER` to take placement 34 at any point count, and placement
1 on a straight baseline. Ran the fit from a clean apply and counted
collisions with `tools/count_label_collisions.py`. Rendered the grid.

## What we found

The first render re-wrapped names that already had a break: "Te Rāpaki-o- /
Te / Rakiwhakaputa" and a lone "/" in "Te Heru-o-Kahukura / Sugarloaf".
The 16-character wrap now skips a name with its own break.

| New collisions over stock | Log 0073 | This log |
|---|---|---|
| > 500 m² | 307 | 220 |
| > 2000 m² | 134 | 116 |
| > 5000 m² | 26 | 44 |

The > 5000 m² count rose. The label shape of a fitted name is larger than
its drawn text (log 0073), so that count is not reliable. On the render:

- "Crater Rim Walkway" is clear of "Te Whakatakanga-o-te-ngārehu-o-
  te-ahi-a-Tamatea".
- "Te Upoko-o-Kurī / Witch Hill" no longer sits on "Te Ahi-a-Tamatea". It
  now touches spot height "421".
- "Te Rāpaki-o-Te Rakiwhakaputa" sits over the settlement, as on stock.
- "The Tors" touches spot height "422".

A move cost of 400 per mm, not 40, did not change the counts. It stays 40.

## What changed

- `CARTO_POINT_FILTER` includes placement 34.
- `carto_flat_wrap_expression` skips names that contain a line break.
- Tests in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-31.

## Confidence & gaps

Grade D. Spot heights still collide with moved names. G2 still fails. Most
remaining collisions are along-line road names at junctions.
