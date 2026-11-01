#!/usr/bin/env python3
"""
render_comparison.py — draw one synthetic terrain scene with two styles.

Every colour, width, opacity, font, size, halo and letter-spacing is read from
the style JSON (evaluated at zoom 14), so differences in the pictures are
differences in the styles. The terrain and features are SYNTHETIC — this is a
controlled test scene, not a rendering of real LINZ tiles. It is not MapLibre:
antialiasing, line joins and label placement differ from the real renderer.

Usage:
    python3 tools/render_comparison.py --fonts /path/to/google-fonts/ofl --out docs/visuals
"""
import argparse
import json
import math
import os
import sys

import contourpy
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import palette_audit as pa  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Z = 14          # zoom at which style values are evaluated
S = 2           # supersampling / retina factor
W, H = 620, 460  # logical px
M_PER_PX = 6.5   # ~z14 at NZ latitudes

# ----------------------------------------------------------------- style access

def interp(v, z=Z):
    if isinstance(v, dict) and "stops" in v:
        st = v["stops"]
        if z <= st[0][0]:
            return st[0][1]
        for (z0, a), (z1, b) in zip(st, st[1:]):
            if z0 <= z <= z1:
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    return a + (b - a) * (z - z0) / (z1 - z0)
                return a if z - z0 < z1 - z else b
        return st[-1][1]
    if isinstance(v, list) and v and v[0] == "interpolate":
        pts = v[3:]
        pairs = list(zip(pts[0::2], pts[1::2]))
        return interp({"stops": pairs}, z)
    return v


class Style:
    def __init__(self, path):
        d = json.load(open(path))
        self.s = d.get("style", d)
        self.by = {l["id"]: l for l in self.s["layers"]}

    def has(self, lid):
        l = self.by.get(lid)
        return l is not None and l.get("layout", {}).get("visibility") != "none"

    def p(self, lid, prop, default=None, z=Z):
        return interp(self.by[lid].get("paint", {}).get(prop, default), z)

    def lay(self, lid, prop, default=None, z=Z):
        return interp(self.by[lid].get("layout", {}).get(prop, default), z)

    def colour(self, lid, prop, z=Z):
        c = pa.parse_colour(self.p(lid, prop, z=z))
        op = self.p(lid, prop.split("-")[0] + "-opacity", 1, z=z)
        op = op if isinstance(op, (int, float)) else 1
        return (c[0], c[1], c[2], c[3] * op)


# ----------------------------------------------------------------- terrain

def make_dem():
    y, x = np.mgrid[0:H, 0:W].astype(float)
    z = 350 + 0.0 * x
    # main ridge NW→SE with a peak, side spurs, a valley with a lake basin
    def g(cx, cy, sx, sy, h, rot=0):
        c, s = math.cos(rot), math.sin(rot)
        dx, dy = x - cx, y - cy
        u, v = c * dx + s * dy, -s * dx + c * dy
        return h * np.exp(-(u ** 2 / (2 * sx ** 2) + v ** 2 / (2 * sy ** 2)))
    z += g(330, 170, 260, 55, 900, math.radians(30))
    z += g(400, 140, 70, 60, 450)                      # summit
    z += g(210, 300, 120, 35, 420, math.radians(-50))  # spur
    z += g(500, 330, 90, 40, 380, math.radians(70))    # spur
    z -= g(150, 120, 60, 45, 160)                      # basin (lake)
    z += 18 * np.sin(x / 23.0) * np.cos(y / 31.0)     # texture
    return z


def hillshade(z, azimuths, weights, alt=45, exag=1.0):
    """Lambertian shading. Azimuth is clockwise from north (map convention).
    Image rows run north→south, so the northward gradient is -d/drow.
    Verified: a hill lit from 315° is bright on its upper-left (NW) side."""
    dz_drow, dz_dcol = np.gradient(z * exag, M_PER_PX)
    dz_de, dz_dn = dz_dcol, -dz_drow
    n = np.stack([-dz_de, -dz_dn, np.ones_like(z)])
    n /= np.linalg.norm(n, axis=0)
    out = np.zeros_like(z)
    for az, w in zip(azimuths, weights):
        a, h = math.radians(az), math.radians(alt)
        l = np.array([math.sin(a) * math.cos(h), math.cos(a) * math.cos(h), math.sin(h)])
        out += w * np.clip(np.tensordot(l, n, axes=1), 0, 1)
    return out / sum(weights)


# ----------------------------------------------------------------- drawing

def rgba_t(c):
    return tuple(int(round(v)) for v in c[:3]) + (int(round(255 * c[3])),)


def layer_img():
    return Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))


def over(base, top):
    base.alpha_composite(top)


