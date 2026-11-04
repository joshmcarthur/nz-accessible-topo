# 0073 — Label collisions measured; wider fit reach

**Date:** 2026-11-05

## Question

How many label collisions does the accessible face add over stock (G2)?
Does a wider fit reach reduce them?

## What we did

Wrote `tools/count_label_collisions.py`. It draws the face with the QGIS
labelling engine and intersects the label shapes of every placed pair. A
pair counts as new when stock has no collision between the same two texts.
Ran it on the BX24 4 km extent for stock and accessible.

Re-ran `fit_carto_labels.py` from a clean apply. The fit file was the same
as the 3 November file, so it was not stale.

Widened the fit reach from 1.5 mm to 3 mm across and from 0.5 mm to 1.5 mm
up. The move cost stays at 40 per mm. Rendered the grid and compared
`1572000-5170000` before and after.

## What we found

Stock places 7,268 label parts for 5,510 carto_text features. Accessible
places 5,510. No name is missing. Stock splits some curved names into parts.

New collisions over stock:

| Overlap on the ground | Before | 3 mm reach |
|---|---|---|
| > 500 m² | 315 | 307 |
| > 2000 m² (0.8 mm² on paper) | 158 | 134 |
| > 5000 m² | 32 | 26 |

Stock has 4 collisions over 2000 m². G2 still fails.

Of the 134, 59 involve a multi-line name (placement 34), such as
"Te Waipapa / Diamond Harbour". The fit tool moves only one-line flat names.
Most others are along-line road names that meet at junctions.

On `1572000-5170000` "Ōtūherekio" moved off the Cass Bay water name, and
"Te Ahi-a-Tamatea" moved off "Te Upoko-o-Kurī". No name moved away from its
feature.

The label shape is not always the drawn text. "Te Upoko-o-Kurī / Witch
Hill" and "Te Ahi-a-Tamatea" report 49,164 m² of overlap, but they only
touch on the render. Treat the counts as a trend, not as exact areas.

## What changed

- `fit_carto_labels_main.py`: `REACH_X_MM` 3.0, `REACH_Y_MM` 1.5.
- `tools/count_label_collisions.py`, `nzat.qgis.new_collisions` and a test.
- `docs/method.md` names the tool. B-31 records the counts.

## Confidence & gaps

Grade D. The metric is approximate. Next levers: fit multi-line names, and
shift along-line names away from junctions.
