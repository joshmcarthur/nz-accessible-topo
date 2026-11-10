# Tools

Python lives in `src/nzat/`. Files in this directory are thin wrappers, so
`python3 tools/build_style.py` still works. After `uv sync`, run tools with
`uv run python tools/...`. Tests live under `tests/`: `uv run pytest`. Lint:
`uv run ruff check`.

## palette_audit.py

Audits a MapLibre GL style JSON for:

- text contrast (WCAG 2.x ratio) of each label against its halo;
- separability of declared "must-distinguish" colour pairs under normal
  vision, protanopia, deuteranopia, tritanopia (Machado et al. 2009 matrices),
  greyscale, and a crude red-headtorch model.

```
python3 tools/palette_audit.py path/to/style.json \
    --pairs tools/pairs-accessible-v0.json \
    --md docs/current-state/audit-linz-topographic-v2.md
```

Pair colours that live in `tools/style-topo50.json` are dotted paths.
`palette_audit.py` resolves those paths before it measures. Literal hex stays
for paper and for LINZ inks the style file does not own.

The maths is checked against reference values (CIEDE2000 Sharma et al. test
pairs; black/white = 21:1). The *perceptual thresholds* used to flag results
are working assumptions — treat output as evidence grade D.

Known limitations:
- Data-driven (`["match", ...]`, `stops`) colours are skipped; only literal
  colours are audited.
- Labels drawn on an icon (e.g. highway shields) are reported against the
  map background and show as false failures.
- Simulation is for *dichromacy* (severity 1.0). Anomalous trichromats see
  more than this; it is a worst case.

## tag_urban_text.py

Tags `carto_text` names inside the urban fill (`residential_area map`). It
writes `urban_text.json` beside the project: a sorted list of row ids. The
apply step gives a black name in that list an urban-fill halo. A layer lookup
in a label expression hangs the render (log 0090), so this runs once, before
the apply step.

```
python tools/tag_urban_text.py --project accessible/nztopo50.qgs
python3 tools/override_topo50_project.py stock/nztopo50.qgs accessible/nztopo50.qgs
```

Run it with the QGIS Python. With no `--extent` it tags every row in the
country: 3456 ids, 135 KB, about 10 s (log 0093).

## fit_carto_labels.py

Fits flat `carto_text` names whose labels collide. QGIS tests label boxes as
yes or no. This tool scores glyph ink and halo, so it can choose the position
with the least overlap. It tries each name on one line or in its wrapped form,
moved in 0.25 mm steps. It writes `carto_fit.json` beside the project. Run the
apply step again to draw the fitted names.

```
python tools/fit_carto_labels.py --project accessible/nztopo50.qgs \
    --font fonts --extent 1564000,5154000,1588000,5190000
python3 tools/override_topo50_project.py stock/nztopo50.qgs accessible/nztopo50.qgs
```

Run it with the QGIS Python. Other labels count as filled boxes. Point symbols
are not counted. The glyph masks are about 2.5% smaller than the QGIS boxes.

## render_symbol_tiles.py

Draws each legend symbol in 10 mm test tiles at sheet size, 600 dpi. One
tile for each fill under the symbol (paper, native, exotic, scrub, scattered,
water, urban, sand, swamp, ice). One tile for each class across it on paper
(contour mesh, grid line, stream, road, name). The samples come from the
legend swatch table and draw through the applied map layers.

```
$QPY tools/render_symbol_tiles.py --project accessible/nztopo50.qgs \
    --font fonts --out render/symbol-tiles
```

Run it with the QGIS Python, after the apply step. `--key` draws one swatch.
The output is one folder of tiles and one strip PNG per swatch key, and
`tiles.json`. 86 keys, 1146 tiles, about 60 s.

## export_symbol_tiles.py

Scores the symbol test tiles and writes `site/src/data/symbol-tiles.json`.
The ink pixels of the paper tile are the symbol. A pixel stays visible when
it still differs from the ground just outside the symbol: 3:1 for greyscale
and red light, CIEDE2000 10 for the colour conditions. In a conflict tile
the pixel must also keep its paper-tile colour. A tile fails a condition
when under half of the ink stays visible. That half is our own floor (grade D).

```
uv run python tools/export_symbol_tiles.py
```

Run `render_symbol_tiles.py` first. CI does not run this: the tiles are not
in the repo. The score does not test shape confusion, for example a spot
height dot on the sand stipple.

## find_symbol_sheets.py

Find 4 km squares that hold legend classes BX24 does not. Uses DuckDB in the
QGIS Python. Host Python does not have DuckDB.

```
$QPY tools/find_symbol_sheets.py --out /tmp/symbol-cover.json
$QPY tools/find_symbol_sheets.py --render-dir render/legend-cover --theme Map5View-all
```

Log 0108 is the table. Do not invent types for rows the parquet lacks.

1 km in-situ crops for `/symbols/` (600 dpi, Map5View-all, centred on the hit):

```
$QPY tools/find_symbol_sheets.py --in-situ-dir site/public/symbols --theme Map5View-all
uv run python tools/export_symbol_table.py
```

