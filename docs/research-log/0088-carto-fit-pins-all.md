# 0088 — The label fit pins every flat name

**Date:** 2026-11-05

## Question

Can the render match the label fit model if the fit pins the names it
does not move?

## What we did

The fit wrote a row only for names it moved. QGIS placed the other flat
names again in the final render. Now the fit writes a row for every flat
name it reads, moved or not. Each row pins the name with PositionX and
PositionY.

Pinning alone moved three other pairs closer. So we also tried a taller
gap band above and below a name. We ran the fit, the collision count and
the grid render for each step.

We also tried a fit that moves names whose boxes come within the gap band
of a neighbour, not only names whose boxes touch. It changed no count. We
dropped it.

## What we found

| Run | New >500 / >2000 / >5000 m² | Name pairs >2000 m² | New overlap m² |
|---|---|---|---|
| log 0087 (moved names only, band 0.4 mm) | 184 / 93 / 40 | 66 | 746,767 |
| pin all, band 0.4 mm | 183 / 94 / 41 | 67 | 752,766 |
| moved names only, band 0.6 mm | 168 / 91 / 38 | 63 | 676,707 |
| pin all, band 0.6 mm (kept) | 170 / 92 / 38 | 64 | 680,347 |

All runs place 4193 labels. Pinning drops no label.

- "North Hagley Park"/"Victoria Lake" box overlap fell from 78,011 to
  19,820 m². The render now shows a clear gap. In log 0087, QGIS moved
  "Victoria Lake" up 84 m after the fit. The pin keeps it where the fit
  model had it.
- Without pins, the 0.6 mm band leaves "North Hagley Park"/"Victoria Lake"
  at 80,790 m². The pin is the part that fixes this pair.
- "Te Ahi-a-Tamatea"/"Te Moenga-o-Wheke / The Tors" fell from 10,758 to
  0 m². "Te Upoko-o-Kurī / Witch Hill" now takes one line above both. It
  does not cross "Te Ahi-a-Tamatea" (cell 1572000-5170000).
- "Kaituna Pass"/"Remarkable Dykes" fell from 22,863 to 0 m².
- Three pairs got worse. "Major Hornbrook Track"/"Mt Cavendish" went from
  0 to 25,172 m². "Ferrymead Park"/"Substation" went from 0 to 6,815 m².
  "Casebrook"/"Sch" went from 0 to 6,150 m². In each pair, about 0.3 mm
  of white is left between the names. Before the pin, QGIS had moved one
  name away by chance.
- For "Ferrymead Park", the fit model finds no ink of the name within
  0.6 mm of "Substation". The render shows about 0.35 mm. So the model
  and the render still differ in the vertical gap.

## What changed

- `fit_carto_labels_main.py`: writes a fit row for every flat name.
  `carto_fit.json` now holds 425 rows, not about 120.
- `best_candidate.py`: `GAP_Y_PX` is 15 (0.6 mm), not 10.
- Test in `tests/qgis/test_best_candidate.py`. It fails with the 0.4 mm
  band. The pin step needs QGIS, so the test covers only the band.
- `docs/style-topo50.md`, B-31.

## Confidence & gaps

Grade B. The render now follows the fit model. The counts improve on log
0087. Two named pairs are fixed. Three pairs are closer than before.

- The fit model reads a larger vertical gap than the render at
  "Ferrymead Park"/"Substation". Find where the masks and the QGIS label
  box differ in height or baseline. Fix that before a wider band.
- The run with no pins counts a little better (168 / 91 / 38). It leaves
  the Hagley pair touching. The difference is three local pairs.
