#!/usr/bin/env python3
"""
build_style.py — derive the accessible style from LINZ's topographic-v2.

Every change is a named transform tagged with the recommendation (R-xx) it
implements, and is recorded in a change log so a reviewer can see exactly
what moved and why. Re-run after updating upstream/ to rebase on LINZ.

Usage:
    python3 tools/build_style.py                      # writes styles/*.json + docs/styles/*-changes.md
    python3 tools/build_style.py --check-only         # build in memory, print summary
"""
import argparse
import copy
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import palette_audit as pa  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPSTREAM = os.path.join(ROOT, "upstream", "linz-topographic-v2.json")
WHITE = (255, 255, 255)

# ------------------------------------------------------------------ parameters
# Values come from docs/recommendations.md and docs/palette-experiments/proposed-v0.md.
P = {
    "hillshade_direction": 337.5,                         # R-03 (F-14, F-15)
    "contour_index": "#8A4F1C",                           # R-04
    "contour_intermediate": "#C4814B",                    # R-04 rev. (log 0020): lightest same-hue brown ≥3.2:1
    "contour_index_width": {"stops": [[10, 0.8], [12, 1.2], [15, 1.8]]},
    "contour_intermediate_width": {"stops": [[12, 0.6], [16, 0.9]]},  # thinner: dense slopes read as texture
    "scrub": "rgba(163, 204, 144, 1)",                    # R-10 (#A3CC90)
    "scattered_scrub": "rgba(224, 237, 216, 1)",          # R-10 (#E0EDD8)
    "closed_track_shadow": "rgba(26, 26, 26, 0.55)",      # R-11
    "text_contrast_min": 4.8,                             # R-07: WCAG 4.5 + 0.3 margin for antialiasing / print variance
    "red_light_min": 3.0,                                 # R-11 (F-21)
    "text_size_min": 10,                                  # R-09 (F-09), web px
    "letter_spacing_em": 0.05,                            # R-08 provisional (F-07)
    # Glyph stacks served by the LINZ glyph endpoint that are already used by
    # the upstream style — we only map onto stacks known to exist.
    "deitalicise": {                                      # R-05 (F-05)
        "Open Sans Italic": "Open Sans Regular",
        "Open Sans Bold Italic": "Open Sans Bold",
        "Open Sans Light Italic": "Open Sans Regular",
        "Roboto Italic": "Open Sans Regular",
        "Roboto Bold Italic": "Roboto Bold",
        "Roboto Black Italic": "Roboto Black",
    },
}

SPRITE_ID = "nzat"


# ------------------------------------------------------------------ colour helpers

def lab_to_rgb(lab):
    L, a, b = lab
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    def finv(t):
        return t ** 3 if t > 6 / 29 else 3 * (6 / 29) ** 2 * (t - 4 / 29)

    x, y, z = finv(fx) * 0.95047, finv(fy), finv(fz) * 1.08883
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bb = 0.0557 * x - 0.2040 * y + 1.0570 * z
    return tuple(float(v) for v in pa.linear_to_srgb([r, g, bb]))


def fmt(rgb, a=1.0):
    r, g, b = (int(round(max(0, min(255, v)))) for v in rgb)
    return f"rgba({r}, {g}, {b}, {a:g})"


def darken_until(rgb, ok):
    """Lower CIELAB L* (hue/chroma kept) until ok(rgb) is True."""
    L, a, b = pa.rgb_to_lab(rgb)
    cur = rgb
    while not ok(cur) and L > 0:
        L -= 0.5
        cur = lab_to_rgb((L, a, b))
    return cur


# ------------------------------------------------------------------ build

