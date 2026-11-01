# 0004 — Audit LINZ's published web topographic style

**Date:** 2026-11-01

## Question
What does LINZ's current web topographic style actually do, measured rather
than eyeballed?

## What we did
- Read LINZ Basemaps docs on vector tile usage and styling. Learned the tiles
  use the Shortbread schema and that the style is public.
- Sparse-cloned `linz/basemaps-config` and audited
  `config/style/topographic-v2.json` at `581b44a`.
- Confirmed the repo is MIT-licensed (Crown copyright LINZ) — so we can fork
  the style as a starting point rather than writing one from scratch.
- Wrote `tools/pairs-linz-topographic-v2.json`: 11 colour pairs that a map
  reader needs to tell apart, each with a reason.
- Ran the audit; wrote `docs/current-state/linz-basemaps-topographic-v2.md`.

## What we found
See W1–W8 in the current-state doc. The most important:
- **Water labels** are uniformly below 4.5:1 and italic — both issues
  compound (see later typography findings).
- **Vegetation classes** that affect route choice are not separable for
  dichromats, and barely for anyone.
- **Contours** are thin, low contrast and share a hue with highways.
- **Closed tracks** rely on a faint shadow — a safety-relevant distinction
  carried by the weakest possible signal.

## What changed
- Added `docs/current-state/linz-basemaps-topographic-v2.md`
- Added generated `docs/current-state/audit-linz-topographic-v2.md`
- Added `tools/pairs-linz-topographic-v2.json`

## Confidence & gaps
- The audit only sees literal colours; data-driven expressions are skipped.
- A 0.5 px line on a 3x retina screen is not the same as on a 1x monitor;
  zoom-dependent widths need rendering tests (OQ-04).
- The print Topo50 may differ from this web style; we have not yet measured
  print colours (gap from log 0002 still open).
