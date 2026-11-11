#!/usr/bin/env python3
"""Turn sheet GeoTIFFs from render_sheets.py into one PMTiles archive.

Needs gdal (3.x) and the pmtiles CLI on PATH. Run with the host Python,
not the QGIS Python.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.render.make_tiles import main

if __name__ == "__main__":
    sys.exit(main())
