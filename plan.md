# Plan

## Objective

Render Topo50 sheet BX24 with LINZ's map container, then change QML labels and symbology and render that sheet again. Leave the Nimbus Sans LINZ files unchanged. The accessible sheet uses Atkinson Hyperlegible Next with Ō/ō added.

## Scope

In scope: B-28, B-22, B-23, B-25, B-24.

Out of scope: B-01, B-02, B-03, B-26, B-29, tile serving, and site work beyond the evidence-graph refresh that a recommendation edit requires. B-11 is in scope: it is the Atkinson swap on the accessible sheet.

## Approach

Use the pinned STAC project for topographic-qgis @ c0edcfc:

https://d1jzh93b1t1cv.cloudfront.net/qgis/nztopo50/commit_prefix=c/commit=c0edcfc8c8b4321359cd9dbc2f66cd8d0e539a78/nztopo50.json

Clone linz/topographic-system outside this repo, record the commit, and build packages/map with its container script. Start Colima first. Mount the cache on the host.

map prepare and map export download the national GeoParquet layers the project links. QGIS clips to BX24 at export. The cache, the upstream checkouts, and full-resolution exports stay out of git. Commit a review PNG. Commit the PDF when it is under 20 MB.

B-25, B-11, and B-24 are QML transforms on a pinned checkout, then map deploy, then the same container. Italic style names map to upright faces of Atkinson Hyperlegible Next. The face is built at render time by tools/patch_atkinson_omacron.py from the OFL sources. The family name is NZAT Legible Test. There is no Narrow master, so stock Narrow labels use the regular width. The size floor is 7 pt, and 6 pt for spot heights. Symbology follows R-04, R-10, R-11, and R-17. Colours go through palette_audit.py in pair mode.

## Next steps

1. Log the B-28 decision. Stop for commit.
2. Stock BX24 render (B-22, B-23). Stop for commit.
3. Upright labels, size floor, and the Atkinson swap (B-25, B-11). Stop for commit.
4. Symbology (B-24). Stop for commit.

## Constraints

Free disk was about 38 GB when this plan was approved, and Colima was stopped. Stop a render if free space would fall below 8 GB. The national contour parquet is 1.75 GB. BX24 is the print-legend sheet and is flat. A steep sheet is later work (OQ-09).
