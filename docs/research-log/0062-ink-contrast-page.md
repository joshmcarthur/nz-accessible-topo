# 0062 — Site ink contrast matrix

**Date:** 2026-11-04

## Question

Does the site show every pair in the Topo50 pair file, including leftover Map5View inks that log 0060 named and log 0061 left unnamed?

## What we did

Named the leftover inks in `tools/style-topo50.json`: island outline `#0083BB`, exotic fill `#A4D65E` at 0.2, vegetation outline `#A7C05E`. Added pairs for those classes versus paper, index and intermediate contour versus stream, and shelterbelt versus native forest.

Wrote `tools/export_ink_matrix.py`. It reads `tools/pairs-topo50-accessible.json` through `resolve_pairs` and `pair_audit`. It writes `site/src/data/ink-matrix.json`. The `/inks/` page sorts fail rows first. Each row shows a line-on-fill swatch, Grey CR, Red CR, Normal ΔE, worst CVD ΔE, and Pass or Fail as a word plus a mark. CI diffs that JSON. `npm run data` regenerates it.

No new vision model. The pair file is the list. The matrix is not a Cartesian N×N of every hex.

## What we found

The exporter reports 51 pairs. Before the paint pass in log 0063, 39 pairs failed R-01 grey 3:1 or red 3:1. Stream versus paper still failed Grey CR. Island outline versus paper already passed (4.23:1 grey). Exotic fill and vegetation outline versus paper failed, as log 0060 measured.

The page is the checklist for the paint pass. C6 still reads `pairs-accessible-v0.json` only.

## What changed

- `tools/style-topo50.json` names island outline, exotic fill, and vegetation outline.
- `tools/pairs-topo50-accessible.json` holds those pairs plus contour versus stream and shelterbelt versus native.
- `src/nzat/site/export_ink_matrix.py` writes the site table.
- `site/src/pages/inks.astro` shows the table. Nav links to `/inks/`.
- This log. B-41 is done.

## Confidence & gaps

The matrix measures configured inks, not anti-aliased pixels on the face. Paint had not yet closed stream, scrub, shelterbelt, or grid. That is log 0063. R-01 stays open.
