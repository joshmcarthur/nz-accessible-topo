# 0049 — Same-hue road lightness cannot close R-04 without a new choice

**Date:** 2026-11-03

## Question

Can a lightness change of the painted road inks meet R-04 ΔE ≥10 against both contour browns, while staying in the same hue (R-02)?

## What we did

Kept CIELAB a* and b* of PMS151 `#FF7F00` and of highway `#E31A1C`. Swept L* from 20 to 88. Scored each candidate against index `#8A4F1C` and intermediate `#C4814B` with `palette_audit.py`. No layer was patched. No square was redrawn.

## What we found

PMS151 at L* 82–88 (`#FFA83B` to `#FFB94C`) meets ΔE ≥10 against both contour browns. Those fills are paler than stock orange. Grey vs paper is about 1.7–1.9. Red-light vs paper is 1.0. The dark casing would still carry the line under red light. Dark maroon at L* 20–24 also meets the ΔE bar. That is not orange.

Highway `#E31A1C` has **no** L* that meets ΔE ≥10 against both contour browns. Index versus that red is protan ΔE 0.9 at the painted value.

The plan says: do not invent a new orange; start from PMS151; if a same-hue orange cannot meet the bar, leave R-04 open and stop. Highway has no same-hue solution. Road has only a paler orange or a non-orange dark. Picking either is a new choice.

## What changed

- This log.
- Lore question on painted R-04 pairs.

## Confidence & gaps

R-04 stays open. Road and highway fills stay unowned. Contour fills stay `#8A4F1C` / `#C4814B`.
