# Decisions

## B-28: Leave Nimbus Sans LINZ unchanged

**Status:** Accepted
**Date:** 2026-11

### Context

Topo50 labels use Nimbus Sans LINZ, the faces in `linz/topographic-qgis` `fonts/` at `c0edcfc`. `fonts/LICENSE` distributes them under AGPL-3.0 with this extra term: the font programs may be included in a PostScript or PDF document, whatever licence that document uses. B-25 changes which face and size the QML requests. B-11, later, may point the QML at another family. Either path can be done by editing the QML or by editing the font files.

### Decision

Leave the Nimbus Sans LINZ files unchanged. Do not copy the OTF files into this repo.

QML may select an upright face of that family and a larger size. A later swap uses an OFL face. This project does not modify Nimbus and does not publish a modified Nimbus.

### Rationale

The exemption covers embedding the stock font programs in a PDF. A QML change that asks for Regular or Narrow, or for a larger size, uses those stock programs. It does not create a derivative font.

A modified Nimbus would be an AGPL-3.0 font. Shipping it would mean shipping the AGPL text and the font source. This slice does not need glyph edits. Nimbus already contains the macron vowels (F-30).

An OFL face (Open Sans, or Atkinson Hyperlegible Next under F-26) is the path when a different family is wanted. That swap replaces the family name in the QML. It does not fork Nimbus.

This is a plain reading of `fonts/LICENSE` and of AGPL-3.0 as it applies to a font program. It is not legal advice.

### Consequences

B-25 and B-24 stay in the QML. Rendered PDFs may embed the stock faces. B-11 stays a QML family change to an OFL face. A future glyph change belongs on an OFL font, and needs a new decision if someone proposes editing Nimbus instead.