def poly(base, pts, colour):
    im = layer_img()
    ImageDraw.Draw(im).polygon([(x * S, y * S) for x, y in pts], fill=rgba_t(colour))
    over(base, im)


def pattern_fill(base, pts, tile):
    mask = Image.new("L", (W * S, H * S), 0)
    ImageDraw.Draw(mask).polygon([(x * S, y * S) for x, y in pts], fill=255)
    tiled = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    for ty in range(0, H * S, tile.height):
        for tx in range(0, W * S, tile.width):
            tiled.paste(tile, (tx, ty))
    clear = Image.new("RGBA", tiled.size, (0, 0, 0, 0))
    over(base, Image.composite(tiled, clear, mask))


def line(base, pts, colour, width, dash=None):
    """Draw a polyline. Translucent lines are drawn opaque then alpha-applied, so
    self-overlaps don't double up (as in MapLibre)."""
    im = layer_img()
    d = ImageDraw.Draw(im)
    w = max(1, int(round(width * S)))
    solid = tuple(int(round(v)) for v in colour[:3]) + (255,)
    P = [(x * S, y * S) for x, y in pts]
    if not dash:
        d.line(P, fill=solid, width=w, joint="curve")
    else:
        on, off = dash[0] * width * S, dash[1] * width * S
        acc, draw_on = 0.0, True
        for (x0, y0), (x1, y1) in zip(P, P[1:]):
            seg = math.hypot(x1 - x0, y1 - y0)
            t = 0.0
            while t < seg:
                lim = on if draw_on else off
                step = min(lim - acc, seg - t)
                if draw_on:
                    a, b = t / seg, (t + step) / seg
                    d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)],
                           fill=solid, width=w)
                t += step
                acc += step
                if acc >= lim - 1e-6:
                    acc, draw_on = 0.0, not draw_on
    a = im.getchannel("A").point(lambda v: int(v * colour[3]))
    im.putalpha(a)
    over(base, im)


