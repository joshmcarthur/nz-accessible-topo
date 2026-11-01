# 0021 — Site scaffold: evidence Sankey and "how people see maps"

**Date:** 2026-11-01

## Question
How do we present the reasoning and working publicly, in a way that stays
true to the docs and meets the standards the project argues for?

## What we did
- **Made the evidence chain machine-readable.** `tools/extract_graph.py`
  parses sources, findings, recommendations and the style change log into
  `site/src/data/graph.json`, and **lints** the chain: every finding must cite
  a source; every recommendation must rest on something.
- **Fixed what the lint found.** F-22, F-26 and F-29 cited no source;
  R-13 – R-16 had no "Rests on" line. Our own measurements are now
  first-class, graded-D sources (`S-OUR-*` in `sources.md`). R-04's title
  updated to match the log-0020 revision.
- **Theme shared with the map.** `tools/export_tokens.py` derives CSS tokens
  from `build_style.py`'s parameters, including a one-hue evidence-grade ramp
  (lightness only, each step ≥3:1 on paper), and refuses to write tokens that
  fail contrast.
- **Astro site** (`site/`, Astro 7.3.8 pinned — the newest release was four
  days old, so we took one >2 weeks old). Pages: overview with Sankey, how
  people see maps, evidence trail tables, a page per finding and
  recommendation, and the research log read straight from `docs/`.
- **Sankey** rendered at build time to SVG (d3-sankey): works without JS,
  every node a focusable link; a small script traces a node's full chain on
  hover/focus. Columns fixed by kind; d3's ordering relaxation instead of
  alphabetical order removed most crossings.
- **Comparisons** are manifest-driven (`comparisons.json`, `conditions.json`),
  pre-rendered by `tools/build_site_assets.py` with the audit's own models.
  Switching is CSS-only (`:has()` + radios); selection is shown by fill
  **and** a check mark. Legend crops are defined in the manifest and cut from
  LINZ's original TIFF.
- **The site checks itself.** `tools/check_site.py` runs axe-core (WCAG 2.2
  A/AA + best practice) and an italics scan over every page. First run: two
  content issues (a skipped heading level in an embedded snippet; an empty
  table header in log 0014) — both fixed. Now 70 pages, zero violations.
  Added as a CI job.

## Design decisions (and why)
- Real IDs (S-, F-, R-) are the visible labels: they're how the docs, commits
  and site cross-reference each other.
- The Topo50 1 km grid appears faintly in the page margins — the one motif
  every NZ map reader recognises — and never behind text.
- A Sankey is itself a colour-heavy graphic, so grades use one hue with
  lightness steps, the grade letter is always printed, and the same data is
  in tables.

## What the Sankey shows that the docs didn't
Tracing R-04 (contours) shows it rests mostly on our own measurements plus
WCAG and LINZ's data dictionary — grade C/D. That's visible at a glance now,
and is why R-04 is a priority for user testing (R-16).

## Gaps
See `site/README.md`: log-internal links, dark theme, replication in grades.
