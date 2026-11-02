# 0042 — Reserved track-access channel

**Date:** 2026-11-02

## Question

Is a casing/colour channel left unused so track access status can be added later without a redesign?

## What we did

R-11 already encodes closed tracks with cross-bars. Closed is not access. Access (public/private, DOC, walkway) is not in the Topo50 layers (F-25).

`tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false. Those values live in `tools/style-topo50.json`. The QGIS apply step does not paint access. The vector build does not paint access. No access ink was added.

The four squares were drawn again at 600 dpi. The closed-track square still shows the heavier dashed line and the cross-bars. Access is not drawn.

## What we found

The Met when text is now true. The reserved channel is unused. R-12 is met. It stays provisional: access data is still missing.

## What changed

- `tools/style-topo50.json` holds `tracks.access`.
- `tools/build_style.py` reads those values and refuses to paint access.
- `tools/override_topo50_project.py` refuses to paint access.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

A later step that paints access is a new choice. It needs an access attribute or an overlay source. The next step is R-03.
