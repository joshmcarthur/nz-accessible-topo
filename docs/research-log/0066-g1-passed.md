# 0066 — G1 passed; R-11 met

**Date:** 2026-11-05

## Question

Does a 0.5 mm `cross2` every 3 mm still read as a railway, an embankment, or a cliff where closed tracks are dense?

## What we did

Log 0065 set size 0.5 mm and interval 3 mm (every second gap of the `1;0.5` dash). Applied that style onto `squares/accessible/nztopo50.qgs`. Redrew the closed-track square and the 4 km accessible face.

Josh reviewed the G1 cells against stock:

- `1576000-5182000`
- `1580000-5170000`
- `1572000-5170000`
- `1584000-5158000`
- `1576000-5166000`

## What we found

G1 passed. The mark does not read as a railway, an embankment, or a cliff on those cells. R-11 "Met when" holds for closed tracks on this grid: red-light contrast was already ≥3:1 (log 0035), and the new symbol does not look like another legend symbol where tracks run close together.

B-30 is done. R-11 is met.

## What changed

- `BACKLOG.md`: B-30 Done; R-11 met; G1 dropped from the next-check list.
- `docs/recommendations.md`: R-11 met.
- This log.

## Confidence & gaps

The review is our own judgement (grade D). A steep sheet is not in this grid (OQ-09). The vector sprite is still a denser mark. G3, G4, G5, and G6 stay open.
