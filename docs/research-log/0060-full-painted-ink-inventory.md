# 0060 — Full painted-ink inventory on Map5View

**Date:** 2026-11-04

## Question

Which inks does the accessible project actually paint on the BX24 map face, and which of them fail R-01 that log 0048 did not list?

## What we did

Log 0048 read only the classes on the print must-distinguish list. This step read every visible layer.

Parsed `squares/accessible/nztopo50.qgs` in `~/Projects/github.com/linz/topo50-bx24`, the project that drew the 4 km grid. Took the layer ids in the `Map5View` visibility preset. For each enabled symbol layer, read `color`, `line_color` and `outline_color` with `parse_qgis_colour`. Folded symbol alpha and layer opacity onto white paper. Read rule and category labels for the vegetation, track, water, relief and landcover layers. Read the data-defined contour colour expression. Counted exact pixels of each ink on `render/bx24-4km/face-accessible.png`. Measured WCAG contrast against paper, and against painted fills where a line sits on them.

## What we found

Inks that draw on the BX24 face and that the pair file does not test:

| Layer / class | Ink | Contrast vs paper | On fills |
|---|---|---:|---|
| `water_line map` (streams, drains), coastline, water outlines | `#009EFF` | 2.86 | 1.81 on scrub, 2.44 on native, 2.24 on water fill |
| `vegetation_line map` shelter_belt | `#94FF3B` | 1.26 | 1.08 on native |
| `vegetation_point map` (green dots) | `#94FF3B` | 1.26 | — |
| `Grid_lines` | `#29A0D3` | 2.97 | — |
| `island` outline | `#0083BB` | 4.23 | — |
| `residential_area map` fill | `#BCBAB6` | 1.94 | black on it 10.84 |
| vegetation exotic fill | `#A4D65E` at 0.2 | 1.11 | — |
| vegetation outline | `#A7C05E` | 2.03 | — |

Inks the style owns, as painted (for reference): index contour `#7A5542` at 0.85 (data-defined), intermediate casing `#7A5542` at 0.5 (2.24), road fill `#EC7000` (3.05), highway `#E31A1C` (4.74), road casing `#232323` (15.72), contour-number FontMarker `#7A5542` (6.55), scrub `#A3CC90` at 0.78 (1.58) with hatch `#3F6B32` (6.25), native `#E1EAC3` at 0.71 (1.17). Tracks, railways, fences, relief lines and buildings are black or near-black.

Painted but not on the BX24 face (0 exact pixels): `#F000EC`, `#FF009F`, `#E748A2`, `#71E7D5`, `#A3D650`, `#4ACABD`, `#E15989`, `#FF0000`. These sit on ELSE or NULL rules, runways, or the DMS margin.

**Correction.** `docs/current-state/audit-topo50-print.md` passes watercourse against paper at 3.79:1. That number is the print legend ink. The project paints streams in `#009EFF` at 2.86:1. Thin anti-aliased stream pixels on the face are lighter still (`#42ABD8` 2.61, `#62B1DA` 2.38). The grid review first named `#29A0D3` as the stream ink. That is the grid-line ink.

The static `contour` line colour in the XML is `#FF7F00`. A data-defined expression replaces it, so a static read alone gives the wrong contour ink.

## What changed

- This log. The pair file is not changed. Adding line-on-fill pairs and the missing classes is backlog work (R-01, log 0058).

## Confidence & gaps

The parse reads static colours and the contour expression only. Other data-defined colours may hide behind static defaults. SVG markers may recolour inside the SVG. Exact-pixel counts miss thin anti-aliased lines, so a count of 0 does not prove an ink is absent on every sheet. One sheet only.
