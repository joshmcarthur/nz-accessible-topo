# 0080 — Patched Atkinson Bold for town names

**Date:** 2026-11-05

## Question

Log 0079 found two cues that need a Bold face. Josh approved the download.
Where should Bold go?

## What we did

Downloaded `fonts/ttf/AtkinsonHyperlegibleNext-Bold.ttf` (66,792 bytes,
sha256 `994414047df66bb4998d01c1cb1eeb4a2ddc4622d1aa56bbb8adbeca7645b041`)
from `googlefonts/atkinson-hyperlegible-next` at `7925f50`, the commit the
licence finding names. Patched it with `tools/patch_atkinson_omacron.py`
into `NZATLegibleTest-Bold.ttf`. `font_check.py` reports all ten macron
vowels and U+0304. QGIS lists the family styles as Bold and Regular. The
file stays outside the repo, beside the Regular face.

The label style rule now sends a stock style that contains bold to Bold.
Rendered the grid twice: italic as Bold, then italic as Regular.

## What we found

| Italic maps to | New collisions > 2000 m² | Look |
|---|---|---|
| Bold | 130 | Spot heights and blue water names heavy |
| Regular | 125 | Same as log 0077, town names Bold |

CHRISTCHURCH, Belfast, Sumner, Lyttelton, and Diamond Harbour draw Bold
again. Brown already marks natural names (log 0072). Bold on every italic
label (spot heights, water names, natural names) added weight and
collisions without a new cue.

## What changed

- `fonts.raster_natural_style` is Regular. Bold styles map to Bold.
- The render loads the whole font folder.
- `docs/style-topo50.md`, B-32, tests.

## Confidence & gaps

Grade D. The vector style still uses Open Sans.
