# 0027 — One style file for the accessible rules

**Date:** 2026-11-02

## Question

Where do colour, type size, font family, and symbol rules for the accessible Topo50 style live?

## What we did

Copied the current values from `tools/override_topo50_project.py` into `tools/style-topo50.json`. Pointed that script at the file. Left `tools/build_style.py` on its own palette.

## What we found

The style file has no sheet code. The apply script still writes the same inks and the same size floors. The vector style still keeps a second palette in `tools/build_style.py`.

The file records two inks the apply step does not paint. The project road ink is `#D5B43C`. The print-legend highway is `#EA6300`.

The raster family in the file is `NZAT Legible Test`. The vector family in the file is Open Sans. The vector build does not read the file yet.

## What changed

- `tools/style-topo50.json` holds the rules.
- `tools/override_topo50_project.py` reads that file.
- `docs/style-topo50.md` says how to apply the file.
- `tools/test_tools.py` checks the file for a sheet code and checks that the apply step reads the settled inks.

## Confidence & gaps

The vector build is a later step. The along-line question marks are still a render defect. They do not change this file. R-09 is the next recommendation.
