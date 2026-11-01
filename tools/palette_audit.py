#!/usr/bin/env python3
"""
palette_audit.py — audit a MapLibre/Mapbox GL style for accessibility risks.

What it measures (all are *models* of perception — evidence grade D until
validated with users; see docs/method.md):

1. WCAG 2.x contrast ratio of every text label against its halo (composited
   over a stated background).
2. Separability of "must-distinguish" colour pairs (pairs.json) under:
     - normal trichromatic vision
     - protanopia, deuteranopia, tritanopia (Machado, Oliveira & Fernandes 2009,
       severity 1.0, applied in linear RGB)
     - greyscale (photocopy / e-ink / monochrome print): relative luminance
     - narrow-band red illumination (red headtorch): reflectance in the R
       channel only — a crude physical model, see docs/findings/field-conditions.md
   Separability is reported as CIEDE2000 ΔE (for colour conditions) and as a
   luminance contrast ratio (for greyscale / red light).

Usage:
    python3 tools/palette_audit.py STYLE.json [--pairs tools/pairs.json] [--md OUT.md]

Only numpy is required.
"""
import argparse
import json
import math
import re
import sys

import numpy as np

# ---------------------------------------------------------------- colour maths

def parse_colour(s):
    """Parse 'rgba(r,g,b,a)', 'rgb(r,g,b)', '#rrggbb' -> (r,g,b,a) with r,g,b 0-255."""
    if not isinstance(s, str):
        return None
    s = s.strip()
    m = re.match(r"rgba?\(([^)]*)\)", s)
    if m:
        parts = [p.strip() for p in m.group(1).split(",")]
        r, g, b = (float(p) for p in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        return (r, g, b, a)
    m = re.match(r"#([0-9a-fA-F]{6})$", s)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    return None


def composite(fg, bg):
    """Alpha-composite fg (r,g,b,a) over opaque bg (r,g,b[,a]) -> opaque (r,g,b)."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))


def srgb_to_linear(c):
    c = np.asarray(c, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(c, 0, 1)
    return 255.0 * np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def rel_luminance(rgb):
    r, g, b = srgb_to_linear(rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# Machado, Oliveira & Fernandes (2009), severity 1.0, linear RGB.
MACHADO = {
    "protanopia": np.array([[0.152286, 1.052583, -0.204868],
                            [0.114503, 0.786281, 0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
    "deuteranopia": np.array([[0.367322, 0.860646, -0.227968],
                              [0.280085, 0.672501, 0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
    "tritanopia": np.array([[1.255528, -0.076749, -0.178779],
                            [-0.078411, 0.930809, 0.147602],
                            [0.004733, 0.691367, 0.303900]]),
}


def simulate(rgb, kind):
    lin = srgb_to_linear(rgb)
    return tuple(linear_to_srgb(MACHADO[kind] @ lin))


def rgb_to_lab(rgb):
    r, g, b = srgb_to_linear(rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))


def red_light_reflectance(rgb):
    """Relative reflectance under narrow-band red light: linear R channel only."""
    return float(srgb_to_linear(rgb)[0])


# ---------------------------------------------------------------- style access

def load_style(path):
    s = json.load(open(path))
    return s.get("style", s)  # basemaps-config wraps the style in {"style": ...}


def first_colour(paint, keys):
    for k in keys:
        v = paint.get(k)
        c = parse_colour(v) if isinstance(v, str) else None
        if c:
            return c
    return None


def text_audit(style, bg):
    rows = []
    for layer in style["layers"]:
        if layer.get("type") != "symbol":
            continue
        paint = layer.get("paint", {})
        tc = parse_colour(paint.get("text-color", "")) if isinstance(paint.get("text-color"), str) else None
        if not tc:
            continue
        halo = parse_colour(paint.get("text-halo-color", "")) if isinstance(paint.get("text-halo-color"), str) else None
        halo_w = paint.get("text-halo-width", 0)
        behind = composite(halo, bg) if halo and (not isinstance(halo_w, (int, float)) or halo_w > 0) else bg
        fg = composite(tc, behind)
        cr = contrast_ratio(rel_luminance(fg), rel_luminance(behind))
        font = layer.get("layout", {}).get("text-font", [""])
        font = font[0] if isinstance(font, list) and font and isinstance(font[0], str) else str(font)
        rows.append((layer["id"], cr, font, paint.get("text-color"), paint.get("text-halo-color")))
    return rows


def pair_audit(pairs, bg):
    out = []
    for p in pairs:
        a = composite(parse_colour(p["a"]["colour"]), bg)
        b = composite(parse_colour(p["b"]["colour"]), bg)
        res = {"name": p["name"], "a": p["a"]["label"], "b": p["b"]["label"], "why": p.get("why", "")}
        res["normal"] = ciede2000(rgb_to_lab(a), rgb_to_lab(b))
        for k in MACHADO:
            res[k] = ciede2000(rgb_to_lab(simulate(a, k)), rgb_to_lab(simulate(b, k)))
        res["grey_cr"] = contrast_ratio(rel_luminance(a), rel_luminance(b))
        res["red_cr"] = contrast_ratio(red_light_reflectance(a), red_light_reflectance(b))
        out.append(res)
    return out


# ---------------------------------------------------------------- reporting

def flag_de(v):
    # Rough interpretive bands for CIEDE2000 between map symbols at small size.
    # <5: likely confused at map-symbol size; 5-10: distinguishable side by
    # side, risky in isolation; >10: comfortably distinct. These thresholds are
    # a working assumption (grade D) — see docs/findings/colour-vision.md.
    return "❌" if v < 5 else ("⚠️" if v < 10 else "✅")


def flag_cr(v):
    return "❌" if v < 1.5 else ("⚠️" if v < 3 else "✅")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("style")
    ap.add_argument("--pairs", default=None)
    ap.add_argument("--bg", default="#ffffff", help="background colour for compositing")
    ap.add_argument("--md", default=None)
    args = ap.parse_args()

    bg = parse_colour(args.bg)[:3]
    lines = []
    w = lines.append

    # STYLE may be "-" to audit only a pairs file (e.g. a proposed palette).
    rows = text_audit(load_style(args.style), bg) if args.style != "-" else []
    italic = sum(1 for r in rows if "Italic" in r[2])
    if rows:
        w(f"## Text contrast (label vs halo, composited on {args.bg})\n")
        w(f"Symbol layers with a solid text colour: {len(rows)}. Italic: {italic}.\n")
        w("| Layer | Contrast | ≥4.5:1 | Font | text-color | halo |")
        w("|---|---:|:-:|---|---|---|")
        for lid, cr, font, tc, hc in sorted(rows, key=lambda r: r[1]):
            w(f"| `{lid}` | {cr:.2f} | {'✅' if cr >= 4.5 else ('⚠️' if cr >= 3 else '❌')} | {font} | `{tc}` | `{hc}` |")
        fails = [r for r in rows if r[1] < 4.5]
        w(f"\n**{len(fails)} of {len(rows)} label layers are below 4.5:1.**\n")

    if args.pairs:
        pairs = json.load(open(args.pairs))
        res = pair_audit(pairs, bg)
        w("## Must-distinguish pairs\n")
        w("ΔE = CIEDE2000 (❌ <5, ⚠️ 5–10, ✅ >10). Grey/Red = luminance contrast ratio "
          "under greyscale and red-light models (❌ <1.5, ⚠️ <3, ✅ ≥3).\n")
        w("| Pair | Normal ΔE | Protan ΔE | Deutan ΔE | Tritan ΔE | Grey CR | Red-light CR |")
        w("|---|---:|---:|---:|---:|---:|---:|")
        for r in res:
            w(f"| **{r['name']}**: {r['a']} vs {r['b']} | {r['normal']:.1f} {flag_de(r['normal'])} "
              f"| {r['protanopia']:.1f} {flag_de(r['protanopia'])} | {r['deuteranopia']:.1f} {flag_de(r['deuteranopia'])} "
              f"| {r['tritanopia']:.1f} {flag_de(r['tritanopia'])} | {r['grey_cr']:.2f} {flag_cr(r['grey_cr'])} "
              f"| {r['red_cr']:.2f} {flag_cr(r['red_cr'])} |")
        w("")
        for r in res:
            if r["why"]:
                w(f"- **{r['name']}** — {r['why']}")

    out = "\n".join(lines)
    if args.md:
        open(args.md, "w").write(out + "\n")
    print(out)


if __name__ == "__main__":
    sys.exit(main())
