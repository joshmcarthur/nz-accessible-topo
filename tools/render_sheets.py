#!/usr/bin/env python3
"""Draw every Topo50 sheet face to a georeferenced GeoTIFF (EPSG:2193).

Run this with the QGIS python. The host Python does not have QGIS.
One QGIS process loads the project once and loops over the sheets.
The size of each image comes from its sheet bbox at 1:50,000 and --dpi.
A sheet whose .tif exists is skipped, so a run can resume.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.render_sheets_main import main

if __name__ == "__main__":
    sys.exit(main())
