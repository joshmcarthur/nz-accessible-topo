#!/usr/bin/env python3
"""
patch_atkinson_omacron.py — PROOF OF CONCEPT: add Ō/ō to Atkinson Hyperlegible Next.

Adds `Omacron` (U+014C) and `omacron` (U+014D) as composites of O/o + uni0304,
the same construction the font uses for Ā Ē Ī Ū ā ē ī ū. The macron's x offset
is computed by centring it over the base glyph's bounding box; this rule
reproduces the existing Amacron and Umacron offsets exactly (log 0017), and
for the symmetric 'o' it agrees with the advance-centre rule.

Source must be the OFL-1.1 release from github.com/googlefonts/atkinson-hyperlegible-next
(see docs/findings/atkinson-licence.md). The output is renamed so it can't be
confused with the official font. Intended for testing and for an upstream PR,
not for distribution.

Known gaps: upright statics only; kerning classes not extended to the new
glyphs; no hinting review.

Usage: python3 tools/patch_atkinson_omacron.py IN.ttf OUT.ttf
"""
import sys

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent

NEW_FAMILY = "NZAT Legible Test"


def bbox_centre(glyf, name):
    g = glyf[name]
    g.recalcBounds(glyf)
    return (g.xMin + g.xMax) / 2


def composite(glyf, base, mark, x, y):
    g = Glyph()
    g.numberOfContours = -1
    g.components = []
    for name, dx, dy in ((base, 0, 0), (mark, x, y)):
        c = GlyphComponent()
        c.glyphName, c.x, c.y, c.flags = name, int(round(dx)), int(round(dy)), 0
        g.components.append(c)
    g.components[0].flags = 0x0200  # USE_MY_METRICS
    g.recalcBounds(glyf)
    return g


def main(src, dst):
    f = TTFont(src)
    glyf, hmtx = f["glyf"], f["hmtx"]
    mark = "uni0304"
    mc = bbox_centre(glyf, mark)
    # check the rule against an existing capital before trusting it
    a_off = [c.x for c in glyf["Amacron"].components if c.glyphName == mark][0]
    assert abs(round(bbox_centre(glyf, "A") - mc) - a_off) <= 1, "centring rule does not reproduce Amacron"
    cap_y = [c.y for c in glyf["Amacron"].components if c.glyphName == mark][0]
    low_y = [c.y for c in glyf["amacron"].components if c.glyphName == mark][0]

    order = list(f.getGlyphOrder())
    for new, base, y, cp in (("Omacron", "O", cap_y, 0x14C), ("omacron", "o", low_y, 0x14D)):
        if new in order:
            continue
        order.append(new)
        f.setGlyphOrder(order)
        glyf.glyphOrder = order
        glyf[new] = composite(glyf, base, mark, bbox_centre(glyf, base) - mc, y)
        hmtx[new] = hmtx[base]
        for t in f["cmap"].tables:
            if t.isUnicode():
                t.cmap[cp] = new
        if "GDEF" in f and f["GDEF"].table.GlyphClassDef:
            f["GDEF"].table.GlyphClassDef.classDefs[new] = 1  # base glyph
    f["maxp"].numGlyphs = len(order)
    if "post" in f and f["post"].formatType == 2.0:
        f["post"].extraNames = []
        f["post"].mapping = {}

    style = f["name"].getDebugName(2) or "Regular"
    for rec in list(f["name"].names):
        if rec.nameID in (1, 16):
            rec.string = NEW_FAMILY
        elif rec.nameID == 4:
            rec.string = f"{NEW_FAMILY} {style}"
        elif rec.nameID == 6:
            rec.string = f"{NEW_FAMILY.replace(' ', '')}-{style.replace(' ', '')}"
        elif rec.nameID == 3:
            rec.string = f"{NEW_FAMILY} {style} (patched; adds U+014C/U+014D)"
    f.save(dst)
    print("wrote", dst)


if __name__ == "__main__":
    main(*sys.argv[1:3])
