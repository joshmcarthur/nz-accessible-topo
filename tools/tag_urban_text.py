#!/usr/bin/env python3
"""Tag carto_text names inside the urban fill, and write urban_text.json beside the project.

The apply step gives a black name in that list an urban-fill halo, so its halo does not cut a
white hole in the street grid (G4). A layer lookup in a label expression hangs the render
(log 0090), so this runs once before the apply step, not at render time.

Run it with the QGIS Python on the stock or accessible project, then run the apply step again:

    python tag_urban_text.py --project accessible/nztopo50.qgs [--extent XMIN,YMIN,XMAX,YMAX]
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.tag_urban_text_main import main

if __name__ == "__main__":
    sys.exit(main())
