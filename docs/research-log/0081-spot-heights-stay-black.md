# 0081 — Spot heights stay black

**Date:** 2026-11-05

## Question

The Topo50 pair audit lists 18 failing pairs. Which of them hide map
information on the grid?

## What we did

Ran `palette_audit.py` with `tools/pairs-topo50-accessible.json`. Most
fails are known trade-offs: road and highway hue in red light (the dark
casing carries them), spring glyph shape (R-17), and the receding
intermediate mesh (R-04). Checked two on the grid: intermediate contour on
urban fill (1.15:1 grey) on `1576000-5174000`, and spot heights near
contour numbers on `1580000-5162000`.

## What we found

- Neither face draws contours under urban fill. The urban pair does not
  occur on paper. No change.
- Log 0072 painted every black italic label in index brown, including
  spot heights. Contour-number FontMarkers already use index brown and
  upright Regular (R-04, R-05). So "349" (a spot height) and "300" (a
  contour value) had the same ink, face, and weight. Only rotation told
  them apart. In stock they differ in colour: black heights, orange
  contour values.

This is a usability regression from log 0072.

## What changed

- The natural-ink rule skips text that is a number with an optional m.
  Spot heights stay black. Natural-feature names stay brown.
- Test in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-32.

## Confidence & gaps

Grade D. G4 (spot heights close to locality size) is open again. The
spot-height floor is 6 pt and locality is 7 pt or more, and digits do not
read as words.
