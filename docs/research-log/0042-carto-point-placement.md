# 0042 — Flat carto text moves to free space

**Date:** 2026-11-02

## Question

Can QGIS move a name that collides after the larger accessible type, instead of drawing it on top of another name?

## What we did

Every clashing label in the cold spring square is a `nztopo50_carto_text` row. Each row has one hand-drawn baseline for 6–7 pt Nimbus. The layer draws it with curved placement and `AllowOverlapIfRequired`. One fixed baseline gives QGIS no other place to put the label. No row links to the feature it labels.

The apply step now splits `nztopo50_carto_text` into two label rules:

- Flat one-line rows (`text_placement = 1`, `text_orientation = 0`, no line break) get a short horizontal line at the stock baseline. The line is centred on the stock label. It is the estimated accessible label width plus 1 mm at each end. Parallel line placement allows above and below the line, with 0.5 mm overrun. The stock `offset` distance stays.
- Every other row keeps the curved settings and the fold split.

A flat dual name breaks after its ` / `, so `Ōmawete / Coopers Knob` draws on two centred lines. The line length uses the longer line. The flat rule labels only the largest part of its line, so both text lines draw.

A flat single name longer than 16 characters wraps at 16 (`labels.carto_point.wrap_chars`). A leading `Te ` gets a no-break space, so `Te` stays with the next word. The flat rule's line height is 0.85 (`line_height`).

The width estimate is characters × size × 0.6 em. Atkinson measures 0.45–0.63 em per character on the cold spring names. `AllowOverlapIfRequired` stays. No name is removed.

The four squares were drawn again with QGIS 4.2.3.

## What we found

- Cold spring: `Rhodes Spring`, `Ōmawete / Coopers Knob`, and `A579` stay at their stock positions and do not overlap. `573m` flips below its baseline to clear `A579`.
- QGIS prefers the middle of the line, so the stock position wins when it is free. The sideways move is limited to about 1.5 mm (75 m).
- A line label draws where its line crosses the drawn extent. Names at the square edge still draw. The closed foot track square now shows `150` and a cut-off `Awaro…` at its edges.
- Estuary and Port Hills did not change. Their names are multiline or along a line.
- Two earlier tries used cartographic point placement around the stock label centre. Orders `O, T, B, R, L, TR, TL, BR, BL` and `O, T, B, TSR, TSL, BSR, BSL, TR, TL, BR, BL` both moved `Ōmawete / Coopers Knob` about 500 m east. QGIS aligns the "slightly" positions to the anchor point, so `TSR` also moves a centred label by half its width. A point label whose anchor is outside the drawn extent is not drawn.
- `@map_scale` is null in a label geometry generator. The line uses the fixed 1:50,000 sheet scale.
- On the full BX24 face, the two-line split clears four of six dual names: Adderley, Godley, Cass, and Aua. `Ōmawete /` still overlaps `Rhodes Spring`. `Te Upoko-o-Kurī /` still overlaps `421` and `Te Moeng…`.
- The flat rule keeps the stock strict line anchor at 50 %. The label stays at the middle of its line, and the allowance gives no sideways move. A 2 mm allowance, the on-line position, and a lower spot-height priority gave no change.
- With `PreventOverlap`, the two overlapping dual names are not drawn. No free position exists for them.
- A hint anchor lets QGIS slide the label. It also moves `Godley Head` onto `Gun emplacements` and `Ōrongomai` onto `505`, with free water below `Godley`. Rule priority 5 and label engine version 2 gave the same result. The strict anchor stays.
- A square or a crop moves labels to fit its extent. Placement is judged on the full face.
- QGIS sizes a one-line label box from the font ascent plus descent. NZAT Legible Test has 984 + 316 = 1.3 em. On one line, `Ōmawete / Coopers Knob` fits above its baseline in ink, but its box overlaps `Rhodes Spring` and `A579` by about 1 mm. The macron on `Ō` reaches 829, higher than the bottom of the `Spring` descenders (−192), so a box drawn tight to the letters also collides. QGIS then puts the name below, on `A579`.
- Tighter font metrics (850 / 200), size-based priority, obstacles off, and `IgnoreWhitespaceCollisions` did not move it above. QGIS cannot choose between two texts for one label.
- Spot heights at 6 pt cleared no name. The wrap clears `South Hagley Park` from `Sch` and `HAGLEY AVE`. QGIS's own wrap breaks `Te | Upoko-o-Kurī | / Witch Hill`, so dual names are not wrapped.
- At 0.85 line height, `Ōmawete /` sits fully under `Rhodes Spring`.

## What changed

- `tools/override_topo50_project.py`: `patch_carto_point_labels`, `carto_flat_line_expression`, and `carto_flat_wrap_expression`.
- `tools/style-topo50.json`: `labels.carto_point` (`allowance_mm`, `advance_em`, `overrun_mm`, `wrap_chars`, `line_height`).
- `tools/test_tools.py`: the carto_text test checks both rules, the wrap, and the line height.
- The four accessible square pictures in `docs/visuals/squares`, and the accessible half of `docs/visuals/10-bx24-compare.png`.

## Confidence & gaps

The width is an estimate. A long all-caps name can be wider than its line. The allowance and the overrun cover the cold spring names. If no free position exists within the allowance, the name overlaps in place. The `map` container runs QGIS 4.2.2. The full sheet has not been exported again. `docs/visuals/10-bx24-compare.png` shows the full face with the split. We do not know why QGIS moves a sliding label onto a fixed curved label when free space exists. The wrap applies to every long single name, including names that had room. A wrap only where names collide needs a step that renders, measures, and chooses; it would use the same boxes and would not fix the spring.
