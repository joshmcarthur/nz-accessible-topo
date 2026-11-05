# 0085 — Flat names drop stock alignment padding

**Date:** 2026-11-05

## Question

Why do several of the largest remaining collisions (G2) involve
multi-line names that look off-centre?

## What we did

Listed the largest new collisions after log 0084. Read the stored
`text_string` of those names. Evaluated a cleaning expression in QGIS 4.2.3
on five of them. Re-ran the fit and the collision count. Rendered the grid.

## What we found

Stock pads some names to align them on a curved baseline:
`"Te Moenga-o-Wheke /\n       The Tors"`, `"Richmond Hill\n      Farm"`,
`"\n \nMcCormacks\n Bay"`, `"South   New Brighton"`. The flat rule kept the
padding. Each line was wider than the text, the second line sat off to one
side, and the width estimate for the flat baseline was too long. The
one-line fit form also used the raw text.

## What changed

- `CARTO_CLEAN_TEXT` removes leading blanks, spaces after a line break,
  and runs of two or more spaces. `CARTO_FLAT_TEXT` and the one-line fit
  form use it. The fit tool collapses whitespace the same way.
- Test in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-31.

New collisions over 2000 m² fell from 111 to 105. "Livingstone Bay" and
"Te Rāpaki-o- / Te Rakiwhakaputa" now centre on their anchor.

## Confidence & gaps

Grade D. Baseline (curved) names keep their padding. Stock uses it there.
