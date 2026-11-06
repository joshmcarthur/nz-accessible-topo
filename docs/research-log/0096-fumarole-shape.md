# 0096 — Fumarole shape proposal (not applied)

**Date:** 2026-11-06

## Question

Josh: fumarole must "use a different shape". Hot spring is a black × (`springs.hot`). What dark shape can a fumarole use that does not match another `/symbols/` glyph?

## Proposal (for Josh)

Do not apply this yet.

### Shape

Three short vertical steam ticks over a filled oval vent. Black. About 1.6 mm tall. Stroke 0.2 mm. The ticks sit above a small filled oval (the vent).

### Why this shape

- Hot spring is a black ×. A larger × would differ by size only. Josh rejected that.
- Geothermal bore is a circled ×. Keep that glyph. Darken it later. Do not reuse it here.
- Cold spring is a `#005C8F` circle. A circle with ticks would still read as a spring.
- Cave is a dome on a baseline. Trig is a filled triangle. Mast is a tall open triangle. Bivouac is now an open tent with a ridge. Locked gate is a bar with a square. None of those is steam over a vent.
- Meaning: a fumarole vents steam. The ticks carry that. The × carries "hot" for the spring.

### Size and ink

- Mark 1.6 mm (above the 1.4 mm floor).
- Stroke 0.2 mm (above the 0.15 mm floor).
- Ink `#000000` (21:1 on paper, 21:1 under red light).

### What this is not

- Not a six-point star or asterisk. Those collapse to a × at 1.6 mm.
- Not a diamond. That can read as the locked-gate square, rotated.
- Not a second × at a different size.

### Apply later

`landcover_point` holds fumarole. Map5View hides that layer (N-5). Even after Josh accepts the shape, the sheet will not draw it until that layer is on.

## What we did not change

No QGIS patch. No style-file key. No SVG. The `/symbols/` row now points here and waits for review.
