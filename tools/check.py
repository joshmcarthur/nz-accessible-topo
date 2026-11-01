#!/usr/bin/env python3
"""
check.py — CI gate for the built styles (R-14).

Fails (exit 1) if any of these regress:
  C1  styles/*.json are not what build_style.py produces from upstream/ (stale build)
  C2  any italic face is used (R-05)
  C3  any label is below 4.5:1 against its halo, except documented
      false positives (labels drawn on an icon) (R-07)
  C4  hillshade primary light is not 337.5° (R-03)
  C5  a font family outside the macron-verified list is used (R-06, F-12)
  C6  any must-distinguish pair in tools/pairs-accessible-v0.json drops
      below its declared floor (R-01)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_style  # noqa: E402
import palette_audit as pa  # noqa: E402

ROOT = build_style.ROOT
# Families whose google/fonts builds have all ten macron vowels
# (tools/font_check.py, logs 0006 and 0014). NB: the LINZ glyph server's PBFs
# have not been inspected — see OQ-13.
MACRON_VERIFIED = ("Open Sans", "Roboto", "Noto Sans")
TEXT_ALLOWLIST = {"All-Highway-Labels-three", "All-Highway-Labels-standard"}  # white text on shield icon

failures = []


def fail(code, msg):
    failures.append(f"{code}: {msg}")


def fonts_in(style):
    for l in style["layers"]:
        f = l.get("layout", {}).get("text-font")
        if isinstance(f, list):
            for x in f:
                if isinstance(x, str):
                    yield l["id"], x


for md in (False, True):
    variant, b = build_style.build(md)
    path = os.path.join(ROOT, "styles", f"accessible-{variant}.json")
    on_disk = json.load(open(path))
    if on_disk != json.loads(json.dumps(b.doc)):
        fail("C1", f"{path} is stale — run tools/build_style.py")
    style = on_disk.get("style", on_disk)

    for lid, font in fonts_in(style):
        if "Italic" in font:
            fail("C2", f"{variant}:{lid} uses {font}")
        if not font.startswith(MACRON_VERIFIED):
            fail("C5", f"{variant}:{lid} uses unverified family {font}")

    for lid, cr, *_ in pa.text_audit(style, (255, 255, 255)):
        if cr < 4.5 and lid not in TEXT_ALLOWLIST:
            fail("C3", f"{variant}:{lid} text contrast {cr:.2f}")

    for l in style["layers"]:
        if l["type"] == "hillshade":
            d = l["paint"].get("hillshade-illumination-direction")
            primary = d[0] if isinstance(d, list) else d
            if primary != 337.5:
                fail("C4", f"{variant}:{l['id']} primary light {primary}")

pairs_path = os.path.join(ROOT, "tools", "pairs-accessible-v0.json")
for r, p in zip(pa.pair_audit(json.load(open(pairs_path)), (255, 255, 255)), json.load(open(pairs_path))):
    floor = p.get("floor", {})
    worst_de = min(r[k] for k in ("normal", "protanopia", "deuteranopia", "tritanopia"))
    if worst_de < floor.get("de", 0):
        fail("C6", f"{r['name']}: worst ΔE {worst_de:.1f} < {floor['de']}")
    if r["grey_cr"] < floor.get("grey", 0):
        fail("C6", f"{r['name']}: greyscale {r['grey_cr']:.2f} < {floor['grey']}")
    if r["red_cr"] < floor.get("red", 0):
        fail("C6", f"{r['name']}: red-light {r['red_cr']:.2f} < {floor['red']}")

if failures:
    print("FAIL\n  " + "\n  ".join(failures))
    sys.exit(1)
print("OK — C1–C6 pass")
