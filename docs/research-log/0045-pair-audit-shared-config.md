# 0045 — Pair audit reads the shared config

**Date:** 2026-11-02

## Question

Can the pair audit read colours from `tools/style-topo50.json` so a style change cannot drift from the gate?

## What we did

Pair files keep names, floors, and why. A colour that lives in `tools/style-topo50.json` is a dotted path. `palette_audit.py` resolves that path before it measures. Closed-track casing also names `tracks.closed_foot.casing_alpha`.

Literal hex stays for paper and for LINZ inks the style file does not own. Historic label ink stays `rgb(145, 0, 0)`: it is a darkened result, not a configured colour.

`check.py` C6 still reads `tools/pairs-accessible-v0.json`. It resolves those pairs first. C6 does not read `pairs-topo50-accessible.json`. C6 does not fail against `#EA6300`.

`font_check.py` on the patched TTF reports all ten macron vowels and the combining macron.

The four squares were drawn again at 600 dpi. The estuary square shows `Estuary of` and `and Avon` as blue letters. It has no black question marks. Hillshade stayed off: no `dem.tif`.

## What we found

C1–C6 pass. Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

R-14 Met when is true. Pair colours that live in the style file come from that file. New ❌ rows still fail C6.

## What changed

- `tools/palette_audit.py` resolves dotted colour paths from the style file.
- `tools/pairs-accessible-v0.json` and `tools/pairs-topo50-accessible.json` use those paths.
- `tools/check.py` C6 resolves pairs before it measures.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

Paper and LINZ highway, pipeline, and water fills stay as hex. A later step that puts those inks in the style file can switch those paths. The next step is R-13.
