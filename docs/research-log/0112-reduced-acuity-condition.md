# 0112 — A reduced-acuity condition for the symbol tiles

**Date:** 2026-11-10

## Question

The six vision conditions test colour and lightness. None tests size. Which
symbols does a reader with reduced acuity lose?

## What we did

- Read the WHO vision impairment grades (S-WHO-ICD11-VISION) and a
  validated low-vision image filter (S-XIONG-2021). New finding F-32.
- Added a seventh condition to `tile_visibility.py`: typical colour vision
  through a Gaussian blur in linear light. The blur is as wide (full width
  at half maximum) as the detail a 6/18 eye resolves at 400 mm: 3 arc
  minutes, 0.35 mm on the sheet, 8.2 px at 600 dpi, sigma 3.5 px. The
  floor is the same CIEDE2000 10 as for typical colour vision.
- 6/18 is the WHO limit of mild impairment. 400 mm is a common near-test
  distance.
- Scored the 1146 tiles again.

## What we found

476 tiles fail one condition or more. 141 of them fail reduced acuity only.

On paper, with nothing across the symbol, 20 of 86 symbols fall below half
visible under reduced acuity:

- **Nothing left (0 to 6%):** hot spring cross, embankment, stopbank,
  unmetalled road, intermediate and supplementary contours, the sand and
  mud stipples, the vegetation fills.
- **Under half:** moraine wall, scree, shingle, depression contours, tank,
  spot-height dot, ice contours, cutting, cliff, uncovered reservoir,
  large canal.

A pattern fill that blurs to a flat tint still marks its area, so the
stipple and vegetation rows are less serious than the score says. The
point and line marks are the real losses: the hot spring cross, the
spot-height dot, the tank, and the relief ticks.

The intermediate contour result agrees with the accepted exception (log
0054): the 20 m mesh is recessive by design.

## What changed

- `docs/findings/size-and-weight.md` (F-32), `docs/sources.md`.
- `src/nzat/render/tile_visibility.py`, `tests/render/test_tile_visibility.py`.
- `site/src/data/symbol-tiles.json`, `site/src/pages/symbol-tiles.astro`.

## Confidence & gaps

Grade D for the numbers. The principle (acuity loss removes high spatial
frequencies) is grade B.

- The blur is not the validated filter. It has no contrast sensitivity
  term, and the width rule (full width equals the resolved detail) is our
  own choice.
- We read the WHO grades from a table in a journal article, not from the
  ICD-11 page.
- One acuity level and one reading distance. A reader at 6/12, or at
  300 mm, loses less.
- No recommendation rests on F-32 yet. R-09 and the F-31 line floors are
  the place for it.
