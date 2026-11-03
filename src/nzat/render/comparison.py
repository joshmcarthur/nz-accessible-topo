import math
import os

import contourpy
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from nzat.colour.parse_colour import parse_colour
from nzat.render.hillshade import H, S, W, Z
from nzat.render.style import Style

LAKE = [
    (95, 95),
    (150, 78),
    (205, 100),
    (210, 140),
    (170, 165),
    (115, 155),
    (88, 128),
]
SCRUB = [(250, 250), (330, 230), (380, 270), (360, 330), (290, 345), (240, 310)]
SCATTERED = [(380, 270), (470, 250), (540, 290), (520, 360), (430, 370), (360, 330)]
RIVER = [(150, 165), (170, 220), (160, 280), (190, 340), (175, 400), (200, 460)]
HIGHWAY = [(0, 430), (120, 415), (250, 440), (400, 420), (620, 445)]
PIPELINE = [(620, 120), (520, 160), (450, 210), (380, 250)]
TRACK = [(205, 120), (260, 140), (320, 150), (395, 145)]
CLOSED = [(400, 150), (460, 200), (520, 230), (600, 260)]

FONT_FILES = {
    "Open Sans": (
        "opensans/OpenSans[wdth,wght].ttf",
        "opensans/OpenSans-Italic[wdth,wght].ttf",
    ),
}
WEIGHTS = {"Regular": 400, "Medium": 500, "Bold": 700, "Light": 300}


def _rgba_t(c):
    return tuple(int(round(v)) for v in c[:3]) + (int(round(255 * c[3])),)


def _layer_img():
    return Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))


def _over(base, top):
    base.alpha_composite(top)


def _poly(base, pts, colour):
    im = _layer_img()
    ImageDraw.Draw(im).polygon([(x * S, y * S) for x, y in pts], fill=_rgba_t(colour))
    _over(base, im)


def _pattern_fill(base, pts, tile):
    mask = Image.new("L", (W * S, H * S), 0)
    ImageDraw.Draw(mask).polygon([(x * S, y * S) for x, y in pts], fill=255)
    tiled = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    for ty in range(0, H * S, tile.height):
        for tx in range(0, W * S, tile.width):
            tiled.paste(tile, (tx, ty))
    clear = Image.new("RGBA", tiled.size, (0, 0, 0, 0))
    _over(base, Image.composite(tiled, clear, mask))


def _line(base, pts, colour, width, dash=None):
    """Draw a polyline. Translucent lines are drawn opaque then alpha-applied, so
    self-overlaps don't double up (as in MapLibre)."""
    im = _layer_img()
    d = ImageDraw.Draw(im)
    w = max(1, int(round(width * S)))
    solid = tuple(int(round(v)) for v in colour[:3]) + (255,)
    P = [(x * S, y * S) for x, y in pts]
    if not dash:
        d.line(P, fill=solid, width=w, joint="curve")
    else:
        on, off = dash[0] * width * S, dash[1] * width * S
        acc, draw_on = 0.0, True
        for (x0, y0), (x1, y1) in zip(P, P[1:], strict=False):
            seg = math.hypot(x1 - x0, y1 - y0)
            t = 0.0
            while t < seg:
                lim = on if draw_on else off
                step = min(lim - acc, seg - t)
                if draw_on:
                    a, b = t / seg, (t + step) / seg
                    d.line(
                        [
                            (x0 + (x1 - x0) * a, y0 + (y1 - y0) * a),
                            (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b),
                        ],
                        fill=solid,
                        width=w,
                    )
                t += step
                acc += step
                if acc >= lim - 1e-6:
                    acc, draw_on = 0.0, not draw_on
    a = im.getchannel("A").point(lambda v: int(v * colour[3]))
    im.putalpha(a)
    _over(base, im)


def _line_pattern(base, pts, tile, spacing_px):
    """Repeat a line-pattern sprite's bar perpendicular to the line."""
    d = ImageDraw.Draw(base)
    P = [(x * S, y * S) for x, y in pts]
    bar_h = tile.height
    acc = spacing_px * S / 2
    for (x0, y0), (x1, y1) in zip(P, P[1:], strict=False):
        seg = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
        nx, ny = -uy, ux
        t = acc
        while t < seg:
            cx, cy = x0 + ux * t, y0 + uy * t
            h = bar_h / 2
            d.line(
                [(cx - nx * h, cy - ny * h), (cx + nx * h, cy + ny * h)],
                fill=(20, 20, 20, 255),
                width=2 * S // 2 + 1,
            )
            t += spacing_px * S
        acc = t - seg


def _font_for(name, size, fonts_dir):
    italic = "Italic" in name
    weight = next((w for k, w in WEIGHTS.items() if k in name), 400)
    reg, ita = FONT_FILES["Open Sans"]
    f = ImageFont.truetype(
        os.path.join(fonts_dir, ita if italic else reg), int(round(size * S))
    )
    try:
        f.set_variation_by_axes([weight, 100])
    except Exception:
        pass
    return f


