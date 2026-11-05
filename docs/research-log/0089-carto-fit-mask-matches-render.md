# 0089 — The label fit masks match the render

**Date:** 2026-11-05

## Question

Log 0088 said the fit model reads a larger vertical gap than the render.
Is the glyph mask in the fit placed at a different height from the name
that QGIS draws?

## What we did

We used a probe script. It reads the accessible project with the
`carto_fit.json` from log 0088. It renders only the carto_text layer at
2 m per pixel (635 dpi), the same grid as the fit. It builds each name's
ink mask with the same code as `fit_carto_labels_main.py`. It stamps the
mask at the pinned point, as the fit does. Then it compares the mask
pixels with the rendered ink pixels.

We did this for the three pairs that got worse in log 0088:
"Ferrymead Park"/"Substation", "Major Hornbrook Track"/"Mt Cavendish" and
"Casebrook"/"Sch". We also searched for the shift that best aligns mask
and render, from -4 to +4 pixels in each direction.

## What we found

| Pair | Best mask shift (rows, cols) | Ink gap | Box overlap (log 0088) |
|---|---|---|---|
| Ferrymead Park / Substation | +1, 0 | 1.24 mm | 6,815 m² |
| Major Hornbrook Track / Mt Cavendish | not measured | 0.64 mm | 25,172 m² |
| Casebrook / Sch | +1, −1 | 0.64 mm | 6,150 m² |

- The mask and the render agree to 1 pixel (2 m, 0.04 mm). The render is
  1 pixel lower. Rounding of the mask origin can explain it. It is not a
  baseline or descent error.
- Mask width and height equal the QGIS label box to 0.1 pixel for all
  names we checked.
- The ink gap between "Ferrymead Park" and "Substation" is 1.24 mm in the
  render. The 0.35 mm in log 0088 was not an ink-to-ink gap.
- The ink gap is 0.64 mm for "Major Hornbrook Track"/"Mt Cavendish" and
  for "Casebrook"/"Sch". That is the 0.6 mm gap band plus one pixel. The
  fit did what the model asked.
- The collision counter measures QGIS label boxes, not ink. A one-line
  7 pt box is 3.2 mm tall. It has about 0.8 mm of empty space above the
  capitals and 0.7 mm below the baseline. Two names with a 0.6 mm ink gap
  can still have boxes that overlap by about 1 mm.
- So the three "worse" pairs in log 0088 are box overlaps. Their ink does
  not touch, and there is a clear gap between the names.

## What changed

Nothing in the code. No mask offset was found to fix.

## Confidence & gaps

Grade B for "the masks match the render". We checked three pairs and
five names in one area of the sheet. All agree to 1 pixel.

- The box counter over-counts stacked names. A count of ink overlap, or
  ink within a gap band, would show what a reader sees. Add it beside the
  box count before more tuning against box numbers.
- Neighbours that are not flat names are still stamped as full QGIS
  boxes. That makes the fit keep too far from them, not too close.
- "Mt Cavendish" is drawn in a colour the probe did not class as ink. Its
  check used the mask only.
