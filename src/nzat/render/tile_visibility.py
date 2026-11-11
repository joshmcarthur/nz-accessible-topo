"""Score how much of a symbol stays visible in a test tile.

The paper tile holds the symbol alone, so its ink pixels are the symbol mask.
A mask pixel in a scene tile is visible when it still differs from the ground
around the symbol by the floor for that vision condition. In a conflict tile
the pixel must also keep its paper-tile colour: ink from the other class is
not the symbol. Symbol ink beside visible ink counts with it.
"""

import math

import numpy as np
from PIL import Image, ImageFilter

from nzat.colour.apply_matrix import GREYSCALE, RED_HEADTORCH, apply_matrix
from nzat.colour.ciede2000 import ciede2000
from nzat.colour.rgb_to_lab import rgb_to_lab
from nzat.colour.simulate import MACHADO
from nzat.colour.srgb import linear_to_srgb, srgb_to_linear

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
# Reduced acuity (F-32): typical colour vision, then a blur. Scored last.
ACUITY = "acuity"
ACUITY_SNELLEN = 18  # 6/18, the WHO limit of mild vision impairment
READING_MM = 400
TILE_DPI = 600
CONTRAST_FLOOR = 3.0  # R-01, grey and red light
DELTA_E_FLOOR = 10.0  # R-04, colour conditions

INK_DIFF = 48  # A paper-tile pixel this far from white is symbol ink.
INTACT_DIFF = 32  # A conflict-tile pixel this close to the paper tile is intact.
RING_INNER_PX = 2  # Skip the anti-aliased edge.
RING_OUTER_PX = 12  # 0.5 mm of ground around the symbol.
# Ink within 0.35 mm of visible ink is found with it: a casing carries its
# road, an outline carries its area. 0.35 mm is the F-31 and F-32 figure.
LOCATE_PX = 8
# A name owns the ground under its letters and halo, plus a 0.2 mm margin.
NAME_FOOTPRINT_PX = 14
_QUANT = 8


def acuity_sigma_px(snellen=ACUITY_SNELLEN, reading_mm=READING_MM, dpi=TILE_DPI):
    """Return the blur for an eye that resolves snellen/6 arc minutes.

    The Gaussian is as wide (full width at half maximum) as the smallest
    detail that eye resolves at the reading distance.
    """
    detail_mm = reading_mm * math.tan(math.radians(snellen / 6 / 60))
    return detail_mm * dpi / 25.4 / (2 * math.sqrt(2 * math.log(2)))


def blur(rgb, sigma):
    """Blur an sRGB array in linear light, as defocus does. Return sRGB ints."""
    radius = int(math.ceil(3 * sigma))
    x = np.arange(-radius, radius + 1)
    kernel = np.exp(-(x**2) / (2 * sigma**2))
    kernel /= kernel.sum()
    lin = np.pad(
        srgb_to_linear(rgb), ((radius, radius), (radius, radius), (0, 0)), "edge"
    )
    for axis in (0, 1):
        lin = np.apply_along_axis(np.convolve, axis, lin, kernel, "valid")
    return np.rint(linear_to_srgb(lin)).astype(int)


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


def _located_share(visible, mask):
    """Return the share of the symbol that is visible ink or beside it."""
    return round(float((_grow(visible, LOCATE_PX) & mask).sum()) / float(mask.sum()), 3)


def name_footprint(alone):
    """Return the pixels a name owns: its ink, its halo and a small margin."""
    return _grow(symbol_mask(alone), NAME_FOOTPRINT_PX)


def covered_share(paper, alone):
    """Return the share of the symbol that lies under the name's footprint."""
    mask = symbol_mask(paper)
    if not mask.any():
        return 0.0
    return float((mask & name_footprint(alone)).sum()) / float(mask.sum())


def visible_fractions(paper, tile, conflict, alone=None, yields=False):
    """Return {condition: share of the symbol that stays visible}.

    `alone` is the conflict tile with no symbol. Where the other class inks a
    pixel, that pixel is not the symbol, even when the two inks match.
    With `yields`, the symbol gives way under a name: only the part outside
    the name's footprint is measured.
    Return None when the symbol has no ink or no ground around it.
    """
    mask = symbol_mask(paper)
    ring = ground_ring(mask)
    if not mask.any() or not ring.any():
        return None
    if yields and alone is not None:
        outside = mask & ~name_footprint(alone)
        if outside.any():
            mask = outside
    keep = mask
    if conflict:
        keep = mask & (np.abs(_rgb(tile) - _rgb(paper)).max(axis=2) <= INTACT_DIFF)
        if alone is not None:
            keep &= ~symbol_mask(alone)
    views = {
        name: (_rgb(apply_matrix(tile.convert("RGB"), matrix)), name in LIGHTNESS_ONLY)
        for name, matrix in CONDITIONS.items()
    }
    views[ACUITY] = (blur(_rgb(tile), acuity_sigma_px()), False)
    out = {}
    for name, (seen, lightness_only) in views.items():
        visible = np.zeros(mask.shape, dtype=bool)
        visible[keep] = _differs(
            seen[keep], np.median(seen[ring], axis=0), lightness_only
        )
        out[name] = _located_share(visible, mask)
    return out
