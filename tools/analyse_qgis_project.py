#!/usr/bin/env python3
"""
analyse_qgis_project.py — summarise LINZ's Topo50 QGIS cartography.

Usage: python3 tools/analyse_qgis_project.py /path/to/topographic-qgis [carto_text.parquet]
"""

import sys

import _bootstrap  # noqa: F401
from nzat.render.analyse_qgis_project import main

if __name__ == "__main__":
    main(*sys.argv[1:3])
