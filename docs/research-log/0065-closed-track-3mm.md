# 0065 — Closed-track × every 3 mm

**Date:** 2026-11-05

## Question

Is 4.5 mm too sparse for a 0.5 mm closed-track ×?

## What we did

Log 0064 set size 0.5 mm and interval 4.5 mm (every third gap of the `1;0.5` dash). Josh asked to tighten the interval to 3 mm.

`tracks.closed_foot.marker_interval_mm` is now 3. That is every second dash cycle. Size stays 0.5 mm. The first mark still sits in a gap (offset 1.25 mm). Dash and line weight stay the same as an open foot track.

Applied the style onto `squares/accessible/nztopo50.qgs`. Redrew the closed-track square and the 4 km accessible face.

## What we found

4.5 mm left too much unmarked dash on the sparse square and on Evans Pass. 3 mm sits between every-gap (1.5 mm) and every-third-gap (4.5 mm).

G1 stays open until the new cells are reviewed.

## What changed

- `tools/style-topo50.json`: `marker_interval_mm` 3.
- This log. B-30 stays on review.

## Confidence & gaps

A steep sheet is not in this grid. Review G1 on `1580000-5170000` and `1572000-5170000`.
