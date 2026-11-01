# 0018 — Atkinson licence, and a proof-of-concept Ō/ō patch

**Date:** 2026-11-01

## Question
Is Atkinson Hyperlegible Next licensed so we can add the missing macron
vowels — and if so, how?

## What we did
- Read `OFL.txt` in the upstream repo directly.
- Searched for the Braille Institute's own licence; found that its website
  download carries a different OFL-derived licence, reportedly with Reserved
  Font Names for *Next*.
- Inspected how the font builds Ā/Ū/ā/ē (composites of base + `uni0304`),
  derived the placement rule, verified it reproduces existing glyphs, and
  wrote `tools/patch_atkinson_omacron.py`.
- Rendered official vs patched, with and without text shaping.

## What we found
- F-26: GitHub release is plain OFL 1.1, no RFN; modified versions must stay
  OFL (forward-licensed).
- F-27: the Braille Institute download is a different licence — use the
  GitHub sources and rename.
- F-28 (**changes an earlier finding**): the missing glyphs only break
  per-codepoint renderers. HarfBuzz decomposes ō and positions the macron
  using the font's mark feature, so the official font works in shaped
  renderers. MapLibre's glyph PBFs are per-codepoint, so the web still needs
  the fix.
- F-29: the fix is two composites per master; offsets 179 (Ō) and 96 (ō).

## What changed
- `docs/findings/atkinson-licence.md`, `tools/patch_atkinson_omacron.py`,
  `docs/visuals/05*`, `06*`; F-10 and R-06 refined; sources added.
- The patched font binaries are **not** committed: they're reproducible from
  the script, and the right home for the fix is upstream.

## Confidence & gaps
- Licence reading is plain-language, not legal advice.
- Patch untested in QGIS/MapLibre; kerning for Ō/ō not added; italic and
  variable fonts not patched; designers may prefer a different macron
  position — another reason to go upstream.
