#!/usr/bin/env python3
"""make_sprites.py — generate the `nzat` sprite sheet (1x and 2x) used by R-10/R-11.

Images are drawn procedurally so they are reviewable as code:
  scattered_stipple  16×16 fill pattern: sparse dark-green dots (R-10)
  closed_crossbar    12×8 line pattern: a dark bar across the track every 12 px (R-11)
"""

import _bootstrap  # noqa: F401
from nzat.sprites.build import main

if __name__ == "__main__":
    main()
