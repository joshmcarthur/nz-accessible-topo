# 0084 — Spot heights keep their 6 pt rank

**Date:** 2026-11-05

## Question

Why do spot heights ("258", "204") look as large as place names on
`1580000-5170000` (G4)?

## What we did

Counted carto_text sizes on the BX24 extent. Read `size_floor` and the
carto_text Size expression.

## What we found

All 232 spot heights are carto_text at 6 pt. Names are mostly 5.5 to 6 pt
and lift to the 7 pt floor. `labels.spot_height_floor_pt` (6 pt) only
applied to layers named `relief_point`. So carto_text heights also lifted
to 7 pt, the same size as the names around them. Stock draws heights one
step under names.

## What changed

- The carto_text Size expression keeps text that is a number with an
  optional m at `spot_height_floor_pt`. Other text keeps the 7 pt floor.
- Test in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-33, B-31.

New collisions over 2000 m² fell from 125 to 111.

## Confidence & gaps

Grade D. 6 pt is the R-09 floor for heights. Black, digits, and 6 pt now
rank heights under names, as in stock.
