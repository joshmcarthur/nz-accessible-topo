# 0103 — Map5View-paper and Map5View-all

**Date:** 2026-11-06

## Question

Josh asked for named variants of the hidden-layer set: one `-paper`, one `-all`.
N-5 said confirm before turning layers on. These names keep the print sheet
and a full-symbol proof as two themes, not one toggle.

## What we did

Apply copies stock `Map5View` to `Map5View-paper` (same visibility) and
`Map5View-all`. `-all` turns on `map.all_layers` in the style file and removes
the empty `checked-legend-nodes` on `relief_line map`, so those rules draw.
Square, sheet, and legend renders take `--theme`. The default stays `Map5View`.

## What we found

Map5View already lists `structure_line`, `structure`, and `structure_point` at
`visible="0"`. `water_point`, `tunnel_line`, `landcover_point`, `landuse`, and
`marine` are absent from the preset. `-all` adds them. `relief_line map` is
visible, but its checked-legend-nodes list is empty, so no relief mark draws
on the print theme.

## What changed

- `src/nzat/qgis/patch_map_themes.py`
- `map` keys in `tools/style-topo50.json`
- `--theme` on `render_square.py`, `render_sheets.py`, `render_legend.py`

## Confidence & gaps

XML-fixture tests cover the preset copy. QGIS apply still has to write the
themes into the BX24 project. Blocked `/symbols/` rows stay blocked until a
legend or export run uses `--theme Map5View-all`.
