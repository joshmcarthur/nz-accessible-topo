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
STYLE_PATH = os.path.join(ROOT, "tools", "style-topo50.json")
WHITE = (255, 255, 255)

# ------------------------------------------------------------------ parameters
# Values come from docs/recommendations.md and docs/palette-experiments/proposed-v0.md.
P = {
    "hillshade_direction": 337.5,                         # R-03 (F-14, F-15)
    "contour_index": "#8A4F1C",                           # R-04
    "contour_intermediate": "#C4814B",                    # R-04 rev. (log 0020): lightest same-hue brown ≥3.2:1
    "contour_index_width": {"stops": [[10, 0.8], [12, 1.2], [15, 1.8]]},
    "contour_intermediate_width": {"stops": [[12, 0.6], [16, 0.9]]},  # thinner: dense slopes read as texture
    "closed_track_shadow": "rgba(26, 26, 26, 0.55)",      # R-11
    "red_light_min": 3.0,                                 # R-11 (F-21)
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


def load_style_rules(path=None):
    with open(path or STYLE_PATH, encoding="utf-8") as handle:
        return json.load(handle)


RULES = load_style_rules()


def is_place_name(layer_id, text_field):
    """A place-name label is a Place-Label layer with text to read."""
    if text_field in (None, ""):
        return False
    return isinstance(layer_id, str) and layer_id.startswith("Place-Label-")


def label_floor_px(layer_id, text_field, rules=None):
    """Return the web size floor in px for this label."""
    labels = (rules or RULES)["labels"]
    if is_place_name(layer_id, text_field):
        return labels["place_name_floor_px"]
    return labels["web_floor_px"]


def floor_text_size(size, floor):
    """Raise one text size to the floor. Keep a size that is already high enough."""
    if isinstance(size, (int, float)) and not isinstance(size, bool) and size < floor:
        return floor
    return size


def place_rank_size(layer_id, rules=None):
    """Return the place-rank size in px. A layer with no rank returns None."""
    labels = (rules or RULES)["labels"]
    for rank in labels["place_hierarchy"]:
        if layer_id in rank["layers"]:
            return rank["size_px"]
    return None


def hierarchy_ratios(ranks):
    """Return the size ratio of each rank to the rank before it."""
    sizes = [rank["size_px"] for rank in ranks]
    return [sizes[i + 1] / sizes[i] for i in range(len(sizes) - 1)]


def resolved_text_size(size, floor, rank_size):
    """Return the size after the floor. A place rank replaces that size."""
    sized = floor_text_size(size, floor)
    if rank_size is None:
        return sized
    return floor_text_size(rank_size, floor)


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


def text_contrast_min(rules=None):
    """Return the label contrast floor. The number lives in tools/style-topo50.json."""
    return (rules or RULES)["label_contrast"]["min_ratio"]


def halo_alpha(rules=None):
    """Return the opaque halo alpha. The number lives in tools/style-topo50.json."""
    return (rules or RULES)["label_contrast"]["halo_alpha"]


def vegetation_fill(kind, rules=None):
    """Return the opaque vector fill for a vegetation class. Colour lives in tools/style-topo50.json."""
    colour = (rules or RULES)["vegetation"][kind]["colour"]
    return fmt(pa.parse_colour(colour)[:3])


def darken_for_text(rgb, behind, min_ratio):
    """Lower L* until the ink meets min_ratio against behind. Keep hue."""
    def ok(colour):
        return pa.contrast_ratio(pa.rel_luminance(colour), pa.rel_luminance(behind)) >= min_ratio

    return darken_until(rgb, ok)


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
        scrub = vegetation_fill("scrub")
        scattered = vegetation_fill("scattered")
        self.layer("Vegetation-Scrub")["paint"]["fill-color"] = scrub
        self.note("R-10", "Vegetation-Scrub", f"fill → {scrub}")
        sc = self.layer("Vegetation-Scatteredscrub")
        sc["paint"]["fill-color"] = scattered
        self.note("R-10", "Vegetation-Scatteredscrub", f"fill → {scattered}")
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

            # R-09 size floor and place ranks. The numbers live in tools/style-topo50.json.
            floor = label_floor_px(lid, lay.get("text-field"))
            ts = lay.get("text-size")
            rank_size = place_rank_size(lid)
            if isinstance(ts, (int, float)) and not isinstance(ts, bool):
                new_ts = resolved_text_size(ts, floor, rank_size)
                if new_ts != ts:
                    lay["text-size"] = new_ts
                    self.note("R-09", lid, f"text-size {ts} → {new_ts}")
            elif isinstance(ts, dict) and "stops" in ts:
                new = [
                    [z, floor_text_size(v, floor)] if isinstance(v, (int, float)) and not isinstance(v, bool) else [z, v]
                    for z, v in ts["stops"]
                ]
                if new != ts["stops"]:
                    ts["stops"] = new
                    self.note("R-09", lid, f"text-size stops floored at {floor}")

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

            # R-07 opaque halo. The floor and the alpha live in tools/style-topo50.json.
            contrast_floor = text_contrast_min()
            target_alpha = halo_alpha()
            hc = paint.get("text-halo-color")
            hcol = pa.parse_colour(hc) if isinstance(hc, str) else None
            if hcol and hcol[3] < target_alpha:
                paint["text-halo-color"] = fmt(hcol[:3], target_alpha)
                self.note("R-07", lid, f"halo alpha {hcol[3]:g} → {target_alpha:g}")
                hcol = (*hcol[:3], float(target_alpha))
            behind = pa.composite(hcol, WHITE) if hcol else WHITE
            fg = pa.composite(tcol, behind)

            def contrast_ok(rgb):
                return pa.contrast_ratio(pa.rel_luminance(rgb), pa.rel_luminance(behind)) >= contrast_floor

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
                if before_cr < contrast_floor:
                    why.append(f"contrast {before_cr:.2f}→{after_cr:.2f}")
                if before_rl < P["red_light_min"]:
                    why.append(f"red-light {before_rl:.2f}→{after_rl:.2f}")
                rid = "R-07" if before_cr < contrast_floor else "R-11"
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
