# 0003 — Build a reproducible palette audit tool

**Date:** 2026-11-01

## Question
How do we measure accessibility of a map style in a way others can re-run,
rather than eyeballing it?

## What we did
- Wrote `tools/palette_audit.py` (numpy only).
- CVD simulation: Machado, Oliveira & Fernandes (2009) matrices, severity 1.0,
  applied in linear sRGB. Chosen because it is the physiologically-based model
  used by most modern simulators and handles all three dichromacies.
- Colour difference: CIEDE2000. Verified against Sharma, Wu & Dalal (2005)
  test data (pair 1 → 2.0425, pair 3 → 1.0000; both matched exactly).
- Contrast: WCAG 2.x relative-luminance ratio (verified black/white = 21:1).
- Added two non-standard conditions that matter in the field: greyscale
  (photocopies, mono laser print, e-ink GPS units) and narrow-band red light.

## Decisions
- Flag thresholds (ΔE <5 ❌, 5–10 ⚠️) are a **working assumption**. Small map
  symbols need larger ΔE than large patches; published "just noticeable
  difference" values (~1–2.3) are for large side-by-side patches and are too
  optimistic for 0.5 px lines. Logged as OQ-03.

## What changed
- `tools/palette_audit.py`, `tools/README.md`

## Confidence & gaps
- Maths: high (verified). Perceptual interpretation: low until user-tested.
