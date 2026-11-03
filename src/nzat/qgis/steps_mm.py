import numpy as np

STEP_MM = 0.25


def steps_mm(low, high):
    """Steps of STEP_MM from low to high that include 0, so a name with no overlap stays put."""
    return np.concatenate(
        (
            -np.arange(0, -low + STEP_MM / 2, STEP_MM)[::-1],
            np.arange(STEP_MM, high + STEP_MM / 2, STEP_MM),
        )
    )
