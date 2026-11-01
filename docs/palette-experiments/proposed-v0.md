# Palette experiment v0

A first, deliberately small set of colour changes, tested with the same tool
and pair names as the LINZ baseline so before/after is comparable.

**This is not a style yet.** It's a test of whether the problems in W1–W8
can be fixed by colour/lightness alone, or need pattern and shape.

## Candidate values

| Element | LINZ `topographic-v2` | v0 candidate | Rationale |
|---|---|---|---|
| Index contour | `rgba(206,103,6,0.75)` 0.4–0.6 px | `#8A4F1C` solid | Darker brown: lightness separates it from orange highways (F-18, F-20) |
| Intermediate contour | same as index | `#A8703C` solid | Keeps index/intermediate hierarchy while ≥3:1 on white |
| Water labels | `#008CCC` italic | `#005C8F` **upright** | ≥4.5:1 text (F-20); no italics (F-05) |
| Scrub | `#C7E4B7` | `#A3CC90` | Bigger lightness step… |
| Scattered scrub | `#CCDEC3` | `#E0EDD8` **+ stipple** | …plus a pattern, because lightness alone is still <1.5:1 in greyscale |
| Closed track | red 40% shadow | dark casing **+ cross-bar pattern** | Encode in shape, not red hue (F-03, F-21) |
| Historic site | red `#CB0C0C` label | dark ink label + distinct symbol | Red text drops to 1.62:1 against paper under red light |

## Before → after (key rows)

| Pair | Baseline worst-case | v0 worst-case | Verdict |
|---|---|---|---|
| Contour vs white | grey 2.66, red-light 1.39 | grey 6.53, red-light 3.45 | **Fixed** by colour |
| Contour vs highway | ΔE ≈5.8–6.8, grey 1.29 | ΔE ≥30.7, grey 3.15 | **Fixed** by colour |
| Contour vs pipeline | tritan ΔE 3.8 | tritan ΔE 27.5 | **Fixed** by colour |
| Scrub vs scattered scrub | ΔE 3.6 (tritan), grey 1.03 | ΔE ≥13.4, grey 1.49 | **Improved**; still needs pattern for greyscale |
| Scrub vs water | tritan ΔE 8.4, grey 1.04 | tritan ΔE 8.6, grey 1.26 | **Not fixed** by colour — rely on shoreline line + context |
| Water label contrast | 3.25–3.73:1 | 6.24:1 | **Fixed** |
| Historic label vs paper (red light) | 1.62 | 9.00 | **Fixed** by changing ink, moving meaning to symbol |
| Closed vs open track | grey 1.72, red-light 1.10 | pattern-based | **Fixed** by shape |

Full generated tables: [audit-proposed-v0.md](audit-proposed-v0.md).

## What this tells us

1. **Lightness is the robust channel.** Every fix that worked under greyscale
   and red light did so by changing lightness, not hue.
2. **Pale fills can't be fixed by colour alone.** Water vs scrub vs scattered
   scrub all sit in a narrow light band (they must, so that linework on top
   stays legible). Patterns and edge lines have to carry part of the meaning.
3. **Darker contours have a cost not measured here** — visual weight. Dark
   contours on steep NZ terrain (e.g. 20 m interval on 45° slopes is a line
   every ~0.4 mm at 1:50k) could swamp tracks and labels. Needs rendering
   tests on real sheets (OQ-09).
