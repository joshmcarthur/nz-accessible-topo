# 0061 — Line-on-fill pairs and log 0060 classes

**Date:** 2026-11-04

## Question

Does the pair audit report every line-on-fill pair that R-01 now requires, and the stream, shelterbelt, and grid classes from log 0060?

## What we did

Named the unowned Map5View inks in `tools/style-topo50.json` `reference_inks`: stream `#009EFF`, shelterbelt `#94FF3B`, grid `#29A0D3`, urban fill `#BCBAB6`. The apply step does not paint those keys.

Added 19 pairs to `tools/pairs-topo50-accessible.json`: index contour, intermediate contour casing, stream, and track on scrub, native, water, and urban; plus stream, shelterbelt, and grid versus paper. Existing native-versus-scrub and scrub-versus-water pairs now carry vegetation fill alpha.

`resolve_colour_spec` treats a style-file alpha greater than 1 as a QGIS 0–255 byte. Vegetation fills stay `180` and `200` in the style file.

Ran `palette_audit.py - --pairs tools/pairs-topo50-accessible.json --config tools/style-topo50.json`. Each side still composites onto paper, then the audit measures the two results. That is the same method as logs 0058 and 0060. Paint did not change. C6 still reads `pairs-accessible-v0.json` only.

## What we found

New pairs that fail R-01 grey 3:1 or red 3:1, with no extra shape on the fill:

| Pair | Grey CR | Red CR |
|---|---:|---:|
| Index contour vs scrub | 2.91 | 1.63 |
| Index contour vs native forest | 3.93 | 2.72 |
| Index contour vs water | 3.61 | 2.15 |
| Index contour vs urban | 2.37 | 1.73 |
| Intermediate contour vs scrub | 1.41 | 1.06 |
| Intermediate contour vs native forest | 1.91 | 1.57 |
| Intermediate contour vs water | 1.75 | 1.24 |
| Intermediate contour vs urban | 1.15 | 1.01 |
| Stream vs scrub | 1.81 | 10.45 |
| Stream vs native forest | 2.45 | 17.43 |
| Stream vs water | 2.24 | 13.75 |
| Stream vs urban | 1.48 | 11.06 |
| Stream vs paper | 2.86 | 21.00 |
| Shelterbelt vs paper | 1.26 | 3.03 |
| Grid vs paper | 2.97 | 14.55 |

Index versus native and index versus water pass grey and fail red. Streams pass red and fail grey. Track versus each fill passes both (black, 10.84:1 or higher).

Stream versus paper is 2.86:1. That matches log 0060. It is not the grid ink. Grid versus paper is 2.97:1. Shelterbelt versus paper is 1.26:1. Index versus scrub from the style file is 2.91:1. Log 0058 measured painted pixels at 2.93:1.

R-01 stays open. No paint change. No grid re-review.

## What changed

- `tools/style-topo50.json` names stream, shelterbelt, grid, and urban fill.
- `tools/pairs-topo50-accessible.json` holds the line-on-fill pairs and the log 0060 classes.
- `resolve_colour_spec` maps a QGIS-byte alpha onto the 0–1 range.
- This log. B-40 is done.

## Confidence & gaps

The audit measures configured inks, not anti-aliased pixels on the face. Island, exotic, and vegetation-outline inks from log 0060 are still unnamed. C6 does not read this pair file. B-41 still needs a site matrix. B-35, B-34, and B-36 still need paint.
