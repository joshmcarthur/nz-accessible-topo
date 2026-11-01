# Findings: can we add macrons to Atkinson Hyperlegible Next?

*Not legal advice. Summary of licence texts and their plain reading.*

## F-26 — Yes: the GitHub/Google Fonts release is plain OFL 1.1, with no Reserved Font Name, and it's forward-licensed
The `googlefonts/atkinson-hyperlegible-next` repo (HEAD `7925f50`) ships the
standard SIL Open Font License 1.1, copyright "The Atkinson Hyperlegible Next
Project Authors", with **no Reserved Font Name declared**. Under OFL 1.1:

| Clause | Meaning for us |
|---|---|
| Permission | use, study, copy, modify, redistribute modified copies ✅ |
| 1 | can't sell the font *by itself* (bundling with a map product is fine) |
| 2 | keep the copyright notice + licence with every copy |
| 3 | Reserved Font Names can't be used by modified versions — **none are reserved in this release** |
| 4 | can't use the authors' names to promote our version (acknowledging them is fine) |
| 5 | **forward licensing:** modified versions must be distributed entirely under OFL, and nothing else. Maps and documents *made with* the font are not bound by this |

**Sources:** S-OFL-ATKINSON-NEXT — `OFL.txt` in the repo (read directly, C).

## F-27 — Caution: the Braille Institute's own download uses a different, OFL-derived licence
The download from brailleinstitute.org/freefont has historically come with a
separate "Atkinson Hyperlegible Font License" — Debian reviewers described it
as a modified OFL. One listing of the *Next* licence names Reserved Font Names
"ATKINSON" and "HYPERLEGIBLE".
**Sources:** S-DEBIAN-ATKINSON (D), S-SCANCODE-ATKINSON (C), S-NEXT-RFN (D,
secondary listing — not verified against the Braille Institute PDF).
**Implication:** licences attach to the copy you receive. **Base any patch on
the GitHub OFL sources**, and rename the result anyway, so it's compliant
whichever text a reader has in mind. Community forks already exist under OFL
(e.g. "Atkinson Hyperlegible Pro").

## F-28 — The missing Ō/ō only breaks renderers that don't shape text
HarfBuzz-based renderers (Pillow+raqm here; also browsers and Qt/QGIS,
expected but not tested) decompose a missing `ō` into `o` + U+0304 and place
the macron with the font's `mark` feature — the official font renders
"Taupō" correctly. Renderers that draw **one glyph per codepoint** show a
missing-glyph box instead. MapLibre's glyph PBFs work that way.
**Evidence:** `docs/visuals/06-shaping-vs-no-shaping.png` (D, measured).
**Implication:** print via QGIS may work today; web maps need the glyphs to
exist (patched font, or upstream fix) *and* glyph PBFs built from that font.

## F-29 — The fix is small and mechanical
Ā and Ū are composites of the base letter + `uni0304`, centred on the base's
bounding box; that rule reproduces their offsets exactly (135, 167). Applying
it to O and o gives offsets 179 and 96 (the symmetric `o` agrees under both
centring rules). `tools/patch_atkinson_omacron.py` does this for static
TTFs and renames the result "NZAT Legible Test".
**Sources:** S-OUR-PATCH (D, measured).
**Known gaps:** upright statics only; kerning classes not extended; not
reviewed by the type designers.
