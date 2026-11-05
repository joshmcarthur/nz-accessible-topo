import numpy as np

from nzat.qgis.best_candidate import best_candidate
from nzat.qgis.steps_mm import steps_mm


def test_carto_fit_prefers_less_ink_overlap():
    # Catches a grid that cannot keep a name in place, or a score that ignores ink overlap or move cost.
    assert 0 in steps_mm(-1.6, 0.5)
    near_ink = np.zeros((20, 40), bool)
    near_ink[5:10, 0:20] = True
    near_halo = near_ink.copy()
    ink = np.ones((5, 10), bool)
    on_top = ("on top", ink, ink, 5, 5, 0)
    clear = ("clear", ink, ink, 25, 5, 0.5)
    far = ("far", ink, ink, 25, 12, 1.0)
    outside = ("outside", ink, ink, 35, 5, 0)
    assert (
        best_candidate([on_top, clear, far, outside], near_ink, near_halo)[0] == "clear"
    )


def test_carto_fit_keeps_a_gap_beside_a_neighbour():
    # Catches a score that lets a name abut its neighbour so the two read as one phrase.
    near_ink = np.zeros((20, 60), bool)
    near_ink[5:10, 0:20] = True
    ink = np.ones((5, 10), bool)
    abut = ("abut", ink, ink, 20, 5, 0.4)
    spaced = ("spaced", ink, ink, 40, 5, 0.5)
    assert best_candidate([abut, spaced], near_ink, near_ink.copy())[0] == "spaced"