class Builder:
    def __init__(self, style):
        self.doc = copy.deepcopy(style)
        self.style = self.doc.get("style", self.doc)
        self.log = []

    def note(self, rid, layer, what):
        self.log.append((rid, layer, what))

    def layer(self, lid):
        for l in self.style["layers"]:
            if l["id"] == lid:
                return l
        raise KeyError(lid)

    def insert_after(self, lid, new_layer, rid, why):
        idx = next(i for i, l in enumerate(self.style["layers"]) if l["id"] == lid)
        self.style["layers"].insert(idx + 1, new_layer)
        self.note(rid, new_layer["id"], f"added after `{lid}` — {why}")

    # R-03 ----------------------------------------------------------------
    def hillshade(self, multidirectional=False):
        for l in self.style["layers"]:
            if l["type"] != "hillshade":
                continue
            p = l["paint"]
            old = p.get("hillshade-illumination-direction")
            if not multidirectional:
                p["hillshade-illumination-direction"] = P["hillshade_direction"]
                self.note("R-03", l["id"], f"illumination direction {old} → {P['hillshade_direction']} (NNW)")
            else:
                p["hillshade-method"] = "multidirectional"
                p["hillshade-illumination-direction"] = [337.5, 292.5, 22.5]
                p["hillshade-illumination-altitude"] = [45, 45, 45]
                # Static colours: zoom-interpolated arrays are not assumed supported.
                p["hillshade-highlight-color"] = ["rgba(255,255,255,0.30)", "rgba(255,255,255,0.12)", "rgba(255,255,255,0.12)"]
                p["hillshade-shadow-color"] = ["rgba(12,12,12,0.45)", "rgba(12,12,12,0.18)", "rgba(12,12,12,0.18)"]
                p.pop("hillshade-accent-color", None)
                self.note("R-03", l["id"], "multidirectional: primary 337.5° + weaker 292.5°/22.5° fill lights "
                          "(F-16). Colours are provisional — tune visually (OQ-07)")

    # R-04 ----------------------------------------------------------------
    def contours(self):
        idx = self.layer("Contours-Index")
        idx["paint"]["line-color"] = P["contour_index"]
        idx["paint"]["line-opacity"] = {"stops": [[10, 0.6], [11, 1]]}
        idx["paint"]["line-width"] = P["contour_index_width"]
        self.note("R-04", "Contours-Index", f"colour → {P['contour_index']} (opaque), width ↑")
        halo = self.layer("Contours-Index-Halo")
        halo.setdefault("layout", {})["visibility"] = "none"
        self.note("R-04", "Contours-Index-Halo", "hidden — darker index line no longer needs a 10% offset shadow")
        for lid in ("Contours-All", "Contours-Designated", "Contours-Natural"):
            l = self.layer(lid)
            l["paint"]["line-color"] = P["contour_intermediate"]
            if lid == "Contours-All":
                l["paint"]["line-width"] = P["contour_intermediate_width"]
                l["paint"]["line-opacity"] = {"stops": [[13, 0.6], [14, 1]]}
            self.note("R-04", lid, f"colour → {P['contour_intermediate']} (opaque)")

    # R-10 ----------------------------------------------------------------
    def vegetation(self):
        self.layer("Vegetation-Scrub")["paint"]["fill-color"] = P["scrub"]
        self.note("R-10", "Vegetation-Scrub", f"fill → {P['scrub']}")
        sc = self.layer("Vegetation-Scatteredscrub")
        sc["paint"]["fill-color"] = P["scattered_scrub"]
        self.note("R-10", "Vegetation-Scatteredscrub", f"fill → {P['scattered_scrub']}")
        stipple = {
            "id": "NZAT-Vegetation-Scatteredscrub-Stipple",
            "type": "fill",
            "source": sc["source"],
            "source-layer": sc["source-layer"],
            "filter": copy.deepcopy(sc["filter"]),
            "minzoom": 11,
            "paint": {"fill-pattern": f"{SPRITE_ID}:scattered_stipple"},
        }
        self.insert_after(sc["id"], stipple, "R-10", "stipple so scattered scrub survives greyscale and CVD")

    # R-11 ----------------------------------------------------------------
    def closed_tracks(self):
        for lid in ("Transport-ClosedFootTracks-Shadow", "Transport-ClosedFootRouteTracks-Shadow"):
            self.layer(lid)["paint"]["line-color"] = P["closed_track_shadow"]
            self.note("R-11", lid, "red 40% shadow → dark casing (lightness, not hue)")
        for lid in ("All-ClosedFootTrack-Labels", "All-ClosedFootRouteTrack-Labels"):
            p = self.layer(lid)["paint"]
            p["text-halo-color"] = "rgba(255, 255, 255, 1)"
            p["text-opacity"] = 1
            if "icon-halo-color" in p:
                p["icon-halo-color"] = "rgba(255, 255, 255, 1)"
            self.note("R-11", lid, "red translucent halo → opaque white (restores text contrast)")
        anchor = "Transport-FootTracks"
        for subclass in ("foot_route_closed", "foot_closed"):
            src = self.layer("Transport-ClosedFootTracks-Shadow")
            bar = {
                "id": f"NZAT-Closed-{subclass}-Crossbar",
                "type": "line",
                "source": src["source"],
                "source-layer": src["source-layer"],
                "filter": ["all", ["==", "kind", "track"], ["==", "subclass", subclass]],
                "minzoom": 12,
                "paint": {"line-pattern": f"{SPRITE_ID}:closed_crossbar",
                          "line-width": {"stops": [[12, 5], [15, 7], [19, 10]]}},
            }
            self.insert_after(anchor, bar, "R-11", "cross-bar pattern: closed status carried by shape")

    # R-05, R-07, R-08, R-09, R-11 (text) -------------------------------------
    def text(self):
        for l in self.style["layers"]:
            if l["type"] != "symbol":
                continue
            lay, paint = l.setdefault("layout", {}), l.setdefault("paint", {})
            lid = l["id"]
            shield = "Highway-Labels" in lid  # white text drawn on an icon

            # R-05 de-italicise — on every layer that names a font, even if the
            # text-field is empty or data-driven, so no italic face is requested.
            f = lay.get("text-font")
            if isinstance(f, list) and f and all(isinstance(x, str) for x in f):
                nf = [P["deitalicise"].get(x, x) for x in f]
                if nf != f:
                    lay["text-font"] = nf
                    self.note("R-05", lid, f"font {f[0]} → {nf[0]}")

            if lay.get("text-field") in (None, ""):
                continue  # icon-only layer (empty text-field) — nothing to read

            # R-09 size floor
            ts = lay.get("text-size")
            if isinstance(ts, (int, float)) and ts < P["text_size_min"]:
                lay["text-size"] = P["text_size_min"]
                self.note("R-09", lid, f"text-size {ts} → {P['text_size_min']}")
            elif isinstance(ts, dict) and "stops" in ts:
                new = [[z, max(v, P["text_size_min"])] if isinstance(v, (int, float)) else [z, v] for z, v in ts["stops"]]
                if new != ts["stops"]:
                    ts["stops"] = new
                    self.note("R-09", lid, f"text-size stops floored at {P['text_size_min']}")

            # R-08 letter-spacing (provisional)
            if not shield and "text-letter-spacing" not in lay:
                lay["text-letter-spacing"] = P["letter_spacing_em"]
                self.note("R-08", lid, f"letter-spacing +{P['letter_spacing_em']} em (provisional)")

            if shield:
                continue
            tc = paint.get("text-color")
            tcol = pa.parse_colour(tc) if isinstance(tc, str) else None
            if not tcol:
                continue

            # R-07 opaque halo
            hc = paint.get("text-halo-color")
            hcol = pa.parse_colour(hc) if isinstance(hc, str) else None
            if hcol and hcol[3] < 1:
                paint["text-halo-color"] = fmt(hcol[:3], 1)
                self.note("R-07", lid, f"halo alpha {hcol[3]:g} → 1")
                hcol = (*hcol[:3], 1.0)
            behind = pa.composite(hcol, WHITE) if hcol else WHITE
            fg = pa.composite(tcol, behind)

            def contrast_ok(rgb):
                return pa.contrast_ratio(pa.rel_luminance(rgb), pa.rel_luminance(behind)) >= P["text_contrast_min"]

            def redlight_ok(rgb):
                return pa.contrast_ratio(pa.red_light_reflectance(rgb), pa.red_light_reflectance(behind)) >= P["red_light_min"]

            before_cr = pa.contrast_ratio(pa.rel_luminance(fg), pa.rel_luminance(behind))
            before_rl = pa.contrast_ratio(pa.red_light_reflectance(fg), pa.red_light_reflectance(behind))
            new = darken_until(fg, lambda c: contrast_ok(c) and redlight_ok(c))
            if new != fg:
                paint["text-color"] = fmt(new)
                if "text-opacity" in paint and isinstance(paint["text-opacity"], (int, float)):
                    paint["text-opacity"] = 1
                after_cr = pa.contrast_ratio(pa.rel_luminance(new), pa.rel_luminance(behind))
                after_rl = pa.contrast_ratio(pa.red_light_reflectance(new), pa.red_light_reflectance(behind))
                why = []
                if before_cr < P["text_contrast_min"]:
                    why.append(f"contrast {before_cr:.2f}→{after_cr:.2f}")
                if before_rl < P["red_light_min"]:
                    why.append(f"red-light {before_rl:.2f}→{after_rl:.2f}")
                rid = "R-07" if before_cr < P["text_contrast_min"] else "R-11"
                self.note(rid, lid, f"text {tc} → {fmt(new)} (L* lowered, hue kept; {', '.join(why)})")

    # sprite + metadata ------------------------------------------------------
    def sprite_and_meta(self, variant):
        old = self.style.get("sprite")
        self.style["sprite"] = [{"id": "default", "url": old}, {"id": SPRITE_ID, "url": "./sprites/nzat"}]
        self.note("infra", "(style)", f"sprite → multi-sprite: LINZ default + `{SPRITE_ID}` (patterns for R-10/R-11)")
        self.style["name"] = f"NZ Accessible Topo {variant}"
        self.style.setdefault("metadata", {})["nzat:derived-from"] = (
            "linz/basemaps-config config/style/topographic-v2.json (MIT, Crown copyright LINZ). "
            "Data: LINZ CC BY 4.0. See upstream/README.md.")
        self.style["id"] = f"nzat_{variant.replace('-', '_')}"
        if "id" in self.doc and self.doc is not self.style:
            self.doc["id"] = self.style["id"]
            self.doc["name"] = self.style["name"]


