# 0064 — Smaller, sparser closed-track ×

**Date:** 2026-11-05

## Question

Can a smaller × at a longer interval still mark a closed foot track, without dominating dense track areas on the 4 km grid?

## What we did

Log 0063 put a 1 mm `cross2` in every dash gap (interval 1.5 mm). Grid review G1 on Evans Pass, Godley Head, and Breeze Bay still read as a zipper.

Josh chose a smaller and sparser mark: size 0.5 mm, interval 4.5 mm. That is every third gap of the `1;0.5` dash. The first mark still sits in a gap (offset 1.25 mm). Outline width is 0.1 mm so the glyph does not fill in. The dash and the line weight stay the same as an open foot track.

`closed_bar_placement` reads `tracks.closed_foot.marker_interval_mm`. It no longer forces one mark per gap.

Applied the style onto `squares/accessible/nztopo50.qgs`. Redrew the closed-track square and the 4 km accessible face.

## What we found

A 1 mm × every 1.5 mm dominates where closed tracks are dense. A 4 mm interval looked open on a sparse square (log 0056). 4.5 mm is three dash cycles, not a return to a sleeper bar.

G1 stays open until the new cells are reviewed.

## What changed

- `tools/style-topo50.json`: `crossbar_size_mm` 0.5, `marker_interval_mm` 4.5, `crossbar_outline_width_mm` 0.1.
- `closed_bar_placement` uses that interval.
- This log. B-30 stays on review.

## Confidence & gaps

The vector sprite is still a denser mark. A steep sheet is not in this grid. Review G1 on `1580000-5170000` and `1572000-5170000`.
