"""Build the site ink-contrast table from the Topo50 pair file."""

import json

from nzat.paths import ROOT, STYLE_PATH, TOPO_PAIRS_PATH
from nzat.style.load_rules import load_rules
from nzat.style.pair_audit import pair_audit
from nzat.style.resolve_pairs import resolve_pairs

MATRIX_PATH = ROOT / "site" / "src" / "data" / "ink-matrix.json"
CVD = ("protanopia", "deuteranopia", "tritanopia")
PAPER = (255, 255, 255)
GREY_FLOOR = 3.0
RED_FLOOR = 3.0
DELTA_E_FLOOR = 10.0


def _round(value, places=2):
    return round(float(value), places)


def matrix_rows(pairs, results):
    rows = []
    for pair, result in zip(pairs, results, strict=True):
        worst = min(result[key] for key in CVD)
        rows.append(
            {
                "name": pair["name"],
                "a": {"label": pair["a"]["label"], "colour": pair["a"]["colour"]},
                "b": {"label": pair["b"]["label"], "colour": pair["b"]["colour"]},
                "why": pair.get("why", ""),
                "normal": _round(result["normal"], 1),
                "protanopia": _round(result["protanopia"], 1),
                "deuteranopia": _round(result["deuteranopia"], 1),
                "tritanopia": _round(result["tritanopia"], 1),
                "worst_cvd": _round(worst, 1),
                "grey_cr": _round(result["grey_cr"]),
                "red_cr": _round(result["red_cr"]),
                "fails_r01": bool(
                    result["grey_cr"] < GREY_FLOOR or result["red_cr"] < RED_FLOOR
                ),
            }
        )
    return rows


def build_matrix(pairs_path=None, style_path=None):
    raw = json.loads((pairs_path or TOPO_PAIRS_PATH).read_text(encoding="utf-8"))
    rules = load_rules(style_path or STYLE_PATH)
    resolved = resolve_pairs(raw, rules)
    results = pair_audit(resolved, PAPER)
    return {
        "source_pairs": "tools/pairs-topo50-accessible.json",
        "source_config": "tools/style-topo50.json",
        "bg": "#FFFFFF",
        "floors": {
            "grey_cr": GREY_FLOOR,
            "red_cr": RED_FLOOR,
            "delta_e": DELTA_E_FLOOR,
        },
        "pairs": matrix_rows(resolved, results),
    }


def main():
    payload = build_matrix()
    MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    MATRIX_PATH.write_text(
        json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    fails = sum(1 for row in payload["pairs"] if row["fails_r01"])
    print(f"{len(payload['pairs'])} pairs, {fails} fail R-01 grey or red 3:1")