def build(multidirectional=False):
    variant = "v0-multidir" if multidirectional else "v0"
    b = Builder(json.load(open(UPSTREAM)))
    b.hillshade(multidirectional)
    b.contours()
    b.vegetation()
    b.closed_tracks()
    b.text()
    b.sprite_and_meta(variant)
    return variant, b


def write_changes(variant, b, path):
    by = {}
    for rid, lid, what in b.log:
        by.setdefault(rid, []).append((lid, what))
    out = [f"# Change log: accessible-{variant} (generated)", "",
           "Every change `tools/build_style.py` made to `upstream/linz-topographic-v2.json`, grouped by recommendation.",
           f"Total changes: {len(b.log)}.", ""]
    for rid in sorted(by):
        out.append(f"## {rid} ({len(by[rid])})\n")
        out += [f"- `{lid}` — {what}" for lid, what in by[rid]]
        out.append("")
    open(path, "w").write("\n".join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    for md in (False, True):
        variant, b = build(md)
        counts = {}
        for rid, _, _ in b.log:
            counts[rid] = counts.get(rid, 0) + 1
        print(variant, dict(sorted(counts.items())))
        if a.check_only:
            continue
        os.makedirs(os.path.join(ROOT, "styles"), exist_ok=True)
        os.makedirs(os.path.join(ROOT, "docs", "styles"), exist_ok=True)
        json.dump(b.doc, open(os.path.join(ROOT, "styles", f"accessible-{variant}.json"), "w"), indent=2, ensure_ascii=False)
        write_changes(variant, b, os.path.join(ROOT, "docs", "styles", f"accessible-{variant}-changes.md"))


if __name__ == "__main__":
    main()
