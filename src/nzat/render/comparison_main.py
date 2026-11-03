import argparse
import os

import numpy as np
from PIL import Image

from nzat.colour.apply_matrix import GREYSCALE, RED_HEADTORCH, apply_matrix
from nzat.colour.simulate import MACHADO
from nzat.paths import ROOT, UPSTREAM
from nzat.render.comparison import caption, grid, render
from nzat.render.hillshade import H, S, W, hillshade
from nzat.render.make_dem import make_dem

SIMS = {
    "normal vision": None,
    "protanopia": MACHADO["protanopia"],
    "deuteranopia": MACHADO["deuteranopia"],
    "tritanopia": MACHADO["tritanopia"],
    "greyscale": GREYSCALE,
    "red headtorch": RED_HEADTORCH,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, help="google/fonts 'ofl' directory")
    ap.add_argument("--out", default=str(ROOT / "docs" / "visuals"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sprites = str(ROOT / "styles" / "sprites")
    dem = make_dem()
    shade_nw = hillshade(dem, [315], [1])
    shade_nnw = hillshade(dem, [337.5], [1])
    shade_multi = hillshade(dem, [337.5, 292.5, 22.5], [0.6, 0.2, 0.2])

    up = render(str(UPSTREAM), a.fonts, sprites, dem, shade_nw)
    v0 = render(
        str(ROOT / "styles" / "accessible-v0.json"), a.fonts, sprites, dem, shade_nnw
    )

    os.makedirs(os.path.join(a.out, "scenes"), exist_ok=True)
    up.save(os.path.join(a.out, "scenes", "synthetic-linz.png"))
    v0.save(os.path.join(a.out, "scenes", "synthetic-accessible-v0.png"))

    grid(
        [
            [
                caption(up, "LINZ topographic-v2", a.fonts),
                caption(v0, "accessible-v0", a.fonts),
            ]
        ]
    ).save(os.path.join(a.out, "01-side-by-side.png"))

    rows = []
    for name, m in SIMS.items():
        if m is None:
            continue
        rows.append(
            [
                caption(apply_matrix(up, m), f"LINZ — {name}", a.fonts),
                caption(apply_matrix(v0, m), f"accessible-v0 — {name}", a.fonts),
            ]
        )
    grid(rows).save(os.path.join(a.out, "02-simulations.png"))

    def shade_img(sh, t):
        g = (
            Image.fromarray((sh * 255).astype(np.uint8))
            .convert("RGB")
            .resize((W * S, H * S), Image.BILINEAR)
        )
        return caption(g, t, a.fonts)

    grid(
        [
            [
                shade_img(shade_nw, "315° NW (Topo50 / LINZ today)"),
                shade_img(shade_nnw, "337.5° NNW (R-03)"),
            ],
            [
                shade_img(shade_multi, "Multidirectional 337.5° + 292.5° + 22.5°"),
                shade_img(
                    hillshade(dem, [135], [1]),
                    "135° SE — control: invites terrain reversal",
                ),
            ],
        ]
    ).save(os.path.join(a.out, "03-relief-lighting.png"))

    box = (60 * S, 90 * S, 470 * S, 215 * S)
    grid(
        [
            [caption(up.crop(box), "LINZ — labels at 2×", a.fonts)],
            [caption(v0.crop(box), "accessible-v0 — labels at 2×", a.fonts)],
        ]
    ).save(os.path.join(a.out, "04-labels-closeup.png"))
    print("wrote", sorted(os.listdir(a.out)))
