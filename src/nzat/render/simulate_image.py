import argparse

from PIL import Image, ImageDraw, ImageFont

from nzat.colour.apply_matrix import GREYSCALE, RED_HEADTORCH, apply_matrix
from nzat.colour.simulate import MACHADO
from nzat.render.load_image import load_image

SIMS = [
    ("normal vision", None),
    ("deuteranopia", MACHADO["deuteranopia"]),
    ("protanopia", MACHADO["protanopia"]),
    ("tritanopia", MACHADO["tritanopia"]),
    ("greyscale / photocopy", GREYSCALE),
    ("red headtorch", RED_HEADTORCH),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--crop")
    ap.add_argument("--font", default=None)
    a = ap.parse_args()
    img = load_image(a.src)
    if a.crop:
        img = img.crop(tuple(int(v) for v in a.crop.split(",")))
    font = ImageFont.truetype(a.font, 22) if a.font else ImageFont.load_default()
    pad, gap = 34, 8
    w, h = img.width, img.height
    out = Image.new("RGB", (2 * w + gap, 3 * (h + pad) + 2 * gap), "white")
    d = ImageDraw.Draw(out)
    for i, (name, m) in enumerate(SIMS):
        x, y = (i % 2) * (w + gap), (i // 2) * (h + pad + gap)
        d.text((x + 6, y + 6), name, font=font, fill=(20, 20, 20))
        out.paste(apply_matrix(img, m), (x, y + pad))
    out.save(a.out)
    print("wrote", a.out)
