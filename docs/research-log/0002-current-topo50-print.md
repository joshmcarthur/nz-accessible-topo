# 0002 — How the printed Topo50 currently works

**Date:** 2026-11-01

## Question
What are the baseline conventions of the printed Topo50 series that any
redesign is departing from?

## What we did
- Read LINZ's *Topo50 Map Reading Guide* in full.
- Read the LINZ data dictionary entry for `contour`.
- Searched for published critiques of Topo50 symbology; found and read Pete
  McDonald's 2020 paper supporting a petition to redesign track symbols.

## What we found
- 20 m contours, NW-lit relief shading, blue/black/green colour convention,
  blue 1 km grid (S-LINZ-GUIDE, S-LINZ-DD-CONTOUR).
- Track symbology all black, inherited from 1977; no public/private access
  distinction (S-MCDONALD-2020).
- The data dictionary includes "representation specification" images per
  class — these are images, not machine-readable values, so exact print
  colours are **not yet captured**.

## What changed
- Added `docs/current-state/topo50-print.md`
- Started `docs/sources.md`

## Confidence & gaps
- Medium. LINZ's guide is authoritative but high-level. Need a physical
  legend (or the print-ready TIFF legend from topomap.co.nz) to record exact
  colours, line weights and typefaces. Logged as a gap.
