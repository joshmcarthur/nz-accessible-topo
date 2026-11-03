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


def main(paths=None):
    paths = paths if paths is not None else sys.argv[1:]
    print("| Font | Macron vowels | U+0304 | x-height/em | x/cap | Glyphs |")
    print("|---|---|:-:|---:|---:|---:|")
    for p in paths:
        r = check(p)
        print(
            f"| {r['name']} | {r['macrons']} | {'✅' if r['combining'] else '❌'} | "
            f"{r['x_em']:.3f} | {r['x_cap']:.3f} | {r['glyphs']} |"
        )
