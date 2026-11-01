#!/usr/bin/env python3
"""simulate_image.py — apply the audit's vision/lighting simulations to a real map image.

Uses the same models as palette_audit.py: Machado et al. (2009) dichromacy in
linear RGB, greyscale (relative luminance), and a red-headtorch model
(reflectance in the red channel only).

Usage: python3 tools/simulate_image.py IN_IMAGE OUT.png [--crop x0,y0,x1,y1] [--title "..."]
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import palette_audit as pa  # noqa: E402

SIMS = [("normal vision", None),
        ("deuteranopia", pa.MACHADO["deuteranopia"]),
        ("protanopia", pa.MACHADO["protanopia"]),
        ("tritanopia", pa.MACHADO["tritanopia"]),
        ("greyscale / photocopy", np.array([[0.2126, 0.7152, 0.0722]] * 3)),
        ("red headtorch", np.array([[1.0, 0, 0]] * 3))]


def apply(img, m):
    if m is None:
        return img
    lin = pa.srgb_to_linear(np.asarray(img).astype(float))
    return Image.fromarray(np.clip(pa.linear_to_srgb(lin @ m.T), 0, 255).astype(np.uint8))


def load_image(path):
    if path.lower().endswith((".tif", ".tiff")):
        import tifffile  # WEBP-compressed GeoTIFFs need tifffile + imagecodecs
        return Image.fromarray(tifffile.imread(path)[..., :3])
    return Image.open(path).convert("RGB")


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
        out.paste(apply(img, m), (x, y + pad))
    out.save(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
