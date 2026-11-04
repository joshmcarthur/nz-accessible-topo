# Handoff: research sandbox → local development

State at handoff: logs 0001–0023, all gates green from a clean
clone. Next work is in [BACKLOG.md](BACKLOG.md).

> **Read log 0023 first.** The intended starting point is `topo-raster-gridded`
> (Topo50 raster), not `topographic-v2`. The primary path is now forking
> `linz/topographic-qgis` and rendering with `linz/topographic-system`'s map
> container (B-22, B-23 are the first steps; both need Docker locally).

## Get the repo

```sh
git clone nz-accessible-topo.bundle nz-accessible-topo
cd nz-accessible-topo
git log --oneline | head        # newest: backlog + handoff
```

## Set up (macOS)

```sh
uv sync --group site
source .venv/bin/activate
uv run playwright install chromium
(cd site && npm ci)
npm i --no-save @maplibre/maplibre-gl-style-spec@26.5.0   # style validator
```

Google Fonts files are needed only for `render_comparison.py` /
`font_check.py`: `git clone --depth 1 --filter=blob:none --sparse
https://github.com/google/fonts && cd fonts && git sparse-checkout set
ofl/opensans ofl/notosans ofl/atkinsonhyperlegiblenext ofl/roboto`.

## Everyday commands

| Task | Command |
|---|---|
| Rebuild styles from LINZ upstream | `python3 tools/build_style.py` |
| Style gates (C1–C6) | `python3 tools/check.py` |
| Package tests | `uv run pytest` |
| Lint | `uv run ruff check` |
| Site data (graph lint, tokens, comparison images) | `cd site && npm run data` |
| Site dev server | `cd site && npm run dev` |
| Site gates (axe WCAG 2.2, no italics, links) | `cd site && npm run build && npm run check` |
| Preview styles on live tiles | `python3 -m http.server 8000` → `localhost:8000/preview/` |
| Live-tile captures | `LINZ_API_KEY=… node tools/screenshots/compare.mjs` |

## Conventions to keep

- **One research-log entry per research commit** (`docs/research-log/NNNN-*.md`):
  question, what we did, what we found, what changed, confidence & gaps.
  Corrections are logged, not silently edited.
- **Generated files are never hand-edited**: `styles/*.json`,
  `docs/styles/*-changes.md`, `site/src/data/graph.json`, `tokens.css`,
  `site/src/data/ink-matrix.json`. CI
  fails if they drift.
- **Every finding cites a source; every recommendation rests on something**:
  `extract_graph.py` enforces this.
- **Pin dependencies to releases ≥2 weeks old.**
- **Verify from a clean clone before claiming done** (log 0022 explains why).

## Known traps

- `python3 -m http.server` started in a directory dies when Astro rebuilds
  `dist/`; use `--directory` with an absolute path.
- Pillow + variable fonts: Open Sans axes are `[Weight, Width]`; draw halo and
  text in separate layers (log 0017).
- `topo-legend-1.tif` is WEBP-compressed: needs `tifffile` + `imagecodecs`.
- `gl-style-validate` prints nothing on success; check the exit code.

## Where to look

| Need | File |
|---|---|
| What we believe and why | `docs/findings/`, `docs/recommendations.md`, `docs/sources.md` |
| What's unresolved | `docs/open-questions.md`, `BACKLOG.md` |
| How we got here | `docs/research-log/` (or the site's Research log) |
| Topo50 QGIS cartography (primary target) | `docs/current-state/topo50-qgis-cartography.md`, `tools/analyse_qgis_project.py` |
| Vector-track style parameters (secondary) | `tools/build_style.py` (`P = {...}`) |
| Site content sources | `site/README.md` |
