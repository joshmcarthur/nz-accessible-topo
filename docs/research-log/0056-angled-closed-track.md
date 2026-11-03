# 0056 — Angled closed-track bars

**Date:** 2026-11-03

## Question

Can a closed foot track stay as light as an open foot track, and still read as closed, without looking like a railway?

## What we did

Set `tracks.closed_foot.width_mm` to 0.15 and `closed_dash` to `1;0.5`. Those match the open foot track. Set `crossbar_angle_deg` to 60. Set `crossbar_size_mm` to 1, the same length as one dash. A second apply writes that angle and that size onto the marker that is already in the project.

Drew the closed-track square again at 600 dpi. The other three squares were not drawn.

## What we found

The closed line is the same weight as the open foot track. The bars sit at 60° to the line. Each bar is 1 mm, the same length as one dash. The brown contours show through the track. The vector sprite is still a perpendicular bar.

## What changed

- `tools/style-topo50.json` line weight, dash, bar angle, and bar length.
- `tools/override_topo50_project.py` updates an existing closed-track marker.
- `docs/visuals/squares/closed-foot-track-accessible.png`.

## Confidence & gaps

The web sprite does not use this angle. If 60° still reads as a sleeper, try another angle in the style file and draw this square again.
