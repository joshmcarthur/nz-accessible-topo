#!/usr/bin/env python3
"""Draw 1 km map squares at 600 dpi, or one rectangle with --extent.

Run this inside the map container. The host Python does not have QGIS.
1000 m on the ground is 20 mm on the 1:50,000 sheet. 20 mm at 600 dpi is 472 px.
The script draws the map face only. It draws the Map5View layers. It does not export the sheet page.

Load every .ttf with QFontDatabase. The stock exporter loads only .otf files.
Set HOME=/tmp before QGIS starts so fontconfig can write a cache.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.font_files import font_files
from nzat.qgis.map_layers import SHEET_PRESET, map_layers
from nzat.qgis.qgis_prefix import CONTAINER_PREFIX, qgis_prefix
from nzat.qgis.render_jobs import DPI, PX
from nzat.qgis.render_square_main import main
from nzat.qgis.sheet_layer_ids import sheet_layer_ids
from nzat.qgis.square_extent import METRES, square_extent
from nzat.qgis.with_dem_layer import with_dem_layer

__all__ = [
    "CONTAINER_PREFIX",
    "DPI",
    "METRES",
    "PX",
    "SHEET_PRESET",
    "font_files",
    "main",
    "map_layers",
    "qgis_prefix",
    "sheet_layer_ids",
    "square_extent",
    "with_dem_layer",
]


if __name__ == "__main__":
    sys.exit(main())
