# 0042 — Flat carto text moves to free space

**Date:** 2026-11-02

## Question

Can QGIS move a name that collides after the larger accessible type, instead of drawing it on top of another name?

## What we did

Every clashing label in the cold spring square is a `nztopo50_carto_text` row. Each row has one hand-drawn baseline for 6–7 pt Nimbus. The layer draws it with curved placement and `AllowOverlapIfRequired`. One fixed baseline gives QGIS no other place to put the label. No row links to the feature it labels.

The apply step now splits `nztopo50_carto_text` into two label rules:

- Flat one-line rows (`text_placement = 1`, `text_orientation = 0`, no line break) get a short horizontal line at the stock baseline. The line is centred on the stock label. It is the estimated accessible label width plus 1 mm at each end. Parallel line placement allows above and below the line, with 0.5 mm overrun. The stock `offset` distance stays.
- Every other row keeps the curved settings and the fold split.

The width estimate is characters × size × 0.6 em. Atkinson measures 0.45–0.63 em per character on the cold spring names. `AllowOverlapIfRequired` stays. No name is removed.

The four squares were drawn again with QGIS 4.2.3.

## What we found

- Cold spring: `Rhodes Spring`, `Ōmawete / Coopers Knob`, and `A579` stay at their stock positions and do not overlap. `573m` flips below its baseline to clear `A579`.
- QGIS prefers the middle of the line, so the stock position wins when it is free. The sideways move is limited to about 1.5 mm (75 m).
- A line label draws where its line crosses the drawn extent. Names at the square edge still draw. The closed foot track square now shows `150` and a cut-off `Awaro…` at its edges.
- Estuary and Port Hills did not change. Their names are multiline or along a line.
- Two earlier tries used cartographic point placement around the stock label centre. Orders `O, T, B, R, L, TR, TL, BR, BL` and `O, T, B, TSR, TSL, BSR, BSL, TR, TL, BR, BL` both moved `Ōmawete / Coopers Knob` about 500 m east. QGIS aligns the "slightly" positions to the anchor point, so `TSR` also moves a centred label by half its width. A point label whose anchor is outside the drawn extent is not drawn.
- `@map_scale` is null in a label geometry generator. The line uses the fixed 1:50,000 sheet scale.

## What changed

- `tools/override_topo50_project.py`: `patch_carto_point_labels` and `carto_flat_line_expression`.
- `tools/style-topo50.json`: `labels.carto_point` (`allowance_mm`, `advance_em`, `overrun_mm`).
- `tools/test_tools.py`: the carto_text test checks both rules.
- The four accessible square pictures in `docs/visuals/squares`.

## Confidence & gaps

The width is an estimate. A long all-caps name can be wider than its line. The allowance and the overrun cover the cold spring names. If no free position exists within the allowance, the name overlaps in place. The `map` container runs QGIS 4.2.2. The full sheet has not been exported again.
