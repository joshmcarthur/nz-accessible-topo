# 0059 — Italic marks natural features in Topo50

**Date:** 2026-11-04

## Question

Is italic in Topo50 only the water convention (F-08), or does it carry a wider class meaning that R-05 removed?

## What we did

Read the stock BX24 `nztopo50_carto_text.parquet` with DuckDB. Kept rows whose bounding box lies inside the 4 km grid extent (1564000–1588000 E, 5154000–5190000 N). The data has no feature-class column. Grouped names by colour (blue for water), by number-only text (spot heights), and by generic words (Valley, Head, Saddle, Peak, Mount, Point, Rock, Island, Pass, Gully). Listed every italic name that is not water or a number. Listed every upright name that holds a landform word.

## What we found

| Group | Rows | Italic |
|---|---:|---:|
| Water (blue) | 66 | 66 |
| Spot heights and numbers | 231 | 230 |
| Roads and tracks | 306 | 0 |
| Facilities and culture | 177 | 0 |

The 69 other italic names are all natural features. Examples: Mount Bradley, Gebbies Pass, Waipuna Saddle, Lions Head, Godley Head, Moki Point, Shag Rock, Quail Island, McQueens Valley, Church Gully, Bottle Lake Forest, Omahu Bush.

Upright names that hold a landform word are settlements, localities, huts or roads: Gebbies Valley, Heathcote Valley, Kaituna Valley, Mount Pleasant, Kain Hill, Kowhai Hills, Horomaka Island Hut, Mount Herbert Shelter.

Italic in Topo50 is the natural-feature class cue. F-08 recorded it only as the water cue. R-05 removed italic, so on the accessible grid McQueens Valley reads the same as Porahu (log 0057, G3).

The contour-number FontMarkers are text drawn as a symbol. They are still italic. The R-05 check counted label styles only.

## What changed

- F-08 and F-30 in `docs/findings/typography.md` record the class meaning.
- R-05 "Met when" covers FontMarker text and needs a non-italic natural-feature cue. R-05 is open again.

## Confidence & gaps

The grouping uses generic words, not a class field, so a few names may be in the wrong group. One sheet only. Which cue to use (colour, weight or case) is a design choice for the backlog. Its effect on readers is not tested (R-16).
