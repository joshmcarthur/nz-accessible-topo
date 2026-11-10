# Findings: line and symbol size

## F-31 — Print lines and symbols have practitioner size floors, not a WCAG millimetre
WCAG 1.4.11 (F-20) sets contrast for graphics. It does not set a stroke
width. Print size floors come from cartographic practice.

**Conversion:** 1 pt = 1/72 in ≈ **0.35 mm**.

**Esri (print, 2008).** Type on a printed map should not be smaller than
5 pt. Symbol minimum sizes are about two thirds of the recommended text
size. For the 6 pt print floor in F-09, that is about **4 pt ≈ 1.4 mm**.
The same note uses a 2-minute visual angle as a conservative "can be seen"
threshold. At a 300 mm reading distance that angle is about **0.17 mm**.
The blog has no millimetre table for line width. It is about seeing a mark,
not about reading a thin line in a contour mesh.
**Sources:** S-ESRI-MINSIZE (C).

**Minnesota map-design guide.** Labels: 6 pt minimum, 8 pt preferred
(already F-09). Same-colour line weights should differ by at least 1 pt.
The worked example is **3 pt / 2 pt / 1 pt** (about 1.06 / 0.71 / 0.35 mm).
A 0.5 pt step is allowed only if the thinner line is about 20% lighter.
Keep line styles to six or fewer. Scale point symbols in 2× size steps.
The guide does not prove a laboratory minimum. It treats **1 pt (0.35 mm)**
as the thin end of a same-colour line family.
**Sources:** S-MN-MAPGUIDE (C).

**USGS US Topo (1:24,000), not 1:50,000.** These are product specs for
standard-vision maps, not a low-vision floor. StreamRiver perennial and
intermittent strokes are **0.80–1.00 pt (0.28–0.35 mm)**. Index contours
are **0.504 pt (0.18 mm)**. Intermediate contours are **0.216 pt (0.08 mm)**.
Paper millimetres do not double when scale halves. Use the millimetre
figures as a same-paper check, not as a scale-up.
**Sources:** S-USGS-SPECS (C).

**This sheet today (BX24, millimetres on paper).**

| Mark | Width or size | In points | Against the floors |
|---|---|---|---|
| Stock stream | 0.10 mm | 0.28 pt | Below USGS stream stroke and MN 1 pt |
| Accessible river and canal (log 0071) | 0.25 mm | 0.71 pt | Above the 0.17 mm visual angle. Under the USGS stream stroke |
| Accessible drain (log 0071) | 0.15 mm | 0.43 pt | One MN 1 pt step thinner would be 0 mm, so the step is smaller |
| Index contour | 0.35 mm | 1.0 pt | Matches MN 1 pt |
| Intermediate contour fill | 0.12 mm | 0.34 pt | USGS-thin; stays recessive (OQ-09) |
| Scrub plant `third_arc` | 1.4 mm | 4.0 pt | Matches Esri 2/3 of 6 pt |
| Closed-track × | 0.5 mm | 1.4 pt | Line-on-line mark, not an area symbol. G1 locked |

**Implication:** A single line floor does not work on this sheet (log 0071).
One 0.35 mm width on every blue line made drains, pond rims and coastline
look like rivers. MN treats 1 pt as the thin end of a family, so each class
needs its own step. Rivers are 0.25 mm and drains 0.15 mm. Polygon outlines,
coastline, shelterbelt, and grid keep stock widths in the darker inks. Scrub
marks use the ~1.4 mm symbol size. Do not copy USGS contour millimetres as a
low-vision floor.

**Grade:** C (practitioner guidance).

## F-32 — Reduced acuity removes fine detail first, and a filter can show it
The WHO grades distance vision by presenting acuity. Mild impairment is
worse than 6/12 and no worse than 6/18. An eye at 6/18 resolves detail of
3 arc minutes, three times the 1 arc minute of 6/6. At a 400 mm reading
distance that is about **0.35 mm** on the sheet. The same loss comes to a
reader with good distance vision who reads a map without reading glasses,
or in poor light.

Xiong and others (2021) simulated low vision for normally sighted readers
with an image filter. The filter moves the normal contrast sensitivity
curve along spatial frequency by the acuity loss, and down by the contrast
sensitivity loss. Measured acuity through the filter was within 0.05 logMAR
of the target (median, 36 readers, 40 conditions). Reading acuity and
critical print size matched real low-vision readers. So acuity loss acts as
a loss of high spatial frequencies, and a filter on the image is a fair
stand-in.
**Sources:** S-WHO-ICD11-VISION (C), S-XIONG-2021 (B).

**Our model.** The symbol test tiles use a simpler filter: a Gaussian blur
in linear light, as wide (full width at half maximum) as the 3 arc minute
detail, which is 8.2 px at 600 dpi (sigma 3.5 px). It has no contrast
sensitivity term. It is not the validated filter.
**Sources:** S-XIONG-2021 (B) for the principle only.

**Implication:** a mark thinner than about 0.35 mm keeps its place on the
sheet but loses its contrast for this reader. That is the same figure as
the 1 pt line floor in F-31. Thin strokes (the hot spring cross, relief
ticks, pattern fills, the spot-height dot) are the first to go.

**Grade:** B for the principle, D for our blur model.
