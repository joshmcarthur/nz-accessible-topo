# 0046 — Variant inks are not named

**Date:** 2026-11-02

## Question

Can this loop publish a greyscale-safe print variant and a high-contrast web variant from the shared style file?

## What we did

R-13 asks for three products from one source: full colour, greyscale-safe print, and a high-contrast web variant. The dispatch, the recommendations, and lore do not name those inks. R-13 has no Met when text.

No palettes were added. `tools/style-topo50.json` was not changed. The QGIS project was not rebuilt. The squares were not redrawn.

The main style stays the full-colour product. The site grey condition stays a simulation of that product. R-01 already requires greyscale or shape on the main style.

## What we found

R-13 stays open. A later step that paints the other two products must name the inks first.

## What changed

- This log.
- The backlog status.
- The style-loop status file.

## Confidence & gaps

B-14 stays later. The next step is R-15.
