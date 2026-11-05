# 0087 — The label fit keeps a gap between names

**Date:** 2026-11-05

## Question

Can a gap term in the carto label fit stop a moved name from abutting a
neighbour, so that two names do not read as one phrase?

## What we did

Added a gap band to the fit score. The band is the neighbour ink, grown
sideways and up and down. Each target ink pixel in the band costs
`GAP_WEIGHT` (3), the same as ink inside a halo. The move cost stays at
40 per mm. Tried three band sizes. Ran the fit, the collision count and
the grid render for each. Drew the fit's own masks for "Ōketeupoko" and
"North Hagley Park" to compare the model with the render.

## What we found

| Band (beside × above/below) | New >500 / >2000 / >5000 m² | Name pairs >2000 m² | New overlap m² |
|---|---|---|---|
| none (log 0086) | 194 / 98 / 38 | 72 | 785,898 |
| 0.4 × 0.4 mm | 196 / 94 / 39 | 68 | 747,599 |
| 1.0 × 0.4 mm | 185 / 96 / 41 | 69 | 788,478 |
| 0.72 × 0.4 mm | 184 / 93 / 40 | 66 | 746,767 |

The pair and area columns use one script for all four runs. It sums each
new name pair once. Its baseline reads 72 and 785,898, not the 69 and
756,717 in log 0086.

The 1.0 mm band put "Te Upoko-o-Kurī / Witch Hill" on one line across
"Te Ahi-a-Tamatea". That is worse in the render. The 0.72 mm band keeps
the two-line form.

With 0.72 × 0.4 mm:

- "Mt Evans"/"A57L" fell from 16,782 to 11,337 m². The render shows a gap.
- "Major Hornbrook Track"/"Mt Cavendish" fell from 29,632 m² to 0.
- "Taukahara"/"Te Poho-o-Tamatea" fell from 12,112 to 5,494 m².
- "Ōketeupoko"/"Tauhinukorokio / Mt Pleasant" fell from 23,095 to
  21,033 m². The gap grew from about 0.5 mm to 0.7 mm. The two names
  still share a baseline. They still read close. A road name above, "1126"
  below and "Mt Cavendish" boxed the name in. No free spot was near.
- "North Hagley Park" still touches "Victoria Lake". The fit model has
  about 1.2 mm between them. The render does not. The gap band cannot fix
  that mismatch.

## What changed

- `overlap_score.py`: new `gap_band` and an optional `near_gap` term.
- `best_candidate.py`: grows neighbour ink by 18 px (0.72 mm) beside and
  10 px (0.4 mm) above and below. Ink in that band adds to the score.
- Test in `tests/qgis/test_best_candidate.py`. It fails without the band.
- `docs/style-topo50.md`, B-31.

## Confidence & gaps

Grade C. The counts improve a little. The cells show clearer gaps at
Mt Evans and Mt Cavendish. Two of the three named pairs are not fixed.

- The fit model and the render differ at "North Hagley Park" and
  "Victoria Lake". Names the fit does not move are free in the final
  render. QGIS can place them again. That is the next lead.
- Names on one baseline need more than a word space. A wider band on the
  same baseline only, or a cost for sharing a baseline, may help
  "Ōketeupoko".
- New collisions over 5000 m² went from 38 to 40.
