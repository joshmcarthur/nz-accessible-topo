# Recommendations

Each recommendation lists the findings it rests on, the strongest evidence
grade behind it, and how we'll know it's met. **Provisional** = rests mainly
on grade C/D evidence or on transferring evidence from a different task.

Status: draft v0 (2026-11-01). Nothing here has been user-tested yet.

**Implementation status (log 0014):** R-03, R-04, R-05, R-07, R-08, R-09,
R-10, R-11 are implemented in `styles/accessible-v0*.json` and gated in CI
(R-14, R-15 done). R-06 met by keeping Open Sans/Roboto. R-01 enforced via
per-pair floors in `tools/pairs-accessible-v0.json`. Not started: R-12, R-13
(print + high-contrast variants), R-16 (user testing).

**Note on R-07 values:** the build darkens each failing label colour along
CIELAB L\* (hue kept) to 4.8:1 (4.5 + margin), so the shipped water-label
blue is `rgba(0,110,171)` rather than the hand-picked `#005C8F` in palette v0.

---

## Principles

### R-01 — Encode anything safety-relevant in lightness and shape; use hue only as a redundant cue
**Rests on:** F-01, F-02, F-03, F-21, F-22, F-23 · **Best evidence:** A/B
**Why:** CVD affects ~8% of men; ageing adds blue–yellow losses; dim light
and red headtorches remove hue information for everyone. Lightness and shape
survive all of these.
**Met when:** every pair in the must-distinguish list either reaches ≥3:1
luminance contrast in the greyscale model **or** differs in pattern/shape,
and the same holds in the red-light model.

### R-02 — Keep the familiar colour grammar; change values within it
**Rests on:** S-LINZ-GUIDE (C), F-24 · **Provisional**
**Why:** Blue = water, brown = relief, green = vegetation, black = culture is
an international convention that SAR teams, trampers and the Defence Force
are trained on. The audit shows most problems are *lightness* problems inside
that grammar, not wrong hues.
**Met when:** a Topo50 user can read the new style without consulting the
legend for the core classes. (Test, see R-16.)

---

## Terrain

### R-03 — Light relief shading from NNW (337.5°), with a soft multidirectional component
**Rests on:** F-14, F-15, F-16, F-17 · **Best evidence:** A–
**Change from today:** Topo50 uses NW (315°).
**Why:** Replicated studies show fewer terrain-reversal errors with NNW than
NW. In the southern hemisphere this is also where the real sun is.
**Met when:** shaded relief generated at 337.5°, blended with a
multidirectional/sky layer; evaluated on both Alpine and lowland sheets.

### R-04 — Darker, solid, wider contours with a clear index/intermediate hierarchy
**Rests on:** F-18, F-20, W3, W5, W6, palette v0 · **Best evidence:** C (WCAG) + D (audit)
**Starting values:** index `#8A4F1C`, intermediate `#C4814B` (revised in log
0020 from `#A8703C`: real Topo50 slopes show 20 m intermediates are dense
enough that they must stay recessive — the lightest same-hue brown meeting
3.2:1, thinner lines; index contours carry relief under red light), no opacity.
Web widths: intermediate ≥1 px, index ≥1.5 px at z13+ (provisional).
Print widths: set by rendering tests on steep sheets (OQ-09).
**Also:** draw `definition = indefinite` contours dashed, so reduced
accuracy in forest/snow is visible.
**Met when:** contours ≥3:1 vs paper; ΔE ≥10 vs highways and pipelines
under all simulated dichromacies (palette v0 achieves this).

---

## Typography

### R-05 — No italics for map labels
**Rests on:** F-05, F-08 · **Best evidence:** B
**Change from today:** 33 of 63 web label layers are italic, including all
water names.
**Why:** Italic styles measurably slowed dyslexic readers; the italic-water
convention is a tradition, not a legibility finding. Carry "this is water"
with colour (≥4.5:1, R-07) and, if needed, a weight or tracking difference.
**Met when:** zero italic faces in the style.

