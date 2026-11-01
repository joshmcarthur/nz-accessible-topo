# Findings: relief shading and contours

## F-14 — Light from NNW reduces terrain-reversal errors compared with NW
The relief inversion (terrain reversal) effect makes valleys look like
ridges when shading is the main depth cue. A controlled study varying light
azimuth found NNW (337.5°), or even N, gave more accurate landform
perception than the conventional NW (315°); a replication with a different
population broadly confirmed it. The strongest illusion was at 225° (SW).
**Sources:** S-BILAND-2017 (B), S-COLTEKIN-2018 (B).
**Grade:** A– (original + replication).
**Topo50 today:** NW (S-LINZ-GUIDE).

## F-15 — NZ-specific twist: northern light is also physically realistic here
Cartographic NW lighting is a northern-hemisphere convention that happens to
be *unrealistic* for real sun (which is in the south there). In NZ, the sun
is in the north, so NNW/N lighting agrees both with the perceptual research
**and** with what users see on real slopes (sunny north faces). There is no
trade-off to make here.
**Sources:** reasoning from F-14 + basic solar geometry (D). Note research
suggests the "light from above" prior may be learned from indoor lighting
as much as the sun (S-COLTEKIN-2023), so this is a bonus, not the argument.

## F-16 — Multidirectional illumination mitigates inversion
A multidirectional "sky" illumination model reduced the relief inversion
illusion even when the dominant light came from the problematic SW.
**Sources:** S-MULTIDIR-2025 (B, conference abstract).
**Grade:** B– (abstract).
**Implication:** combine NNW primary light with soft multidirectional/sky
shading for robustness.

## F-17 — Shading interacts with colour and texture
Adding colour and texture to shaded relief changes 3D-shape identification;
greyscale shading had stronger contrast effects than colour. Overlaying land
cover on semi-transparent shading is a common mitigation.
**Sources:** S-COLTEKIN-2019 (B).
**Implication:** test shading under the final vegetation palette, not alone.

## F-18 — Contours are a graphical object that must be seen
LINZ's web contours are 0.4–0.6 px at 75% opacity, 2.66:1 against white
(W3). WCAG 1.4.11 expects 3:1 for graphics needed to understand content
(see `standards.md`). Contour accuracy is ±~10 m and worse in forest/snow
(S-LINZ-DD-CONTOUR) — a reason to keep *indefinite* contours visually
distinct (LINZ data carries a `definition = indefinite` attribute).
**Sources:** audit (D), S-W3C-1411 (C), S-LINZ-DD-CONTOUR (C).
