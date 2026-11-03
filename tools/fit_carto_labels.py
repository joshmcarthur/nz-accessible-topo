#!/usr/bin/env python3
"""Fit flat carto_text names where their labels collide, and write carto_fit.json.

QGIS tests label boxes as yes or no, so it cannot choose the position with the least ink overlap.
This tool renders the map face, finds flat names whose boxes collide, and tries each one on one
line or in its default form, moved in small steps. It scores glyph ink and halo, not boxes.
Flat names are drawn as glyphs. Every other label is its QGIS box. Point symbols are not counted.

Run it with the QGIS Python on the accessible project, then run the apply step again:

    python fit_carto_labels.py --project accessible/nztopo50.qgs --font fonts \
        --extent 1564000,5154000,1588000,5190000
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.best_candidate import best_candidate
from nzat.qgis.fit_carto_labels_main import main
from nzat.qgis.overlap_score import overlap_score
from nzat.qgis.steps_mm import steps_mm

__all__ = [
    "best_candidate",
    "main",
    "overlap_score",
    "steps_mm",
]


if __name__ == "__main__":
    sys.exit(main())
