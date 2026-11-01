# Findings: typography, dyslexia and low vision

## F-05 — Italics reduce readability for dyslexic readers; roman sans-serif helps
In an eye-tracking study (48 participants with dyslexia, 12 fonts), sans-serif,
monospaced and roman (upright) styles significantly improved reading
performance over serif, proportional and italic styles. Arial Italic in
particular decreased readability. A later journal version found fonts that
helped dyslexic readers were equally good for non-dyslexic readers.
**Sources:** S-RELLO-2013 (B), S-RELLO-2016 (B).
**Grade:** B (single lab; consistent across two publications).

## F-06 — "Dyslexia fonts" do not help
Dyslexie did not improve speed or accuracy for 170 children with dyslexia
(Exp. 1) or for 102 dyslexic + 45 typical readers (Exp. 2); most preferred
Arial. OpenDyslexic showed no improvement in rate or accuracy either.
**Sources:** S-KUSTER-2018 (B), S-WERY-2017 (B), S-RELLO-2016 (B).
**Grade:** A (multiple independent studies agree).
**Map implication:** don't adopt a novelty "dyslexia font". Choose a
well-designed roman sans-serif.

## F-07 — Extra letter spacing helps dyslexic readers (and rescues bad fonts)
Increased inter-letter spacing improved reading accuracy (≈2×) and speed
(≈20%) for dyslexic children in Italian and French, with no gain for typical
readers; the poorest readers benefited most. The proposed mechanism is
**crowding** — dyslexic readers are abnormally affected by flanking letters.
A follow-up found spacing, not font, drove the benefit, and that spacing
removed the penalty of italic and decorative fonts.
**Sources:** S-ZORZI-2012 (B), S-SPACING-2018 (B).
**Grade:** A– (two studies, different labs; children, not adults).
**Map implication:** map labels are short, isolated words — but they are
*heavily crowded by linework*. Tracking (letter-spacing) and halos both
attack crowding. MapLibre exposes `text-letter-spacing`.

## F-08 — Cartographic convention puts water names in italic
Long-standing guidance labels water features in blue italic; area features
in spaced capitals. The LINZ web style follows this (36 of 68 label layers
italic, all water labels italic).
**Sources:** S-AXIS-LABELING (C), S-USGS-SPECS (C), audit (D).
**Tension with F-05:** the convention and the dyslexia evidence point in
opposite directions. Colour + case/weight can carry the "this is water"
signal without italics.

## F-09 — Minimum label sizes and size steps
Practitioner guidance converges on ~6 pt as an absolute print minimum
(8 pt preferred), ~9–10 px on screen, and size differences under ~15%
not being noticed by readers — so hierarchy steps should be bigger than that.
x-height matters as much as point size at small sizes.
**Sources:** S-COLORADO-TYPO (C), S-AXIS-LABELING (C), S-ESRI-MINSIZE (C),
S-MN-MAPGUIDE (C).
**Grade:** C.

## F-10 — Atkinson Hyperlegible targets character confusions; evidence is thin and it can't yet set all Māori names
Designed by the Braille Institute (2019; *Next* 2025) to differentiate
confusable characters (I/l/1, O/0, B/8). Evidence base is mostly the
designers' own user testing, not independent peer-reviewed studies.
**Our check:** Atkinson Hyperlegible Next v2.001 (google/fonts, upstream
commit 7925f50) **lacks precomposed Ō/ō** (U+014C/U+014D) while having the
other macron vowels. It does have a combining macron and mark positioning,
but MapLibre's glyph rendering doesn't do OpenType mark positioning, so
`Taupō`, `Ōtautahi`, `Ōpōtiki`, `Ōamaru` would break on the web.
**Refined in log 0018 (F-28):** shaping renderers (HarfBuzz) *do* render
these correctly with the official font; only per-codepoint renderers like
MapLibre break. Licence permits patching (F-26).
**Sources:** S-ATKINSON (C/D), S-ATKINSON-NEXT (C), `tools/font_check.py` (D).
**Grade:** D (design rationale) / measured fact for glyph coverage.

## F-30 — Topo50's own labels are mostly condensed italic at 5.5–6.5 pt
In the carto_text sample shipped with LINZ's production pipeline, **300 of 445
labels (67%) are italic**, 288 of them *Narrow* (condensed) italic; 394 are
set at 5.5–6.5 pt. Fonts are Nimbus Sans LINZ (a Helvetica-metric URW font,
renamed by LINZ) standing in for the legacy "ATTriumMou" faces; all ten macron
vowels are present. Condensed + italic + small is the combination the
dyslexia research (F-05, F-07) and crowding mechanism point against.
**Sources:** S-LINZ-TOPO-QGIS, S-LINZ-TOPO-SYSTEM (C); S-OUR-QGIS-ANALYSIS (D).
**Caveat:** a test-area sample, not nationwide. Labels are data-defined, so
the fix is an override in the QML (style expression), not a data edit.

## F-11 — Open Sans (LINZ's current face) is already a reasonable choice
Open Sans has full macron coverage and a large x-height (0.535 em vs 0.496
for Atkinson Next, 0.478 for Source Sans 3). Noto Sans is near-identical in
metrics with far wider coverage. The issue in the current style is not the
family; it's the **italics**, **contrast** and **spacing**.
**Sources:** `tools/font_check.py` output (D, measured).

### Font check output
| Font | Macron vowels | U+0304 | x-height/em | x/cap | Glyphs |
|---|---|:-:|---:|---:|---:|
| Open Sans Regular | all | ✅ | 0.535 | 0.750 | 1150 |
| Atkinson Hyperlegible Regular | missing Ōō | ✅ | 0.496 | 0.743 | 369 |
| Atkinson Hyperlegible Next Regular | missing Ōō | ✅ | 0.496 | 0.743 | 392 |
| Source Sans 3 | all | ✅ | 0.478 | 0.724 | 2478 |
| Noto Sans Regular | all | ✅ | 0.536 | 0.751 | 4515 |
| Lexend Regular | all | ✅ | 0.525 | 0.750 | 850 |
-e 
Font files from `google/fonts` @ `6c1dbe2`.
