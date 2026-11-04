# 0072 — Natural names in index brown

**Date:** 2026-11-05

## Question

Does the log 0063 natural-name cue (italic maps to Bold) show on the grid?
If not, what cue can the accessible face draw?

## What we did

Compared `1568000-5158000`, `1572000-5170000`, and `1584000-5166000` with
stock. Read the carto_text `style` values and the FontStyle expression in
the applied project. Rendered a small test with FontStyle Regular plus a
data-defined Bold.

## What we found

G3 still failed. "Pukeiti Point" and "McQueens Valley" drew Regular black,
the same as "Port Levy".

- The patched face is one Regular file. QGIS finds no "Bold" style and
  draws Regular. A data-defined Bold did not make Qt embolden the face.
- The expression sent both Italic and Narrow to the natural style.
  Narrow upright is a settlement or area name (Port Levy, Gebbies Valley).

Style counts on carto_text: Narrow Italic 100,868, Regular 48,957,
Narrow 29,321, process_blue Italic 26,418, black Italic 7,685.

A real Bold file needs a new font download and a second patch. B-32 also
lists index brown as a cue. `#7A5542` is 6.55:1 on paper and 4.29:1 in red
light. Both pass `label_contrast` (4.8 and 3.0).

## What changed

- `labels.natural_colour` `#7A5542` in `tools/style-topo50.json`.
- Apply paints black italic carto_text in that ink. Water names keep blue.
- Only italic maps to `raster_natural_style`. Narrow maps to Regular.
- Spot heights are black italic in the data, so they also turn brown. That
  separates them from locality names of the same size (G4).
- Test in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-32.

## Confidence & gaps

Grade D (our review). Brown names read on the contour mesh because the
white halo separates them. G3 passes on the cells checked. The vector
style does not paint this ink yet. A Bold file is still an option.
G2 collisions are unchanged ("Crater Rim Walkway" under a wrapped name).
