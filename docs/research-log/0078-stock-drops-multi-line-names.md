# 0078 — LINZ's own stock export drops multi-line names

**Date:** 2026-11-05

## Question

Josh noticed the accessible grid shows more names than stock. Does the
stock sheet drop names when they would collide?

## What we did

Compared the placed carto_text labels from `count_label_collisions.py` for
stock and accessible. Then compared seven names that only accessible draws
with LINZ's own export of the sheet (log 0025, `map` container, QGIS
4.2.2, `BX24.png` at 150 dpi). Located the map face on that page by
correlating it with our stock face (correlation 0.73). Cropped each name
from the LINZ export, our stock render, and the accessible render
(`docs/visuals/11-multiline-names-linz-vs-ours.png`).

## What we found

Neither project drops names for collisions. carto_text allows overlap and
is not an obstacle. Every stock name is also in accessible.

Stock draws 60 multi-line names on the extent and accessible draws 71.
LINZ's own export fails the same names as our stock render:

| Name | LINZ export | Our stock | Accessible |
|---|---|---|---|
| Mt Herbert / Te Ahu Patiki | missing | "Mt" and "Herbert" upside down | drawn |
| Te Wharau / Charteris Bay | missing | "Te" and "Wharau" upside down | drawn |
| Te Waipapa / Diamond Harbour | "Te" and broken "Wa apa" | missing | drawn |
| Te Onepoto / Taylors Mistake | "Te" and "Onep" | missing | drawn |
| Te Heru-o-Kahukura / Sugarloaf | missing | broken, upside down | drawn |
| Pukerauaruhe Island | missing | missing | drawn |

QGIS 4.2 cannot fit these multi-line names on their curved baselines in
the LINZ project. The fault is in the stock project, not in our square
script. The accessible flat rule (logs 0052, 0074) draws them straight.

The accessible face also looks busier for a second reason. Type is 7 pt
upright Regular. Stock is 5.5 to 6 pt Narrow Italic. The same name covers
about 1.5 to 2 times the area.

## What changed

- This log and the evidence image.
- `docs/method.md`: the collision count understates stock collisions where
  stock fails to draw a name.

## Confidence & gaps

Grade C for the comparison (same data, LINZ's own export). The published
print Topo50 came from a different pipeline and is not checked here. The
G2 "new collisions" count is biased against accessible near multi-line
names.
