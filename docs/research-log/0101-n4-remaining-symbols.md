# 0101 — Remaining N-4 symbol paint

**Date:** 2026-11-06

## Question

Which remaining `/symbols/` rows that already have a proposal can the apply
step paint now, without a new Josh decision, a hidden Map5View layer, or an
invented class?

## What we did

- Read the remaining `proposed` rows in `src/nzat/site/symbol_rows.py`.
- Read the stock BX24 `nztopo50.qgs` renderers and the national parquet
  class counts (`track_type`, `subtype`, `designation`, `formation`,
  `vegetation.subtype`, `water_line.type`, `relief_point.type`).
- Wrote failing QGIS XML-fixture tests, then patched apply to match each
  proposal. Sizes and inks live in `tools/style-topo50.json`. Owned SVGs
  live in `src/nzat/qgis/symbols/` and copy with `install_owned_symbols`.
- Did not apply fumarole. Did not turn on Map5View-hidden layers. Did not
  run QGIS apply/render.

## What we found

- `railway_line.track_type` is `multiple` on 26 rows. The layer was a
  single 0.25 mm black line. Data-defined width 0.6 mm plus a white dash
  that is on only when `coalesce("track_type", '') = 'multiple'` draws the
  LINZ bar. Single track stays 0.25 mm.
- Two-lane bridge casings at the 0.15 mm line floor did not meet the
  proposal (0.2 mm casings, 1.4 mm ticks). `bridges.two_lane` now holds
  those sizes.
- `building.subtype` includes `greenhouse` (1432 polygons). A rule renderer
  draws those as a 0.2 mm black outline with no fill. Other buildings stay
  solid black.
- Vegetation `type=exotic` splits on `subtype`: 42473 `coniferous`, 2254
  `non-coniferous`. Both can take owned marks in `#6A9A50`. Outline was
  already `#859E3E` from `patch_vegetation._paint_outlines`.
- Contour `designation` is `supplementary` on 1849 rows. `formation` is
  `depression` on 3640 rows. Dash and ticks use `coalesce()` so a NULL
  value does not turn the extra paint on (QGIS 4.2.3 reads NULL as true).
- `relief_point.type` is `saddle` on 700 rows. Spot heights stay 0.3 mm
  dots. Stock `.qgs` fieldConfiguration still says `feature_type`. The
  parquet column is `type`, so the filter uses `type`.
- Moraine, scree and shingle all pointed at `nztopo50_shingle.svg`. Owned
  textures restore crosses/rings, fine stipple, and the original shingle
  at 0.15 mm stroke.
- `water_line.type` is only `river`, `drain`, and `canal`. There is no
  sink or disappearing class. Stream-disappearing stays proposed. Do not
  put an arrow on every river.
- Native fill is unchanged. Fumarole still waits on log 0096.

## What changed

- `src/nzat/qgis/patch_railway.py`, `patch_landcover.py`,
  `patch_relief_point.py`
- `src/nzat/qgis/patch_structures.py`, `patch_contour.py`,
  `patch_vegetation.py`, `patch_thin_lines.py`, `apply.py`
- `src/nzat/qgis/symbols/` (owned copies)
- `tools/style-topo50.json`, `docs/style-topo50.md`
- `src/nzat/site/symbol_rows.py`
- `tests/qgis/test_patch_*.py`

## Confidence & gaps

XML-fixture tests cover the paint. Sheet proof still needs QGIS apply and
grid review. Stream-disappearing still needs a real sink class. Fumarole
still needs Josh. N-5 still hides Map5View-off layers.
