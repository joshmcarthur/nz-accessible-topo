import json

from nzat.check.c1_stale import c1_stale
from nzat.check.c2_italics import c2_italics
from nzat.check.c3_contrast import c3_contrast
from nzat.check.c4_hillshade import c4_hillshade
from nzat.check.c5_fonts import c5_fonts
from nzat.check.c6_pairs import c6_pairs
from nzat.paths import ROOT
from nzat.style.build import build


def main():
    failures = []
    for multidirectional in (False, True):
        variant, builder = build(multidirectional)
        path = ROOT / "styles" / f"accessible-{variant}.json"
        with open(path, encoding="utf-8") as handle:
            on_disk = json.load(handle)
        failures.extend(c1_stale(path, on_disk, builder.doc))
        style = on_disk.get("style", on_disk)
        failures.extend(c2_italics(style, variant))
        failures.extend(c3_contrast(style, variant))
        failures.extend(c4_hillshade(style, variant))
        failures.extend(c5_fonts(style, variant))
    failures.extend(c6_pairs())
    if failures:
        print("FAIL\n  " + "\n  ".join(failures))
        return 1
    print("OK — C1–C6 pass")
    return 0
