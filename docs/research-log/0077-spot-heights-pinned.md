# 0077 — Spot heights stay by their dots

**Date:** 2026-11-05

## Question

Moved names touch spot heights (log 0074). Does the fit tool move the
heights themselves?

## What we did

Spot heights are carto_text placement 1 (229 Narrow Italic numbers on the
BX24 extent), so the flat rule includes them. Compared each fitted
position in `carto_fit.json` with the stock label position.

## What we found

The fit moved 25 spot heights. Five moved more than 2.5 mm: 462 (3.4 mm),
348 and 490 (3.1 mm), 10 and 445 (2.7 mm). A height that far from its dot
can read as the height of a different point. On `1572000-5170000` "462"
sat beside "Mt Vernon", away from its summit dot.

This is a usability regression from the 3 mm reach in log 0073.

## What changed

- `fit_carto_labels_main.py` skips spot heights (`nzat.qgis.is_spot_height`:
  a number with an optional m). They stay at the stock position and count
  as fixed boxes. Names move around them.
- Test `tests/qgis/test_is_spot_height.py`. B-31.

New collisions over 2000 m² rose from 114 to 125. Heights no longer dodge
names. On `1572000-5170000` "462" is back by its dot. "Witch Hill" still
touches "421".

## Confidence & gaps

Grade D. The pair count rose, but each height now marks the correct
point. A name next to a pinned height should get a larger move cost
toward it. G2 stays open.
