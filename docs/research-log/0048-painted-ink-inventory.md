# 0048 — Painted-ink inventory against the recommendations

**Date:** 2026-11-03

## Question

Does the accessible style still paint original Topo50 inks that fail R-01, R-04, R-11, or R-17? The style loop judged contours against gold `#D5B43C`. The squares look orange.

## What we did

Walked Map5View in `~/Projects/github.com/linz/topo50-bx24/accessible/nztopo50.qgs` with `parse_qgis_colour`. Read SimpleLine `line_color` on the layers the square draws. Confirmed against modal pixels on the four 600 dpi squares.

Rebuilt `tools/pairs-topo50-accessible.json` from the print must-distinguish list using those painted inks. Ran `palette_audit.py` against `tools/style-topo50.json`.

The apply step was not changed. No square was redrawn.

## What we found

Gold `#D5B43C` is not the road fill. It is the bivouac SVG colour. Road-layer XML also stores that gold as a legend `color`. The line that Map5View paints is PMS151.

Map5View painted inks that matter:

| Class | Painted ink | Cue besides hue |
|---|---|---|
| Two-lane / sealed / metalled road fill | `#FF7F00` | Dark casing `#232323` |
| Highway fill | `#E31A1C` | Dark casing `#232323` |
| Index contour | `#8A4F1C` (data-defined) | Heavier width 0.45 mm |
| Intermediate contour fill | `#C4814B` (data-defined) | Casing `#8A4F1C` 0.2 mm |
| Water fill | `#D1E7F5` | Process-blue shoreline |
| Buildings, tracks, fences | `#000000` / `#232323` | Shape |
| Native forest / scrub | owned greens | Scrub hatch |
| Contour number marker | `#FF7F00` FontMarker | — |
| Pipeline | not in Map5View | — |
| `water_point` springs | owned glyphs, layer not in Map5View | — |

Print highway `#EA6300` is still not a Map5View ink.

### Gap table

A pair is a gap when R-01 fails and there is no shape, or R-04 ΔE is below 10 under any dichromacy, or R-17 still uses red-orange alone.

| Pair | Result | Gap? |
|---|---|---|
| Intermediate contour vs project road `#FF7F00` | protan ΔE 9.1, tritan ΔE 7.6 | **Yes — R-04** |
| Index contour vs project highway `#E31A1C` | protan ΔE 0.9 | **Yes — R-04** |
| Intermediate contour vs project highway `#E31A1C` | deutan ΔE 8.8 | **Yes — R-04** |
| Intermediate contour vs print highway `#EA6300` | protan ΔE 8.3, deutan ΔE 7.5 | No — not painted |
| Project road vs paper | red-light 1.00 | No — casing `#232323` is 15.72:1 |
| Project highway vs paper | red-light 1.28 | No — same casing |
| Native forest vs scrub | grey 1.45 | No — hatch |
| Scrub vs water | grey 1.42 | No — shoreline |
| Hot vs cold spring | red-light 1.14 | No — glyphs differ |
| Index / intermediate vs paper | grey 6.53, red 3.45 | No |
| Closed-track and historic vs paper | pass | No |

R-04 is open against the inks the map paints. The gold settlement was a measurement error.

R-17 P7 does not reopen for roads: the fill is orange or red, but the casing is dark and meets 3:1 under red light.

No pipeline class is on Map5View, so W6 is not a painted pair.

## What changed

- `tools/style-topo50.json` `reference_inks.project_road` is `#FF7F00`. It also names `project_highway` `#E31A1C`, `project_road_casing` `#232323`, and `water_fill` `#D1E7F5`.
- `tools/pairs-topo50-accessible.json` judges those painted inks.
- This log.

## Confidence & gaps

One accessible `.qgs` and four BX24 squares. A steep sheet is still OQ-09. Contour-number markers still use `#FF7F00`; that is not a current pair. Next is the gap table, then one owned class if that table is accepted.
