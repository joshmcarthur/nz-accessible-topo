# 0098 — Tree point size and glyph

**Date:** 2026-11-06

## Question

N-2 drew `vegetation_point` trees at 1.4 mm with the LINZ filled disk. Dense
cells swamped into green blobs (log 0070). How do we show trees on the map without
breaking readability?

## What we did

Tried sub-legend map sizes with the LINZ `tree.svg` disk, then an owned Y-stroke
at **1.4 mm** (F-31). Blobs returned on **1568000-5166000**.

**Josh (glyph + map size):** use a **tree-like stroke glyph** at **0.2 mm** on
the map. Restore the **log 0070 exempt** for dense canopy points. Legend and
symbol proposal row stay at **1.4 mm**.

**Shape reference:** Mapbox Maki `park` icon (CC0 1.0). Owned file
`nztopo50_tree_stroke.svg` — trunk line plus rounded crown, no fill disk.

## What we found

1.4 mm on every point overlaps regardless of glyph if the data is dense. F-31
applies to the **legend swatch** and to symbols that read alone on the sheet.
Forest class still reads from **native/scrub polygons**.

## Confidence & gaps

Review dense and urban cells at **0.2 mm**. If still heavy, try **0.15 mm**. If
too faint, try **0.25 mm**. Adjust crown stroke in SVG before changing policy again.
