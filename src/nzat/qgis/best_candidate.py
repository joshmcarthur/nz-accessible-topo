from nzat.qgis.overlap_score import overlap_score

MOVE_COST_PER_MM = 40


def best_candidate(candidates, near_ink, near_halo):
    """Return the candidate with the lowest overlap plus move cost.

    Each candidate is (key, ink, halo, col, row, move_mm).
    """
    return min(
        candidates,
        key=lambda c: (
            overlap_score(c[1], c[2], near_ink, near_halo, c[3], c[4])
            + MOVE_COST_PER_MM * c[5]
        ),
    )
