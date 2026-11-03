import json

from nzat.paths import PAIRS_PATH, STYLE_PATH
from nzat.style.pair_audit import pair_audit
from nzat.style.resolve_pairs import resolve_pairs


def c6_pairs():
    with open(PAIRS_PATH, encoding="utf-8") as handle:
        raw = json.load(handle)
    with open(STYLE_PATH, encoding="utf-8") as handle:
        rules = json.load(handle)
    pairs = resolve_pairs(raw, rules)
    failures = []
    for result, pair in zip(pair_audit(pairs, (255, 255, 255)), pairs, strict=True):
        floor = pair.get("floor", {})
        worst_de = min(
            result[key]
            for key in ("normal", "protanopia", "deuteranopia", "tritanopia")
        )
        if worst_de < floor.get("de", 0):
            failures.append(
                f"C6: {result['name']}: worst ΔE {worst_de:.1f} < {floor['de']}"
            )
        if result["grey_cr"] < floor.get("grey", 0):
            failures.append(
                f"C6: {result['name']}: greyscale {result['grey_cr']:.2f} < {floor['grey']}"
            )
        if result["red_cr"] < floor.get("red", 0):
            failures.append(
                f"C6: {result['name']}: red-light {result['red_cr']:.2f} < {floor['red']}"
            )
    return failures