### R-06 — Use a roman, humanist sans with a large x-height and complete macron coverage; do not use "dyslexia fonts"
**Rests on:** F-06, F-10, F-11, F-12 · **Best evidence:** A (dyslexia fonts don't help); measured (coverage)
**Now:** keep **Open Sans** (or **Noto Sans**, near-identical metrics,
broader coverage). Both have all ten macron vowels and x-height ≈0.535 em.
**Later:** adopt **Atkinson Hyperlegible Next** once Ō/ō exist in a build we
can make glyph PBFs from (F-26 – F-29). Preferred route: upstream PR adding
two composites (`docs/upstream/`). Interim route: our renamed OFL patch
(`tools/patch_atkinson_omacron.py`). It's designed to separate I/l/1 and O/0
(`docs/visuals/05`), which matters for grid references and trig IDs. Print
via a shaping renderer (QGIS) may work with the official font already (F-28).
**Met when:** `tools/font_check.py` reports full macron coverage for every
face in the style (hard gate, F-12).

### R-07 — All label text ≥4.5:1 against an opaque halo
**Rests on:** F-20, W1 · **Best evidence:** C
**Change:** water labels `#008CCC` → `#005C8F` (3.3:1 → 6.2:1); contour
labels and grey POI labels darkened; halos fully opaque.
**Met when:** the text-contrast table in the audit has no ⚠️/❌ rows (except
shield-on-icon false positives, documented).

### R-08 — Add modest positive letter-spacing, and allow long names to wrap — **provisional**
**Rests on:** F-07, F-13 · **Best evidence:** A– for continuous reading;
transfer to map labels unproven (OQ-06).
**Starting values:** +0.04–0.08 em tracking on point/area labels; halos
retained; `text-max-width` so hyphenated Māori names break at hyphens.
**Met when:** A/B tested with dyslexic readers on label-finding tasks.

### R-09 — Label size floor and hierarchy steps
**Rests on:** F-09 · **Best evidence:** C
**Values:** print ≥7 pt default, 6 pt absolute floor (spot heights only);
web ≥10 px (≥11 px for place names); adjacent hierarchy levels differ by
≥20%.

---

## Symbols and fills

### R-10 — Vegetation classes that affect travel get pattern as well as tint
**Rests on:** F-02, F-04, palette v0 · **Best evidence:** B + D
**Change:** scrub `#A3CC90`; scattered scrub `#E0EDD8` **plus stipple**.
Water keeps its blue shoreline line.
**Why:** v0 showed colour alone can't separate pale fills in greyscale.

### R-11 — Closed tracks, hazards and historic sites: meaning in shape, not red
**Print evidence (log 0019, P2):** in printed Topo50, a closed track differs
from a foot track *only* by gap length (dash 24/gap 12 vs 23/24). This
applies to print as much as web.
**Rests on:** F-21, W7, palette v0 · **Best evidence:** D (mechanism certain)
**Change:** closed tracks get a dark casing with cross-bars; historic sites
get a distinct glyph with dark-ink labels.
**Met when:** red-light model ≥3:1 vs paper for all safety-relevant marks.

### R-12 — Reserve a symbol channel for track access status
**Rests on:** F-24, F-25 · **Provisional**
**Why:** the most-requested change from the tramping community needs data
we don't have; leave a casing/colour channel unused so it can be added
without redesign.

---

### R-17 — Print-specific fixes found in the Topo50 legend — **new, provisional**
**Rests on:** P1–P9 (`current-state/topo50-print.md`), F-21, F-23 · **Best evidence:** measured (D) + C
- Give **hot and cold springs different glyphs**, not just different inks
  (P3: 1.13:1 in greyscale). Topo50 already does this well for hot spring vs
  fumarole (× vs ⊗) — extend the same idea.
- Separate **native forest from scrub** by a larger lightness step or a
  texture (P5: ΔE 4.8, 1.1:1 greyscale). This changes route choice.
- Keep **scattered scrub as a pattern** (P6) — print got this right; the web
  style should match (R-10 does).
- Apply R-05 to **contour labels and spot heights**, which are italic in
  print (P8).
- Don't use the red-orange ink alone for anything that must be read under a
  red headtorch (P7).

## Products and process

### R-13 — Publish three variants from one source
Full colour (web + print), **greyscale-safe print** (F-23), and a
**high-contrast** web variant for low-vision users.

### R-14 — Run the audit in CI on every style change
`palette_audit.py` and `font_check.py` against the style; fail on new
❌ rows. Makes regressions visible and keeps the evidence chain alive.

### R-15 — Start from LINZ's MIT-licensed `topographic-v2` style
Fork rather than rewrite: it already maps the Shortbread schema, and staying
close to upstream lets improvements flow back to LINZ.

### R-16 — Validate with real users before calling anything "accessible"
Grade D model results must be confirmed. Minimum: (a) CVD readers,
(b) dyslexic readers, (c) readers 60+, (d) LandSAR / tramping club members
familiar with Topo50. Tasks: identify landform (ridge vs valley), follow a
track, find a named feature, judge vegetation, read a grid reference — on
paper under daylight, dusk, and red headtorch, and on a phone.
