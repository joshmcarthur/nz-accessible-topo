import argparse
import json

from nzat.paths import ROOT
from nzat.style.build import build
from nzat.style.write_changes import write_changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    for multidirectional in (False, True):
        variant, builder = build(multidirectional)
        counts = {}
        for rid, _, _ in builder.log:
            counts[rid] = counts.get(rid, 0) + 1
        print(variant, dict(sorted(counts.items())))
        if args.check_only:
            continue
        (ROOT / "styles").mkdir(parents=True, exist_ok=True)
        (ROOT / "docs" / "styles").mkdir(parents=True, exist_ok=True)
        with open(
            ROOT / "styles" / f"accessible-{variant}.json", "w", encoding="utf-8"
        ) as handle:
            json.dump(builder.doc, handle, indent=2, ensure_ascii=False)
        write_changes(
            variant,
            builder,
            ROOT / "docs" / "styles" / f"accessible-{variant}-changes.md",
        )
