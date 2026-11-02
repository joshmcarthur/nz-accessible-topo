# 0025 — Stock BX24 from LINZ's map container

**Date:** 2026-11-01

## Question
Can LINZ's `map` container render one stock Topo50 sheet, and where does the data come from (B-22, B-23)?

## What we did
Pinned `linz/topographic-system` @ `3b6ec60` (2026-10-15). Built `packages/map` into a local image tagged `map`. Ran `tools/render_sheet.sh BX24` against the public project item for `topographic-qgis` @ `c0edcfc`.

The map package release v0.9.0 (2026-03-26) is older than two weeks, but its CLI only reads a private S3 project. `3b6ec60` is the newest commit on or before 2026-10-18 that has `map prepare` and `map export` for the public STAC catalog (S-LINZ-TOPO-SYSTEM).

Colima was running at 2 GB RAM. It was restarted at 8 GB and 4 CPUs for the QGIS export. The base image is `linux/amd64`. This machine is arm64, so the container runs under emulation.

## What we found
The sheet renders. The map face is Christchurch, Lyttelton, and Pegasus Bay. The STAC item says `linz:mapsheet` `BX24`, bbox 172.55–172.85°E, 43.44–43.77°S.

Data path:

- Project: `https://d1jzh93b1t1cv.cloudfront.net/qgis/nztopo50/commit_prefix=c/commit=c0edcfc8c8b4321359cd9dbc2f66cd8d0e539a78/nztopo50.json`
- That item links 42 dataset collections. They are national GeoParquet, about 2.66 GB in total. Contours are 1.75 GB. The collections are CC-BY-4.0.
- `map export` downloads those files into a cache and QGIS clips them to the sheet. There is no per-sheet download.
- Cache and full export: `~/Projects/github.com/linz/topo50-bx24/` (outside this repo).
- The only print layout in the project is `tiff-50` (page 762 × 1066.8 mm). The README example `layout=nztopo50` is not in this project.
- Export dpi is 150. The full PNG is 4500×6300 px, 15 MB. The PDF is 17 MB.

Checksums (sha256) of the full export:

- PDF `4b4983b57d8df0f712845d52278165ffbab3a1fe83389bf8ccee222f9a8e81be`
- PNG `34f22292434307d4de60eee203c65a112eee8c189253d88807ef1dc0fdc7ed9d`

QGIS printed GDAL messages that field constraints were ignored. The PDF and PNG still wrote.

## What changed
- `tools/render_sheet.sh` runs prepare and export for one sheet.
- Review image `docs/visuals/08-bx24-stock.png` (long edge 2000 px). PDF `docs/visuals/08-bx24-stock.pdf` (17 MB, the 150 dpi export).
- The 15 MB full PNG stays in the local output directory.
- B-22 and B-23 moved to Done.

## Confidence & gaps
- One sheet, one dpi, one machine. A 600 dpi export was not run.
- The container is amd64 on an arm64 host. A native image would be faster. This run completed.
- Repeat the render with `tools/render_sheet.sh BX24`. The cache makes the second prepare skip completed downloads.
- The PNG is the full `tiff-50` page. The legend, the sheet index, and the title block are in the same image as the map. A later change is judged on the map layer, not on that page.
