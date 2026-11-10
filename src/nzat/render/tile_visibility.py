"""Score how much of a symbol stays visible in a test tile.

The paper tile holds the symbol alone, so its ink pixels are the symbol mask.
A mask pixel in a scene tile is visible when it still differs from the ground
around the symbol by the floor for that vision condition. In a conflict tile
the pixel must also keep its paper-tile colour: ink from the other class is
not the symbol.
"""

import numpy as np
from PIL import Image, ImageFilter

from nzat.colour.apply_matrix import GREYSCALE, RED_HEADTORCH, apply_matrix
from nzat.colour.ciede2000 import ciede2000
from nzat.colour.rgb_to_lab import rgb_to_lab
from nzat.colour.simulate import MACHADO
from nzat.colour.srgb import srgb_to_linear

# Condition id (site/src/data/conditions.json) to linear-RGB matrix.
CONDITIONS = {
    "normal": None,
    "deutan": MACHADO["deuteranopia"],
    "protan": MACHADO["protanopia"],
    "tritan": MACHADO["tritanopia"],
    "grey": GREYSCALE,
    "red": RED_HEADTORCH,
}
LIGHTNESS_ONLY = ("grey", "red")
CONTRAST_FLOOR = 3.0  # R-01, grey and red light
DELTA_E_FLOOR = 10.0  # R-04, colour conditions

INK_DIFF = 48  # A paper-tile pixel this far from white is symbol ink.
INTACT_DIFF = 32  # A conflict-tile pixel this close to the paper tile is intact.
RING_INNER_PX = 2  # Skip the anti-aliased edge.
RING_OUTER_PX = 12  # 0.5 mm of ground around the symbol.
_QUANT = 8


def _rgb(image):
    return np.asarray(image.convert("RGB")).astype(int)


def symbol_mask(paper):
    """Return the ink pixels of the paper tile as a boolean array."""
    return (255 - _rgb(paper)).max(axis=2) >= INK_DIFF


def _grow(mask, radius):
    image = Image.fromarray(mask.astype(np.uint8) * 255)
    return np.asarray(image.filter(ImageFilter.MaxFilter(2 * radius + 1))) > 0


def ground_ring(mask):
    """Return the pixels just outside the symbol."""
    return _grow(mask, RING_OUTER_PX) & ~_grow(mask, RING_INNER_PX)


def _luminance(rgb):
    lin = srgb_to_linear(rgb)
    return lin @ np.array([0.2126, 0.7152, 0.0722])


def _differs(pixels, ground, lightness_only):
    """Return a boolean per pixel: it meets the floor against the ground."""
    if lightness_only:
        a, b = _luminance(pixels), _luminance(ground)
        ratio = (np.maximum(a, b) + 0.05) / (np.minimum(a, b) + 0.05)
        return ratio >= CONTRAST_FLOOR
    # CIEDE2000 is scalar here, so measure each quantised colour once.
    quantised = pixels // _QUANT * _QUANT + _QUANT // 2
    colours, inverse = np.unique(quantised, axis=0, return_inverse=True)
    ground_lab = rgb_to_lab(tuple(ground))
    passes = np.array(
        [ciede2000(rgb_to_lab(tuple(c)), ground_lab) >= DELTA_E_FLOOR for c in colours]
    )
    return passes[inverse.reshape(-1)]


def visible_fractions(paper, tile, conflict):
    """Return {condition: share of the symbol's ink that stays visible}.

    Return None when the symbol has no ink or no ground around it.
    """
    mask = symbol_mask(paper)
    ring = ground_ring(mask)
    if not mask.any() or not ring.any():
        return None
    keep = mask
    if conflict:
        keep = mask & (np.abs(_rgb(tile) - _rgb(paper)).max(axis=2) <= INTACT_DIFF)
    out = {}
    for name, matrix in CONDITIONS.items():
        seen = _rgb(apply_matrix(tile.convert("RGB"), matrix))
        ground = np.median(seen[ring], axis=0)
        differs = _differs(seen[keep], ground, name in LIGHTNESS_ONLY)
        out[name] = round(float(differs.sum()) / float(mask.sum()), 3)
    return out
