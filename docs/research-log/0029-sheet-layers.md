# 0029 — Draw the sheet layers

**Date:** 2026-11-02

## Question

Why do the square pictures show heavy pink lines, and why does "Heathcote" sit upside down?

## What we did

The square renderer now draws the `Map5View` layers. That is the layer set on the `tiff-50` map. The accessible project leaves `charplace` as `StretchWordSpacingToFit`. The four squares were rendered again at 600 dpi. Stock and accessible use the same extent and the same scale.

## What we found

`landcover_line` is hidden in `Map5View`. The square used to draw it. That layer asks for `feature_type`. The column is `type`. Unmatched rows use the empty symbol. That symbol is a 0.66 mm line in `255,0,159`. `building_point` is also hidden. It draws a square outline in `229,100,163`. The sheet draws `building_point map` instead.

The closed-track square now has 0 pixels in that hot pink. The stock square and the accessible square match the official map face: brown contours, black building squares, a green track, and the name Awaroa.

"Heathcote" is no longer on the estuary square upside down. The accessible square draws "Estuary" upright, as the stock square does.

Each square is its own draw. One run draws the four squares for one project. This batch used two runs. The output of each draw is 472 px. The draw still takes minutes. The layers point at national GeoParquet.

## What changed

- `tools/render_square.py` keeps the `Map5View` layers.
- `tools/override_topo50_project.py` does not replace `charplace`.
- The eight square pictures are in `docs/visuals/squares/`.

## Confidence & gaps

R-09 stays open. The 20% hierarchy list is still not named. Do not start R-07.
