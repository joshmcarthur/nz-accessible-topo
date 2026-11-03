# 0052 — Carto text fit and stock spread

**Date:** 2026-11-03

## Question

Can the accessible sheet place dense flat names with the least overlap, and keep the stock word spread on names that have room?

## What we did

`tools/fit_carto_labels.py` renders the BX24 face with QGIS and finds flat names whose label boxes collide. It tries each name on one line and in its wrapped form, moved in 0.25 mm steps up to 1.5 mm sideways. It scores glyph ink and halo: ink on ink 10, ink in a halo 3, halo on halo 1, plus 40 per mm moved. It writes `carto_fit.json` beside the project. The apply step reads that file (log 0042).

Stock draws most `nztopo50_carto_text` rows with `StretchWordSpacingToFit` or `StretchCharacterSpacingToFit`. QGIS spreads the words or letters to fill the baseline. The apply step had set every stretch mode to default, because stretch squeezed the larger type onto a short line. Now a one-line name keeps its stretch mode when its baseline is longer than the estimated text width (characters × size × 0.6 em). Other rows use default spacing.

The flat rule took any one-line row with `text_placement = 1` and `text_orientation = 0`. That included area names on a long curved baseline, such as `Banks Peninsula` (3.6 km, 30 points). The flat filter now also needs `num_points($geometry) <= 2`. Twenty rows with `text_bend > 0` have a straight 2-point line, so the filter tests points, not the bend.

## What we found

- The fit tool finds 142 colliding flat names and fits 97. Most fits are small moves.
- `Ōmawete / Coopers Knob` goes to one line between `Rhodes Spring` and `A579`, with no ink overlap.
- `Te Upoko-o-Kurī / Witch Hill` goes to one line below `Te Ahi-a-Tamatea`. With halo weight 1 and no halo-on-halo term, the two halos touched. At the weights above, `Te Ahi-a-Tamatea` moves up 0.25 mm and the ink gap is about 0.55 mm.
- A step grid without 0 moved every name, including names with no overlap.
- Glyph masks from `QgsTextRenderer` are about 2.5 % smaller than the QGIS label boxes in both directions. The cause is not known.
- 151 one-line stretch rows on the curved rule have room and now spread, mostly road names (`FERRY ROAD`, `LINWOOD AVENUE`, `MAIN SOUTH LINE`). 154 rows have no room and keep default spacing.
- 30 curved one-line rows leave the flat rule. `Banks Peninsula` spreads across the peninsula as on the stock sheet.
- `Te Ara Pātaka Walkway` does not spread. At the 7 pt floor its estimated width is about 1.7 km. Its stock line is 1.4 km at 5.5 pt.

## What changed

- `tools/fit_carto_labels.py`, with a scoring test in `tools/test_tools.py`.
- `tools/override_topo50_project.py`: `curved_label_mode_expression`, `carto_text_width_expression`, and `CARTO_POINT_FILTER`.
- `docs/style-topo50.md`: the `charplace` rule.

## Confidence & gaps

The fit counts other labels as filled boxes. Point symbols are not counted. The width estimate is 0.6 em per character, so a line just longer than the estimate can still squeeze a name a little. A name whose line is shorter than the larger type cannot spread without a longer baseline. Flat straight names with a stretch mode, such as `Waipuna Saddle`, stay compact so the fit tool can move them.
