# 0086 — Straight letter-spaced names join the fit

**Date:** 2026-11-05

## Question

Why does trig code "A56Y" touch its height "298m" in cell
1576000-5174000, so that the pair reads "298mA56Y"?

## What we did

Compared stock and accessible crops of the trig at Richmond Hill. Read the
stock carto_text rows near each trig code. Listed the placement 1 names with
orientation 0 and more than two points. Changed the flat filter. Re-ran the
fit, the collision count and the grid render.

## What we found

In stock, "298m" ends 26 m (0.5 mm) left of "A56Y" on the same baseline.
The accessible face is wider, so the gap closed.

The fit did not move "A56Y". Stock stores that baseline as eight points, one
segment per letter. The flat filter only took placement 1 lines with two
points or less. The name stayed on the baseline rule at its stock centre.

30 names in BX24 have this shape. Each baseline is level. Examples are
"A56Y", "A57L", "Ōketeupoko", "North New Brighton", "Packhorse Hut" and
"Pegasus Bay". The baseline rule already drops the stock stretch when the
baseline is shorter than the estimated width. Those names gain nothing from
the baseline rule.

## What changed

- `CARTO_POINT_FILTER` also takes a placement 1 name when its baseline is
  level (`bounds_height` under 1 m) and no longer than the estimated text
  width. Names with a longer level baseline, such as Pegasus Bay and Banks
  Peninsula, keep their stock spread.
- `carto_text_width_expression` imports its defaults late, so
  `defaults.py` can build the filter with it.
- Test in `tests/qgis/test_labels.py`. `docs/style-topo50.md`, B-31.

New collisions over 2000 m² fell from 105 to 98. Over 500 m² fell from 217
to 194. Over 5000 m² went from 37 to 38. The old count split a letter-spaced
name into one label per segment. Summed per name pair, new collisions over
2000 m² fell from 76 to 69. The new overlap area fell from 776,616 m² to
756,717 m².

"298m A56Y" now has a word gap. "102m"/"A57A", "315m"/"A580",
"445"/"Ōketeupoko", "BOWER AVENUE"/"North New Brighton" and
"IRWELL ST"/"Springvale" no longer collide. "Cooptown" moved clear of the
highway. "North New Brighton" now wraps onto two lines.

## Confidence & gaps

Grade D. Two pairs got worse. "Ōketeupoko" moved right and now abuts
"Mt Pleasant" (3,025 to 23,095 m²). It reads as one phrase. "North Hagley
Park" moved onto one line above "Victoria Lake" and its descenders touch
that name. The fit allows halos to touch. It has no minimum gap between
names. That is the next lead.
