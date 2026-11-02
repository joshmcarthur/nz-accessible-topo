# 0024 — Accessible Topo50 uses Atkinson Hyperlegible Next; Nimbus stays stock

**Date:** 2026-11-01

## Question
What does the AGPL-3.0 font licence require if we change Topo50 labels, and which face does the accessible sheet use (B-28)?

## What we did
Read `fonts/LICENSE` and `fonts/README.md` in `linz/topographic-qgis` @ `c0edcfc` (S-LINZ-TOPO-QGIS). Compared a modified Nimbus with a swap to Atkinson Hyperlegible Next, whose OFL terms and Ō/ō gap are already recorded (F-26, F-27, F-28, F-29, R-06).

## What we found
Nimbus Sans LINZ is AGPL-3.0. `fonts/LICENSE` adds this term: those font programs may be included in a PostScript or PDF document, whatever licence the document uses. That covers the **stock** sheet, which keeps LINZ's project and therefore these font files. This project does not modify those files and does not copy the OTF files into the repo.

A modified Nimbus would be a derivative font under AGPL-3.0. The accessible sheet does not take that path.

The accessible sheet swaps the label family to **Atkinson Hyperlegible Next**, upright statics, with Ō/ō added by `tools/patch_atkinson_omacron.py` from the OFL sources (F-26, F-29). The patch renames the family to `NZAT Legible Test`. QGIS can already shape Ō/ō from the official font (F-28). The composites are still added so the glyphs exist in the file. The patched font stays OFL. The font binary is built at render time and is not committed.

Atkinson Hyperlegible Next has no Narrow master. Labels that are Nimbus Narrow on the stock sheet become the regular width on the accessible sheet. The patch covers upright statics only, which matches the no-italic rule (R-05). Bold is patched per file when the QML uses Bold.

This is a plain reading of the licence texts. It is not legal advice.

## What changed
- Decision: stock render keeps unmodified Nimbus Sans LINZ. The accessible render uses the patched Atkinson face.
- R-18 and R-06 note the QGIS face. B-28 is Done. B-11 is the swap itself, and moves up with the QGIS label work.
- The full decision record is in the Lore Work `topo50-qgis-render` (`decisions.md`).

## Confidence & gaps
- The reading covers a local PDF render and a QML family swap. It does not cover publishing a modified Nimbus, or serving either font on the web.
- The patch does not extend kerning, and the family name `NZAT Legible Test` is the proof-of-concept name. A public name is a later choice.
- OQ-11 (this project's own licence) is still open.
