#!/usr/bin/env python3
"""Sanity tests for the measurement and rendering tools. Run: python3 tools/test_tools.py"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import palette_audit as pa  # noqa: E402
import render_comparison as rc  # noqa: E402


def test_ciede2000_reference():
    # Sharma, Wu & Dalal (2005) test pairs 1 and 3
    assert round(pa.ciede2000((50, 2.6772, -79.7751), (50, 0, -82.7485)), 4) == 2.0425
    assert round(pa.ciede2000((50, -1.1848, -84.8006), (50, 0, -82.7485)), 4) == 1.0


def test_contrast_black_white():
    assert round(pa.contrast_ratio(pa.rel_luminance((0, 0, 0)), pa.rel_luminance((255, 255, 255))), 2) == 21.0


def test_hillshade_direction():
    # Log 0017: the first renderer lit slopes from the opposite side. Never again.
    y, x = np.mgrid[0:rc.H, 0:rc.W].astype(float)
    z = 1000 * np.exp(-((x - 310) ** 2 + (y - 230) ** 2) / (2 * 60 ** 2))
    for az, lit, dark in [(315, (180, 260), (280, 360)), (0, (170, 310), (290, 310)), (90, (230, 370), (230, 250))]:
        sh = rc.hillshade(z, [az], [1])
        assert sh[lit] > 0.9 and sh[dark] < 0.1, az


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
