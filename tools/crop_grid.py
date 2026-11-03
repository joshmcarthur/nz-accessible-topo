#!/usr/bin/env python3
"""Crop a 4 km chequerboard from stock and accessible BX24 faces.

Host Python is enough. The faces come from tools/render_square.py --extent.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.crop_grid_main import main
from nzat.qgis.sample_grid import BX24_EXTENT, CELL_M, CELL_PX, PHASE

__all__ = [
    "BX24_EXTENT",
    "CELL_M",
    "CELL_PX",
    "PHASE",
    "main",
]


if __name__ == "__main__":
    sys.exit(main())
