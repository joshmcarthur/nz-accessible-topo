"""Measure one legend symbol against the project floors. Pure: no QGIS, no files.

A symbol spec holds its inks and sizes. Each ink has a role:
- carrier: the ink that draws the shape. It must meet the contrast floors.
- accent: a hue that a carrier or a shape already backs up. Shown, not gated.
- fill: an area fill. Shown, not gated. Edges, marks and labels carry the area.
"""

from nzat.style.pair_audit import pair_audit

PAPER = "#FFFFFF"
GRAPHIC_FLOOR = 3.0  # R-01, F-20: 3:1 for graphics, greyscale model
RED_FLOOR = 3.0  # R-01, R-11: the same 3:1 under red light
LINE_FLOOR_MM = 0.15  # F-31: thinnest accepted step on the sheet (drain, log 0071)
MARK_FLOOR_MM = 1.4  # F-31: Esri symbol floor, 2/3 of 6 pt
CVD = ("protanopia", "deuteranopia", "tritanopia")


def measure_pair(ink, behind=PAPER):
    """Grey, red-light and worst-dichromacy figures for one ink on one background."""
    pair = {"name": "", "a": {"label": "", "colour": ink}}
    pair["b"] = {"label": "", "colour": behind}
    result = pair_audit([pair], (255, 255, 255))[0]
    return {
        "grey": round(float(result["grey_cr"]), 2),
        "red": round(float(result["red_cr"]), 2),
        "worst_cvd": round(float(min(result[k] for k in CVD)), 1),
    }


def _check(rule, label, ok, detail):
    return {"rule": rule, "label": label, "pass": bool(ok), "detail": detail}


def _contrast_checks(inks):
    checks = []
    for ink in inks:
        if ink["role"] != "carrier":
            continue
        for behind in (PAPER, ink.get("on")):
            if not behind:
                continue
            m = measure_pair(ink["hex"], behind)
            where = "paper" if behind == PAPER else behind
            name = f"{ink['name']} {ink['hex']} on {where}"
            checks.append(
                _check(
                    "R-01, F-20",
                    "Contrast 3:1",
                    m["grey"] >= GRAPHIC_FLOOR,
                    f"{name}: {m['grey']:.2f}:1",
                )
            )
            checks.append(
                _check(
                    "R-01, R-11",
                    "Red light 3:1",
                    m["red"] >= RED_FLOOR,
                    f"{name}: {m['red']:.2f}:1",
                )
            )
    return checks


def _size_checks(spec):
    checks = []
    exempt = spec.get("exempt")
    for field, label, floor in (
        ("line_mm", "Line width", LINE_FLOOR_MM),
        ("stroke_mm", "Stroke width", LINE_FLOOR_MM),
        ("mark_mm", "Mark size", MARK_FLOOR_MM),
    ):
        value = spec.get(field)
        if value is None:
            continue
        if exempt and field in exempt:
            detail = f"{value} mm. Exempt: {exempt[field]}"
            checks.append(_check("F-31", label, True, detail))
            continue
        detail = f"{value} mm, floor {floor} mm"
        checks.append(_check("F-31", label, value >= floor, detail))
    return checks


def _colour_only_check(spec):
    other = spec.get("colour_only")
    if not other:
        return []
    carrier = next(i for i in spec["inks"] if i["role"] == "carrier")
    m = measure_pair(carrier["hex"], other["hex"])
    detail = (
        f"Same shape as {other['label']} {other['hex']}. "
        f"Grey {m['grey']:.2f}:1, red {m['red']:.2f}:1, "
        f"worst CVD ΔE {m['worst_cvd']:.1f}"
    )
    return [_check("R-17", "Not colour alone", False, detail)]


def evaluate(spec, merged_with=None):
    """Return the checks for one measured or proposed symbol spec."""
    checks = _contrast_checks(spec.get("inks", ()))
    checks += _size_checks(spec)
    checks += _colour_only_check(spec)
    if merged_with:
        checks.append(
            _check(
                "R-01",
                "Own symbol on the sheet",
                False,
                f"The sheet draws it as {merged_with}",
            )
        )
    return checks


def passes(checks):
    return all(check["pass"] for check in checks)
