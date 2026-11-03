import json
import os

from PIL import Image, ImageDraw

from nzat.paths import ROOT

OUT = ROOT / "styles" / "sprites"


def _stipple(s):
    im = Image.new("RGBA", (16 * s, 16 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x, y in [(3, 3), (11, 7), (5, 12)]:
        r = 1.1 * s
        d.ellipse([x * s - r, y * s - r, x * s + r, y * s + r], fill=(46, 92, 40, 230))
    return im


def _crossbar(s):
    im = Image.new("RGBA", (12 * s, 8 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([5 * s, 0, 7 * s - 1, 8 * s - 1], fill=(20, 20, 20, 255))
    return im


_IMAGES = {"scattered_stipple": _stipple, "closed_crossbar": _crossbar}


def build(scale):
    ims = {k: f(scale) for k, f in _IMAGES.items()}
    width = sum(i.width for i in ims.values()) + 2 * scale * (len(ims) - 1)
    height = max(i.height for i in ims.values())
    sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    meta, x = {}, 0
    for k, im in ims.items():
        sheet.paste(im, (x, 0))
        meta[k] = {
            "x": x,
            "y": 0,
            "width": im.width,
            "height": im.height,
            "pixelRatio": scale,
        }
        x += im.width + 2 * scale
    suffix = "" if scale == 1 else f"@{scale}x"
    sheet.save(os.path.join(OUT, f"nzat{suffix}.png"))
    json.dump(meta, open(os.path.join(OUT, f"nzat{suffix}.json"), "w"), indent=1)


def main():
    os.makedirs(OUT, exist_ok=True)
    for s in (1, 2):
        build(s)
    print("wrote", sorted(os.listdir(OUT)))