def line_pattern(base, pts, tile, spacing_px):
    """Repeat a line-pattern sprite's bar perpendicular to the line."""
    d = ImageDraw.Draw(base)
    P = [(x * S, y * S) for x, y in pts]
    bar_h = tile.height  # already at S scale
    acc = spacing_px * S / 2
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
        nx, ny = -uy, ux
        t = acc
        while t < seg:
            cx, cy = x0 + ux * t, y0 + uy * t
            h = bar_h / 2
            d.line([(cx - nx * h, cy - ny * h), (cx + nx * h, cy + ny * h)], fill=(20, 20, 20, 255), width=2 * S // 2 + 1)
            t += spacing_px * S
        acc = t - seg


FONT_FILES = {
    "Open Sans": ("opensans/OpenSans[wdth,wght].ttf", "opensans/OpenSans-Italic[wdth,wght].ttf"),
}
WEIGHTS = {"Regular": 400, "Medium": 500, "Bold": 700, "Light": 300}


def font_for(name, size, fonts_dir):
    # "Open Sans Bold Italic" -> family Open Sans, weight Bold, italic True
    italic = "Italic" in name
    weight = next((w for k, w in WEIGHTS.items() if k in name), 400)
    reg, ita = FONT_FILES["Open Sans"]  # Roboto stacks are rendered with Open Sans metrics (noted in docs)
    f = ImageFont.truetype(os.path.join(fonts_dir, ita if italic else reg), int(round(size * S)))
    try:
        f.set_variation_by_axes([weight, 100])  # axes order: Weight, Width
    except Exception:
        pass
    return f


def label(base, xy, text, style, lid, fonts_dir, anchor="mm", z=Z):
    size = style.lay(lid, "text-size", 12, z=z)
    fname = style.lay(lid, "text-font", ["Open Sans Regular"], z=z)[0]
    spacing = style.lay(lid, "text-letter-spacing", 0, z=z) or 0
    f = font_for(fname, size, fonts_dir)
    tc = style.colour(lid, "text-color", z=z)
    hcv = style.p(lid, "text-halo-color", z=z)
    hc = pa.parse_colour(hcv) if isinstance(hcv, str) else None
    hw = style.p(lid, "text-halo-width", 1 if hc else 0, z=z) or 0
    x, y = xy[0] * S, xy[1] * S
    # Halo and text go in separate layers, alpha-composited: drawing text over
    # an opaque halo in one Pillow layer blends antialiased edges incorrectly.
    halo_im, text_im = layer_img(), layer_img()
    dh, dt = ImageDraw.Draw(halo_im), ImageDraw.Draw(text_im)
    sw = int(round(hw * S))
    if spacing:
        extra = spacing * size * S
        total = sum(f.getlength(ch) for ch in text) + extra * (len(text) - 1)
        cx = x - total / 2
        for ch in text:
            if hc and hw:
                dh.text((cx, y), ch, font=f, fill=rgba_t(hc), anchor="lm", stroke_width=sw, stroke_fill=rgba_t(hc))
            dt.text((cx, y), ch, font=f, fill=rgba_t(tc), anchor="lm")
            cx += f.getlength(ch) + extra
    else:
        if hc and hw:
            dh.text((x, y), text, font=f, fill=rgba_t(hc), anchor=anchor, stroke_width=sw, stroke_fill=rgba_t(hc))
        dt.text((x, y), text, font=f, fill=rgba_t(tc), anchor=anchor)
    over(base, halo_im)
    over(base, text_im)


# ----------------------------------------------------------------- scene

LAKE = [(95, 95), (150, 78), (205, 100), (210, 140), (170, 165), (115, 155), (88, 128)]
SCRUB = [(250, 250), (330, 230), (380, 270), (360, 330), (290, 345), (240, 310)]
SCATTERED = [(380, 270), (470, 250), (540, 290), (520, 360), (430, 370), (360, 330)]
RIVER = [(150, 165), (170, 220), (160, 280), (190, 340), (175, 400), (200, 460)]
HIGHWAY = [(0, 430), (120, 415), (250, 440), (400, 420), (620, 445)]
PIPELINE = [(620, 120), (520, 160), (450, 210), (380, 250)]
TRACK = [(205, 120), (260, 140), (320, 150), (395, 145)]          # to summit
CLOSED = [(400, 150), (460, 200), (520, 230), (600, 260)]          # closed beyond summit


def render(style_path, fonts_dir, sprites_dir, dem, shade):
    st = Style(style_path)
    base = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))

    # hillshade (same strength both sides; only direction/method differ)
    dark = ((1 - shade) * 0.45 * 255).astype(np.uint8)
    hs = Image.new("RGBA", (W, H), (12, 12, 12, 0))
    hs.putalpha(Image.fromarray(dark))
    over(base, hs.resize((W * S, H * S), Image.BILINEAR))

    poly(base, SCRUB, st.colour("Vegetation-Scrub", "fill-color"))
    poly(base, SCATTERED, st.colour("Vegetation-Scatteredscrub", "fill-color"))
    if st.has("NZAT-Vegetation-Scatteredscrub-Stipple"):
        tile = Image.open(os.path.join(sprites_dir, "nzat@2x.png")).crop((0, 0, 32, 32))
        pattern_fill(base, SCATTERED, tile)
    poly(base, LAKE, st.colour("Water-Lake", "fill-color"))

    # contours
    gen = contourpy.contour_generator(z=dem)
    for lvl in range(400, 1700, 20):
        index = lvl % 100 == 0
        lid = "Contours-Index" if index else "Contours-All"
        c = st.colour(lid, "line-color")
        w = st.p(lid, "line-width", 1)
        for seg in gen.lines(lvl):
            if len(seg) > 2:
                line(base, [tuple(p) for p in seg[::2]], c, w)

    line(base, RIVER, st.colour("Waterway-Waterfall-Ln", "line-color"), 1.5)  # water line colour
    line(base, PIPELINE, st.colour("Poi-Pipeline", "line-color"), st.p("Poi-Pipeline", "line-width", 1))
    line(base, HIGHWAY, st.colour("Transport-HWY-Casing", "line-color"), st.p("Transport-HWY-Casing", "line-width"))
    line(base, HIGHWAY, st.colour("Transport-HWY", "line-color"), st.p("Transport-HWY", "line-width"))

    tw = st.p("Transport-FootTracks", "line-width", 1.5)
    tdash = st.p("Transport-FootTracks", "line-dasharray")
    line(base, TRACK, st.colour("Transport-FootTracks-Shadow", "line-color"), st.p("Transport-FootTracks-Shadow", "line-width"))
    line(base, TRACK, st.colour("Transport-FootTracks", "line-color"), tw, tdash)
    line(base, CLOSED, st.colour("Transport-ClosedFootTracks-Shadow", "line-color"),
         st.p("Transport-ClosedFootTracks-Shadow", "line-width"))
    line(base, CLOSED, st.colour("Transport-FootTracks", "line-color"), tw, tdash)
    if st.has("NZAT-Closed-foot_closed-Crossbar"):
        tile = Image.open(os.path.join(sprites_dir, "nzat@2x.png")).crop((36, 0, 60, 16))
        line_pattern(base, CLOSED, tile, 12)

    # labels
    label(base, (150, 122), "Lake Ōhau", st, "All-Lake-Names", fonts_dir)
    label(base, (215, 200), "Ōpito Stream", st, "All-River-Names", fonts_dir)
    label(base, (405, 120), "Pāpaka 1432", st, "Place-Label-Peak-16", fonts_dir)
    label(base, (300, 168), "Kōwhai Hut", st, "Poi-Hut-Label", fonts_dir)
    label(base, (500, 395), "Pā site", st, "Poi-Historic-Site", fonts_dir, z=17)  # only shown from z17
    label(base, (555, 215), "closed", st, "Poi-Hut-Label", fonts_dir)
    label(base, (95, 330), "800", st, "Contours-Label", fonts_dir)
    return base.convert("RGB")


