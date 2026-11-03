import argparse
import json

from nzat.colour.parse_colour import parse_colour
from nzat.paths import STYLE_PATH
from nzat.style.load_maplibre import load_maplibre
from nzat.style.pair_audit import pair_audit
from nzat.style.resolve_pairs import resolve_pairs
from nzat.style.text_audit import text_audit


def _flag_de(v):
    return "❌" if v < 5 else ("⚠️" if v < 10 else "✅")


def _flag_cr(v):
    return "❌" if v < 1.5 else ("⚠️" if v < 3 else "✅")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("style")
    ap.add_argument("--pairs", default=None)
    ap.add_argument(
        "--config",
        default=str(STYLE_PATH),
        help="shared style file for pair colour paths",
    )
    ap.add_argument("--bg", default="#ffffff", help="background colour for compositing")
    ap.add_argument("--md", default=None)
    args = ap.parse_args()

    bg = parse_colour(args.bg)[:3]
    lines = []
    w = lines.append

    rows = text_audit(load_maplibre(args.style), bg) if args.style != "-" else []
    italic = sum(1 for r in rows if "Italic" in r[2])
    if rows:
        w(f"## Text contrast (label vs halo, composited on {args.bg})\n")
        w(f"Symbol layers with a solid text colour: {len(rows)}. Italic: {italic}.\n")
        w("| Layer | Contrast | ≥4.5:1 | Font | text-color | halo |")
        w("|---|---:|:-:|---|---|---|")
        for lid, cr, font, tc, hc in sorted(rows, key=lambda r: r[1]):
            w(
                f"| `{lid}` | {cr:.2f} | {'✅' if cr >= 4.5 else ('⚠️' if cr >= 3 else '❌')} | {font} | `{tc}` | `{hc}` |"
            )
        fails = [r for r in rows if r[1] < 4.5]
        w(f"\n**{len(fails)} of {len(rows)} label layers are below 4.5:1.**\n")

    if args.pairs:
        pairs = json.load(open(args.pairs))
        pairs = resolve_pairs(pairs, json.load(open(args.config)))
        res = pair_audit(pairs, bg)
        w("## Must-distinguish pairs\n")
        w(
            "ΔE = CIEDE2000 (❌ <5, ⚠️ 5–10, ✅ >10). Grey/Red = luminance contrast ratio "
            "under greyscale and red-light models (❌ <1.5, ⚠️ <3, ✅ ≥3).\n"
        )
        w(
            "| Pair | Normal ΔE | Protan ΔE | Deutan ΔE | Tritan ΔE | Grey CR | Red-light CR |"
        )
        w("|---|---:|---:|---:|---:|---:|---:|")
        for r in res:
            w(
                f"| **{r['name']}**: {r['a']} vs {r['b']} | {r['normal']:.1f} {_flag_de(r['normal'])} "
                f"| {r['protanopia']:.1f} {_flag_de(r['protanopia'])} | {r['deuteranopia']:.1f} {_flag_de(r['deuteranopia'])} "
                f"| {r['tritanopia']:.1f} {_flag_de(r['tritanopia'])} | {r['grey_cr']:.2f} {_flag_cr(r['grey_cr'])} "
                f"| {r['red_cr']:.2f} {_flag_cr(r['red_cr'])} |"
            )
        w("")
        for r in res:
            if r["why"]:
                w(f"- **{r['name']}** — {r['why']}")

    out = "\n".join(lines)
    if args.md:
        open(args.md, "w").write(out + "\n")
    print(out)
