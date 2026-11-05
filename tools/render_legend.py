#!/usr/bin/env python3
"""Draw the accessible Topo50 legend: stock legend labels, applied map swatches.

Run this with the QGIS python after the apply step. The host Python does not have QGIS.
The stock legend is topo-legend-1.tif from linz/topographic-system (e2e/assets).
The output is topo-legend-accessible.png beside the project. The applied
project's legend picture points at that file.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.render_legend_main import main

if __name__ == "__main__":
    sys.exit(main())
