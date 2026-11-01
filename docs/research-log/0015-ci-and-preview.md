# 0015 — CI gate and visual preview

**Date:** 2026-11-01

## Question
How do we stop accessibility regressing as the style evolves, and how does a
human actually look at the result?

## What we did
- `tools/check.py` — six gates: build is reproducible (C1), no italics (C2),
  all labels ≥4.5:1 except documented shield false positives (C3), primary
  light 337.5° (C4), only macron-verified families (C5), and per-pair floors
  from `tools/pairs-accessible-v0.json` (C6). Floors sit just under what v0
  achieves; pairs that colour can't solve have a 0 floor on that channel and
  name the pattern/line that carries them instead.
- `.github/workflows/check.yml` — runs sprites-reproducible check, `check.py`,
  MapLibre style validation (spec pinned 26.5.0), and the audit report.
- Confirmed Roboto (used for some labels) has all ten macron vowels.
- `preview/index.html` — synced side-by-side maps with in-browser CVD,
  greyscale and red-light simulation using the same Machado matrices
  (SVG filters operate in linearRGB, matching the audit tool).

## What we found
- **The gate earned its keep on first run:** C2 caught three layers still
  requesting italic faces (`Poi-Windmill`, `Waterway-Flume-Name`,
  `Poi-Showground-Symbol`). They had empty `text-field`s, so the build
  skipped them before de-italicising. Fixed by mapping fonts on every layer
  (the fix landed in the log-0014 build commit, as the gate was run before
  that commit was made).
  Harmless today, but MapLibre would still fetch italic glyph ranges, and a
  future upstream change filling those fields would have reintroduced italics.

## What changed
- `tools/check.py`, `tools/pairs-accessible-v0.json`,
  `.github/workflows/check.yml`, `requirements.txt`, `preview/`.

## Confidence & gaps
- The workflow hasn't run on GitHub yet (no remote). The preview hasn't run
  against live tiles. Both are first things to do after pushing.
