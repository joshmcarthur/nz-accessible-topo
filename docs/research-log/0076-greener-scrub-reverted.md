# 0076 — A greener scrub fill breaks the vector pair (reverted)

**Date:** 2026-11-05

## Question

Log 0071 left the raster scrub cue weak. The fill `#A3CC90` at alpha 26
composites to `#F6FAF4`, ΔE 4.2 from paper. Can a greener fill keep the
index contour ≥3:1 in red light (B-34)?

## What we did

Red light reads only the red channel, so the fill can gain green and lose
blue with red held. Tried `#D6FFAA` at alpha 55. On paper that is
`#F4FFEC`: ΔE about 10 from paper (stock 11.6), 4.5 from native (stock
2.2). Index on scrub was 4.48:1 grey and 3.04:1 red. The raster grid read
green again on `1576000-5174000`.

Committed as `10aac35`, then reverted in `8ef78f0`.

## What we found

The gate run after the commit failed C1 and C6. `build_style.py` paints
`vegetation.scrub.colour` opaque in the vector style. One colour drives two
looks:

- raster: colour at `vegetation.scrub.alpha` over paper
- vector: the same colour at full opacity

`#D6FFAA` opaque is lime. The C6 pair "Scrub vs scattered scrub" uses the
opaque colour and failed: ΔE 8.3, grey 1.09, red 1.10.

## What changed

Nothing in the style. This log records the constraint.

## Confidence & gaps

A raster scrub change needs one of these first:

1. The vector build applies `vegetation.scrub.alpha`, so both media paint
   the same composited ink. The C6 pair must then use alpha too.
2. A separate raster tint in the style file. This splits the palette
   (end state 3 forbids a second palette).

Option 1 keeps one palette. It is a vector change, so it waits for a pass
that owns the vector build. B-34 stays open.

Process note: the commit went out before the gate output was read. Gates
now run before staging.
