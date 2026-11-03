import math

import numpy as np

INK_WEIGHT = 10
HALO_WEIGHT = 3


def overlap_score(target_ink, target_halo, near_ink, near_halo, col, row):
    """Ink on ink counts INK_WEIGHT times, ink inside a halo HALO_WEIGHT times, and halo on halo once."""
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
    return (
        INK_WEIGHT * int(np.count_nonzero(target_ink & ink))
        + HALO_WEIGHT * int(np.count_nonzero(target_halo & ink))
        + HALO_WEIGHT * int(np.count_nonzero(target_ink & halo))
        + int(np.count_nonzero(target_halo & halo))
    )
