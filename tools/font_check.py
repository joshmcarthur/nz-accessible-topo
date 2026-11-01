#!/usr/bin/env python3
"""
font_check.py — check candidate typefaces for NZ topographic labelling.

Reports, per font file:
  - te reo Māori macron vowel coverage (precomposed Āā Ēē Īī Ōō Ūū) and the
    combining macron U+0304 (fallback for decomposed input)
  - x-height / em and x-height / cap-height (larger x-height reads bigger at
    the same point size — matters at 6–8 pt map label sizes)
  - whether an italic companion exists is noted by the caller

Usage: python3 tools/font_check.py FONT.ttf [FONT.ttf ...]
Requires fontTools.
"""
import sys
from fontTools.ttLib import TTFont

MACRONS = "ĀāĒēĪīŌōŪū"
COMBINING_MACRON = 0x0304


def check(path):
    f = TTFont(path)
    cmap = f.getBestCmap()
    missing = [c for c in MACRONS if ord(c) not in cmap]
    os2 = f["OS/2"]
    upm = f["head"].unitsPerEm
    xh = getattr(os2, "sxHeight", 0) or 0
    ch = getattr(os2, "sCapHeight", 0) or 0
    name = f["name"].getDebugName(4) or path
    return {
        "name": name,
        "macrons": "all" if not missing else "missing " + "".join(missing),
        "combining": COMBINING_MACRON in cmap,
        "x_em": xh / upm if xh else float("nan"),
        "x_cap": xh / ch if xh and ch else float("nan"),
        "glyphs": len(f.getGlyphOrder()),
    }


if __name__ == "__main__":
    print("| Font | Macron vowels | U+0304 | x-height/em | x/cap | Glyphs |")
    print("|---|---|:-:|---:|---:|---:|")
    for p in sys.argv[1:]:
        r = check(p)
        print(f"| {r['name']} | {r['macrons']} | {'✅' if r['combining'] else '❌'} | "
              f"{r['x_em']:.3f} | {r['x_cap']:.3f} | {r['glyphs']} |")
