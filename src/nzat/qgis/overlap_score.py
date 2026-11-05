import math

import numpy as np

INK_WEIGHT = 10
HALO_WEIGHT = 3
GAP_WEIGHT = 3


def gap_band(near_ink, px_x, px_y):
    """Return near_ink grown px_x pixels left and right and px_y up and down."""
    band = near_ink.copy()
    for step in range(1, px_x + 1):
        band[:, step:] |= near_ink[:, :-step]
        band[:, :-step] |= near_ink[:, step:]
    wide = band.copy()
    for step in range(1, px_y + 1):
        band[step:, :] |= wide[:-step, :]
        band[:-step, :] |= wide[step:, :]
    return band


def overlap_score(
    target_ink, target_halo, near_ink, near_halo, col, row, near_gap=None
):
    """Ink on ink counts INK_WEIGHT times, ink inside a halo or the gap band HALO_WEIGHT or GAP_WEIGHT times, and halo on halo once."""
    height, width = target_ink.shape
    if (
        col < 0
        or row < 0
        or row + height > near_ink.shape[0]
        or col + width > near_ink.shape[1]
    ):
        return math.inf
    ink = near_ink[row : row + height, col : col + width]
    halo = near_halo[row : row + height, col : col + width]
    score = (
        INK_WEIGHT * int(np.count_nonzero(target_ink & ink))
        + HALO_WEIGHT * int(np.count_nonzero(target_halo & ink))
        + HALO_WEIGHT * int(np.count_nonzero(target_ink & halo))
        + int(np.count_nonzero(target_halo & halo))
    )
    if near_gap is not None:
        gap = near_gap[row : row + height, col : col + width]
        score += GAP_WEIGHT * int(np.count_nonzero(target_ink & gap))
    return score
