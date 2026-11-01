# 0019 — Real Topo50 print: legend audit and real-map simulations

**Date:** 2026-11-01

## Question
The synthetic scene (log 0017) isn't a realistic scenario. Can we test
against real Topo50 output?

## What we tried
- **topomap.co.nz tiles:** not reachable. The sandbox's network allowlist
  can't resolve the host; the web fetcher can read its HTML but won't fetch
  image or tile URLs embedded in pages. The site does offer an MBTiles
  download and a legend, both blocked for the same reason.
- **LINZ `topographic-system` on GitHub (reachable):** this is the repo that
  produces NZTopo50. It contains (a) `topo50_landing.webp`, a real Topo50
  render of the Kawarau River near Gibbston, and (b)
  `e2e/assets/topo-legend-1.tif`, the full Topo50 legend at high
  resolution (WEBP-compressed TIFF; decoded with `tifffile` + `imagecodecs`).
  Repo @ `f253c35`, MIT licence, Crown copyright.

## What we did
- Sampled the modal ink colour of each legend swatch; measured dash/gap
  lengths of the track symbols by run-length along each symbol row.
- Audited the print palette with `palette_audit.py`
  (`tools/pairs-topo50-print.json`).
- Added `tools/simulate_image.py` and ran all six conditions over the real
  Kawarau render (`docs/visuals/07-real-topo50-simulations.png`).

## What we found
P1–P9 in `current-state/topo50-print.md`. Most important:
- **P2:** closed (impassable) tracks differ from foot tracks only by gap
  length (12 → 24 px). No colour, no weight, no glyph. This is the strongest
  single argument for R-11 — in print, not just on the web.
- **P1:** contours and road fills share one ink.
- **P5/P6:** native forest vs scrub is tint-only; but print *does* pattern
  scattered scrub — R-10 restores something the web style lost.
- **P3/P7:** hot vs cold spring fails greyscale; red-orange symbols and
  contours vanish under red light.

## What the real-map simulations add
- Deutan/protan: the highway's red-orange collapses towards contour colour;
  green river flats go khaki. Width and casing still carry roads.
- Greyscale: vegetation nearly disappears; contours fade.
- Red light: water goes dark and strong; contours become faint texture;
  contour labels nearly vanish.
- **Density:** real 20 m contours on steep slopes are already dense in pale
  orange. Darkening *all* intermediates (v0) would be too heavy — revises R-04
  (see log 0020).

## Confidence & gaps
- Colours are from a render, not CMYK print specs; paper, ink and
  overprinting will shift them. Still the best evidence available here.
- One real scene. More realistic scenarios need live tiles — see log 0020.