# ----------------------------------------------------------------- simulations

SIMS = {
    "normal vision": None,
    "protanopia": pa.MACHADO["protanopia"],
    "deuteranopia": pa.MACHADO["deuteranopia"],
    "tritanopia": pa.MACHADO["tritanopia"],
    "greyscale": np.array([[0.2126, 0.7152, 0.0722]] * 3),
    "red headtorch": np.array([[1, 0, 0]] * 3),
}


def simulate(img, m):
    if m is None:
        return img
    a = np.asarray(img).astype(float)
    lin = pa.srgb_to_linear(a)
    out = pa.linear_to_srgb(lin @ np.asarray(m).T)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def caption(img, text, fonts_dir, size=15):
    f = ImageFont.truetype(os.path.join(fonts_dir, FONT_FILES["Open Sans"][0]), size * S)
    try:
        f.set_variation_by_axes([700, 100])
    except Exception:
        pass
    pad = 30 * S
    out = Image.new("RGB", (img.width, img.height + pad), (245, 245, 243))
    out.paste(img, (0, pad))
    ImageDraw.Draw(out).text((10 * S, pad / 2), text, font=f, fill=(20, 20, 20), anchor="lm")
    return out


def grid(rows, gap=6):
    h = sum(r[0].height for r in rows) + gap * S * (len(rows) - 1)
    w = sum(i.width for i in rows[0]) + gap * S * (len(rows[0]) - 1)
    out = Image.new("RGB", (w, h), (255, 255, 255))
    y = 0
    for r in rows:
        x = 0
        for im in r:
            out.paste(im, (x, y))
            x += im.width + gap * S
        y += r[0].height + gap * S
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, help="google/fonts 'ofl' directory")
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "visuals"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sprites = os.path.join(ROOT, "styles", "sprites")
    dem = make_dem()
    shade_nw = hillshade(dem, [315], [1])
    shade_nnw = hillshade(dem, [337.5], [1])
    shade_multi = hillshade(dem, [337.5, 292.5, 22.5], [0.6, 0.2, 0.2])

    up = render(os.path.join(ROOT, "upstream", "linz-topographic-v2.json"), a.fonts, sprites, dem, shade_nw)
    v0 = render(os.path.join(ROOT, "styles", "accessible-v0.json"), a.fonts, sprites, dem, shade_nnw)

    # 1. side by side, normal vision
    grid([[caption(up, "LINZ topographic-v2", a.fonts), caption(v0, "accessible-v0", a.fonts)]]).save(
        os.path.join(a.out, "01-side-by-side.png"))

    # 2. simulations
    rows = []
    for name, m in SIMS.items():
        if m is None:
            continue
        rows.append([caption(simulate(up, m), f"LINZ — {name}", a.fonts),
                     caption(simulate(v0, m), f"accessible-v0 — {name}", a.fonts)])
    grid(rows).save(os.path.join(a.out, "02-simulations.png"))

    # 3. relief lighting only
    def shade_img(sh, t):
        g = Image.fromarray((sh * 255).astype(np.uint8)).convert("RGB").resize((W * S, H * S), Image.BILINEAR)
        return caption(g, t, a.fonts)
    grid([[shade_img(shade_nw, "315° NW (Topo50 / LINZ today)"), shade_img(shade_nnw, "337.5° NNW (R-03)")],
          [shade_img(shade_multi, "Multidirectional 337.5° + 292.5° + 22.5°"),
           shade_img(hillshade(dem, [135], [1]), "135° SE — control: invites terrain reversal")]]).save(
        os.path.join(a.out, "03-relief-lighting.png"))

    # 4. label close-up at true 2x pixels (no resampling)
    box = (60 * S, 90 * S, 470 * S, 215 * S)
    grid([[caption(up.crop(box), "LINZ — labels at 2×", a.fonts)],
          [caption(v0.crop(box), "accessible-v0 — labels at 2×", a.fonts)]]).save(
        os.path.join(a.out, "04-labels-closeup.png"))
    print("wrote", sorted(os.listdir(a.out)))


if __name__ == "__main__":
    main()
