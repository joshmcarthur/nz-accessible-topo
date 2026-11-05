# 0075 — Road suffixes abbreviate when a name overruns

**Date:** 2026-11-05

## Question

After log 0074, 56 of 116 new label collisions involve road names. The
fit tool cannot move along-line names. Can a shorter text reduce them?

## What we did

Counted road suffixes in carto_text on the BX24 extent: 121 names end in a
full word (ROAD, STREET, AVENUE, DRIVE) and 58 already use the short form
(RD, ST, AVE, DR). Topo50 abbreviates where a name is tight.

The Baseline label rule now draws an expression. When the estimated width
of the name (the `carto_point.advance_em` estimate at the floored size) is
longer than its baseline, a final ROAD, STREET, AVENUE, DRIVE, TERRACE,
CRESCENT, or PLACE becomes RD, ST, AVE, DR, TCE, CRES, or PL. Otherwise
the text is unchanged. Re-ran the fit and `count_label_collisions.py`.

## What we found

- 120 more drawn labels end in a short form (596 to 716). No name is lost.
- New collisions over 2000 m² fell from 116 to 114. The count is low
  because the pair key is the text, so an abbreviated name no longer
  matches its stock pair.
- On `1576000-5166000` "PURAU AVENUE" is now "PURAU AVE" and stays on its
  baseline instead of running into the bend.
- Many Topo50 road names are split into word labels ("MARINE" and
  "DRIVE"). A lone suffix label does not match, so "MARINE DRIVE" and
  "BAYVIEW RD" still collide.

## What changed

- `labels.road_abbreviations` in `tools/style-topo50.json`.
- `nzat.qgis.carto_abbreviation_expression`; the Baseline rule draws it.
- Test in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-31.

## Confidence & gaps

Grade D. The width estimate is coarse. Split names need a separate fix,
such as abbreviating a lone suffix label whose baseline is shorter than
the word.
