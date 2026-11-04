# 0057 — A full-grid stock review gates "met"

**Date:** 2026-11-04

## Question

Why did the 4 km BX24 grid show regressions that no gate caught, and what must change in the method?

## What we did

Compared all 27 stock and accessible cells in `render/bx24-4km/` (log 0025 face, `tools/crop_grid.py`). Built side-by-side pairs and zoomed crops. Read `docs/method.md`, the "Met when" text in `docs/recommendations.md`, the style-loop prompt, and logs 0048, 0052 and 0056.

## What we found

Regressions that the change causes (cells by south-west corner):

| ID | Regression | Cells |
|---|---|---|
| G1 | Closed-track bars read as a railway, an embankment or a cliff where tracks are dense | 1576000-5182000, 1580000-5170000, 1572000-5170000, 1584000-5158000, 1576000-5166000 |
| G2 | Names collide or move away from their feature (Evans Pass and Godley Head, Te Ahi-a-Tamatea and Te Upoko-o-Kurī, Diamond Harbour and Pauaohinekotau Head) | 1580000-5170000, 1572000-5170000, 1576000-5166000 |
| G3 | Natural-feature names (valleys, heads, saddles, peaks) look the same as settlement names | 1568000-5158000, 1580000-5162000 |
| G4 | Spot heights are close to locality size. Urban halos cut white holes in the street grid | 1564000-5170000, 1568000-5182000, 1564000-5178000 |
| G5 | Scrub fill and hatch darken large areas. Index contour over scrub is 2.93:1 | 1568000-5166000, 1564000-5170000, 1564000-5162000 |
| G6 | The cased intermediate mesh makes thin streams harder to find on steep slopes | 1580000-5154000, 1584000-5166000 |

Each of these changes passed its own "Met when" threshold. Two method gaps explain why:

1. Every "Met when" is a fixed threshold. `method.md` had no step that compares the result with the stock sheet.
2. The style loop judged each recommendation on one 1 km square chosen for it. The closed-track square has one sparse track. Dense labels, dense closed tracks and large scrub areas were not in any square.

## What changed

- `docs/method.md` has a "When a recommendation is met" section. A full-grid stock review is now the second condition.
- Lore `refs/lore/topo50-qgis-render` records the decision.

## Confidence & gaps

The review is our own visual judgement (grade D). It covers one flat-to-hilly sheet. A steep sheet is still OQ-09. The next logs record the other gaps: tests against fills, symbol confusion, label placement, the italic class cue, and the ink inventory.