def _label(base, xy, text, style, lid, fonts_dir, anchor="mm", z=Z):
    size = style.lay(lid, "text-size", 12, z=z)
    fname = style.lay(lid, "text-font", ["Open Sans Regular"], z=z)[0]
    spacing = style.lay(lid, "text-letter-spacing", 0, z=z) or 0
    f = _font_for(fname, size, fonts_dir)
    tc = style.colour(lid, "text-color", z=z)
    hcv = style.p(lid, "text-halo-color", z=z)
    hc = parse_colour(hcv) if isinstance(hcv, str) else None
    hw = style.p(lid, "text-halo-width", 1 if hc else 0, z=z) or 0
    x, y = xy[0] * S, xy[1] * S
    halo_im, text_im = _layer_img(), _layer_img()
    dh, dt = ImageDraw.Draw(halo_im), ImageDraw.Draw(text_im)
    sw = int(round(hw * S))
    if spacing:
        extra = spacing * size * S
        total = sum(f.getlength(ch) for ch in text) + extra * (len(text) - 1)
        cx = x - total / 2
        for ch in text:
            if hc and hw:
                dh.text(
                    (cx, y),
                    ch,
                    font=f,
                    fill=_rgba_t(hc),
                    anchor="lm",
                    stroke_width=sw,
                    stroke_fill=_rgba_t(hc),
                )
            dt.text((cx, y), ch, font=f, fill=_rgba_t(tc), anchor="lm")
            cx += f.getlength(ch) + extra
    else:
        if hc and hw:
            dh.text(
                (x, y),
                text,
                font=f,
                fill=_rgba_t(hc),
                anchor=anchor,
                stroke_width=sw,
                stroke_fill=_rgba_t(hc),
            )
        dt.text((x, y), text, font=f, fill=_rgba_t(tc), anchor=anchor)
    _over(base, halo_im)
    _over(base, text_im)


def render(style_path, fonts_dir, sprites_dir, dem, shade):
    st = Style(style_path)
    base = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))

    dark = ((1 - shade) * 0.45 * 255).astype(np.uint8)
    hs = Image.new("RGBA", (W, H), (12, 12, 12, 0))
    hs.putalpha(Image.fromarray(dark))
    _over(base, hs.resize((W * S, H * S), Image.BILINEAR))

    _poly(base, SCRUB, st.colour("Vegetation-Scrub", "fill-color"))
    _poly(base, SCATTERED, st.colour("Vegetation-Scatteredscrub", "fill-color"))
    if st.has("NZAT-Vegetation-Scatteredscrub-Stipple"):
        tile = Image.open(os.path.join(sprites_dir, "nzat@2x.png")).crop((0, 0, 32, 32))
        _pattern_fill(base, SCATTERED, tile)
    _poly(base, LAKE, st.colour("Water-Lake", "fill-color"))

    gen = contourpy.contour_generator(z=dem)
    for lvl in range(400, 1700, 20):
        index = lvl % 100 == 0
        lid = "Contours-Index" if index else "Contours-All"
        c = st.colour(lid, "line-color")
        w = st.p(lid, "line-width", 1)
        for seg in gen.lines(lvl):
            if len(seg) > 2:
                _line(base, [tuple(p) for p in seg[::2]], c, w)

    _line(base, RIVER, st.colour("Waterway-Waterfall-Ln", "line-color"), 1.5)
    _line(
        base,
        PIPELINE,
        st.colour("Poi-Pipeline", "line-color"),
        st.p("Poi-Pipeline", "line-width", 1),
    )
    _line(
        base,
        HIGHWAY,
        st.colour("Transport-HWY-Casing", "line-color"),
        st.p("Transport-HWY-Casing", "line-width"),
    )
    _line(
        base,
        HIGHWAY,
        st.colour("Transport-HWY", "line-color"),
        st.p("Transport-HWY", "line-width"),
    )

    tw = st.p("Transport-FootTracks", "line-width", 1.5)
    tdash = st.p("Transport-FootTracks", "line-dasharray")
    _line(
        base,
        TRACK,
        st.colour("Transport-FootTracks-Shadow", "line-color"),
        st.p("Transport-FootTracks-Shadow", "line-width"),
    )
    _line(base, TRACK, st.colour("Transport-FootTracks", "line-color"), tw, tdash)
    _line(
        base,
        CLOSED,
        st.colour("Transport-ClosedFootTracks-Shadow", "line-color"),
        st.p("Transport-ClosedFootTracks-Shadow", "line-width"),
    )
    _line(base, CLOSED, st.colour("Transport-FootTracks", "line-color"), tw, tdash)
    if st.has("NZAT-Closed-foot_closed-Crossbar"):
        tile = Image.open(os.path.join(sprites_dir, "nzat@2x.png")).crop(
            (36, 0, 60, 16)
        )
        _line_pattern(base, CLOSED, tile, 12)

    _label(base, (150, 122), "Lake Ōhau", st, "All-Lake-Names", fonts_dir)
    _label(base, (215, 200), "Ōpito Stream", st, "All-River-Names", fonts_dir)
    _label(base, (405, 120), "Pāpaka 1432", st, "Place-Label-Peak-16", fonts_dir)
    _label(base, (300, 168), "Kōwhai Hut", st, "Poi-Hut-Label", fonts_dir)
    _label(base, (500, 395), "Pā site", st, "Poi-Historic-Site", fonts_dir, z=17)
    _label(base, (555, 215), "closed", st, "Poi-Hut-Label", fonts_dir)
    _label(base, (95, 330), "800", st, "Contours-Label", fonts_dir)
    return base.convert("RGB")


def caption(img, text, fonts_dir, size=15):
    f = ImageFont.truetype(
        os.path.join(fonts_dir, FONT_FILES["Open Sans"][0]), size * S
    )
    try:
        f.set_variation_by_axes([700, 100])
    except Exception:
        pass
    pad = 30 * S
    out = Image.new("RGB", (img.width, img.height + pad), (245, 245, 243))
    out.paste(img, (0, pad))
    ImageDraw.Draw(out).text(
        (10 * S, pad / 2), text, font=f, fill=(20, 20, 20), anchor="lm"
    )
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
