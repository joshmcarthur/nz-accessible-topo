# 0069 — Print size floors for lines and symbols

**Date:** 2026-11-05

## Question

Is there a research millimetre for line and symbol thickness, or do we
have to trial widths on the sheet?

## What we did

Read Esri minimum-size guidance, the Minnesota map-design guide, and USGS
US Topo hydrography and elevation specs. Converted points to millimetres
(1 pt ≈ 0.35 mm). Compared those numbers to BX24 stock and accessible
widths. Did not paint.

## What we found

WCAG 1.4.11 (F-20) is contrast, not thickness. No laboratory millimetre
exists in these sources.

Practitioner floors:

- Print type ≥ 5–6 pt (already F-09).
- Esri: point-symbol size about 2/3 of that text → **~1.4 mm**.
- Esri 2-minute visual angle at 300 mm → **~0.17 mm** to *see* a mark.
- Minnesota: same-colour line family **3 / 2 / 1 pt** (1.06 / 0.71 / 0.35 mm).
  1 pt is the thin end of the example, not a lab proof.
- USGS US Topo 1:24k streams **0.80–1.00 pt (0.28–0.35 mm)**. Index contour
  0.18 mm, intermediate 0.08 mm. Those contour widths are standard-vision
  product specs, not a low-vision floor.

On this sheet, stock streams at 0.10 mm sit below both the visual-angle
check and the USGS stream stroke. Accessible `water_line` at 0.25 mm is
still under 1 pt. Index at 0.35 mm already matches 1 pt. Scrub plants at
1.2 mm sit just under the Esri symbol size.

Recorded as **F-31**. Candidate trial, not painted: **0.35 mm** line floor
for named classes that must be read; **~1.4 mm** for area point-pattern
marks.

## What changed

- `docs/findings/size-and-weight.md` (F-31)
- `docs/sources.md` URLs for S-ESRI-MINSIZE, S-MN-MAPGUIDE, S-USGS-SPECS
- `docs/README.md`
- This log

## Confidence & gaps

Grade C. USGS is a different scale and a different audience. Minnesota is
a state IT guide. Esri is a 2008 blog. A 4 km face trial still has to
confirm clutter on steep slopes (OQ-09).
