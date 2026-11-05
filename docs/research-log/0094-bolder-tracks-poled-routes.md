# 0094 — Bolder foot tracks, a larger closed ×, and dotted poled routes

**Date:** 2026-11-05

## Question

Josh decided the track symbols. How do we apply his decision?
Why did a poled route draw like a foot track?

## What we did

Recorded Josh's decision. His words:

- "the LINZ styles are fine, they just need to be slightly bolder"
- "the closed symbol already in use is fine, it just needs to be made
  slightly bolder and larger"

Read the stock `track_line map` renderer. Counted `track_type` values in
`track_line.parquet` with DuckDB. Measured the "Poled route, track
connector" row in the stock legend `topo-legend-1.tif` (600 dpi). Changed
the apply step. Rendered the 4 km BX24 grid, three 1200 dpi extents, and
the sheet legend.

## What we found

### Why poled routes looked like foot tracks

- The stock renderer categorises on `subtype` only: vehicle, foot, cycle
  only.
- `track_type` is `route` on 422 foot rows (poled routes) and `connector`
  on 1 row. 3 routes are closed.
- So a poled route and a connector drew the foot-track dash.
- The printed LINZ legend draws them as dots: heavier dots for a poled
  route, finer dots for a connector.

### Stock legend measurements

- Dot pitch is 24.3 px at 600 dpi. That is 1.03 mm for both rows.
- A poled-route dot holds about 72 px of ink. That is a 0.40 mm round dot.
- A connector dot holds about 22 px of ink. That is a 0.22 mm round dot.
- The brief said "about 0.3 mm" for the poled-route dot. That is lighter
  than the LINZ dot. Josh asked for the LINZ look, slightly bolder. So the
  dot is 0.45 mm, not 0.3 mm.

### Where to look

- BX24 has no poled route and no connector.
- BX24 has one closed foot track: Godley Head Gun Emplacements Track.
- Hope Pass Track (NZTM 1536400,5278600 to 1539400,5281600) is a poled
  route that meets the Hope Kiwi foot track.
- Lower Matakuhia Track (NZTM 1910000,5686500 to 1913000,5689500) is a
  closed poled route that meets the open Matakuhia foot track.

### Render

- Foot tracks keep the 1;0.5 mm dash. The line is heavier.
- On the G1 cells (`1576000-5182000`, `1580000-5170000`,
  `1572000-5170000`, `1584000-5158000`, `1576000-5166000`) open foot tracks
  show no ×. The heavier dash still reads as a track.
- At Godley Head the 0.7 mm × reads as a ×. It does not read as railway
  ticks, an embankment comb, or a cliff.
- The × is wider than the 0.5 mm dash gap. It touches the dash ends. The
  3 mm interval still leaves two clear dashes between marks, so the
  interval does not change.
- Hope Pass Track now draws as dots. Hope Kiwi Track stays dashed.
- Lower Matakuhia Track draws as dots with the × on top.
- The legend rows now differ: dashes for a foot track, dashes with × for a
  closed track, heavy dots then fine dots for the poled route row.

- Before and after crops: `docs/visuals/14-bolder-tracks-before-after.png`.
  Rows from the top: Hope Pass Track (poled route) at 1200 dpi, Lower
  Matakuhia Track (closed poled route) at 1200 dpi, Godley Head (closed foot
  track) at 300 dpi stock vs this render, then the legend track rows before
  and after.

## What changed

- `tools/style-topo50.json`:
  - `tracks.closed_foot.width_mm` and `open_width_mm`: 0.15 → 0.2.
  - `tracks.closed_foot.crossbar_size_mm`: 0.5 → 0.7.
  - `tracks.closed_foot.crossbar_outline_width_mm`: 0.1 → 0.15.
  - New `tracks.dotted`: `colour` `#000000`, `interval_mm` 1.0,
    `route_dot_mm` 0.45, `connector_dot_mm` 0.3.
- `src/nzat/qgis/patch_tracks.py`:
  - The dashed foot line is off when `coalesce("track_type", '')` is
    `route` or `connector`.
  - Two new marker lines draw round dots for `route` and `connector`.
    Their filters use `coalesce()`, so NULL is never "on" (log 0092).
  - Dots sit so each closed × falls midway between two dots.
  - The closed × draws last, so it sits over the dots.
  - A second apply replaces the dots and moves the × to the end. It does
    not stack markers.
- Tests in `tests/qgis/test_patch_tracks.py`: open poled route draws dots
  not dashes; closed poled route keeps the ×; open foot track has no ×; the
  widths and dot sizes come from the style file; a second apply does not
  stack markers.
- `docs/style-topo50.md`, `BACKLOG.md` (B-30, B-46), log index.
- The legend in `squares/accessible/` was drawn again. The sheet projects
  in `squares/accessible-sheets/` and `sheets/` were not touched.

## Confidence & gaps

Grade D for the look (our review of one BX24 closed track, the G1 cells,
and two extents off BX24).

- The vector build has no `track_type` paint for dots. The vector style
  keeps its own poled-route layers. Vector parity for the dots is a gap.
- The vector build reads none of the changed widths. `tools/build_style.py`
  writes no new output.
- The 0.45 mm dot is heavier than the 0.3 mm in the brief. Josh may want
  it lighter.
- Closed vehicle tracks (3 rows) are not in scope. They keep the stock
  vehicle symbol.
- The sheet batch predates this change. Its faces keep the old tracks.
