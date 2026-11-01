# Findings: colour vision

## F-01 — Colour-vision deficiency is common enough to be a primary design constraint
About 8% of men have a colour vision impairment (mostly red–green); those
affected are slower and less successful at map tasks that depend on colour,
and make considerably more colour-identification errors under reduced
illumination. Rarer forms affect under ~0.3% of people.
**Sources:** S-JENNY-KELSO-2007 (B/C; reviews Birch 1993 and Cole 2004).
**Grade:** A (prevalence is long-established); B for the map-task effects.

## F-02 — Colour vision degrades with age, mostly on the blue–yellow axis
In a random sample of 865 adults aged 58–102 with no congenital deficiency,
abnormal colour vision rose steeply with age, and most errors were
blue–yellow (pastel blue vs purple, yellow vs green/yellow-green). Common
age-related eye diseases produce blue–yellow anomalies early. Older
observers' tritan-like errors resemble those of younger people tested under
**dim light**, linking ageing and low-light performance.
**Sources:** S-SCHNECK-2014 (B; reported via news summaries — primary paper to
be read), S-KNOBLAUCH (B, as cited in S-BARBUR-REVIEW), S-WUERGER-2013 (B).
**Grade:** B.
**Map implication:** pale green vegetation vs pale blue water vs pale grey
scree/sand are exactly the confusions this population is prone to.

## F-03 — Colour-only distinctions fail; use redundant visual variables
The cartographic recommendation is to design for colour-impaired readers by
(a) choosing colours that remain distinct under simulation and (b) adding
non-colour cues — pattern, line style, shape, size, lightness.
**Sources:** S-JENNY-KELSO-2007.
**Grade:** C (professional guidance grounded in B-grade evidence).

## F-04 — The current LINZ web style has measurable CVD weak points
From our audit (W4–W7): scrub vs scattered scrub (ΔE <5 for all dichromats),
contour vs highway (ΔE ≈6 for everyone), contour vs pipeline (tritan ΔE
3.8), and closed-track status carried by a faint shadow.
**Sources:** our audit (D).
**Grade:** D (model output; needs user validation).

## Notes on what is *not* a problem
- Hot vs cold spring and historic-site red vs hut black remain distinct under
  all three simulated dichromacies (ΔE >20). The classic "red vs green" fear
  does not apply to every red in the style; measure before changing.
