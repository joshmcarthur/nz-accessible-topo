#!/usr/bin/env python3
"""Draw symbol test tiles: each legend symbol on each fill and across each conflict.

Run this with the QGIS python. The host Python does not have QGIS.
Each tile is 10 mm at sheet size, 600 dpi. The output directory holds one
folder of tiles and one strip PNG per swatch key, and tiles.json.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.symbol_tiles_main import main

if __name__ == "__main__":
    sys.exit(main())
