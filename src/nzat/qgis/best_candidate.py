from nzat.qgis.overlap_score import gap_band, overlap_score

MOVE_COST_PER_MM = 40
# At 2 m/px on a 1:50,000 sheet: 0.72 mm beside a name, 0.6 mm above or below it.
GAP_X_PX = 18
GAP_Y_PX = 15


def best_candidate(candidates, near_ink, near_halo):
    """Return the candidate with the lowest overlap, gap and move cost.

    Each candidate is (key, ink, halo, col, row, move_mm). Ink within GAP_X_PX beside or
    GAP_Y_PX above or below neighbour ink costs extra, so names keep apart.
    """
    near_gap = gap_band(near_ink, GAP_X_PX, GAP_Y_PX)
    return min(
        candidates,
        key=lambda c: (
            overlap_score(c[1], c[2], near_ink, near_halo, c[3], c[4], near_gap)
            + MOVE_COST_PER_MM * c[5]
        ),
    )
