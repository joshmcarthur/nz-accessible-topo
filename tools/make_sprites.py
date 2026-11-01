#!/usr/bin/env python3
"""make_sprites.py — generate the `nzat` sprite sheet (1x and 2x) used by R-10/R-11.

Images are drawn procedurally so they are reviewable as code:
  scattered_stipple  16×16 fill pattern: sparse dark-green dots (R-10)
  closed_crossbar    12×8 line pattern: a dark bar across the track every 12 px (R-11)
"""
import json
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "styles", "sprites")


def stipple(s):
    im = Image.new("RGBA", (16 * s, 16 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x, y in [(3, 3), (11, 7), (5, 12)]:  # offset grid avoids visible rows
        r = 1.1 * s
        d.ellipse([x * s - r, y * s - r, x * s + r, y * s + r], fill=(46, 92, 40, 230))
    return im


def crossbar(s):
    im = Image.new("RGBA", (12 * s, 8 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([5 * s, 0, 7 * s - 1, 8 * s - 1], fill=(20, 20, 20, 255))
    return im


IMAGES = {"scattered_stipple": stipple, "closed_crossbar": crossbar}


def build(scale):
    ims = {k: f(scale) for k, f in IMAGES.items()}
    width = sum(i.width for i in ims.values()) + 2 * scale * (len(ims) - 1)
    height = max(i.height for i in ims.values())
    sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    meta, x = {}, 0
    for k, im in ims.items():
        sheet.paste(im, (x, 0))
        meta[k] = {"x": x, "y": 0, "width": im.width, "height": im.height, "pixelRatio": scale}
        x += im.width + 2 * scale
    suffix = "" if scale == 1 else f"@{scale}x"
    sheet.save(os.path.join(OUT, f"nzat{suffix}.png"))
    json.dump(meta, open(os.path.join(OUT, f"nzat{suffix}.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for s in (1, 2):
        build(s)
    print("wrote", sorted(os.listdir(OUT)))
