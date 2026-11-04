#!/usr/bin/env python3
"""Count label pairs that overlap on a map face, and the ones stock does not have.

The grid review (G2) needs a number. Run it with the QGIS Python, first on the
stock project, then on the accessible project with --compare:

    count_label_collisions.py --project stock/nztopo50.qgs --font fonts-stock \
        --extent 1564000,5154000,1588000,5190000 --output stock.json
    count_label_collisions.py --project accessible/nztopo50.qgs --font NZAT.ttf \
        --extent 1564000,5154000,1588000,5190000 --output acc.json --compare stock.json

Overlap is the area of the two QGIS label shapes on the ground. 2000 m2 is
0.8 mm2 on the sheet.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.count_collisions_main import main

if __name__ == "__main__":
    sys.exit(main())
