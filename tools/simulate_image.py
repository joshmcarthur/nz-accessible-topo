#!/usr/bin/env python3
"""simulate_image.py — apply the audit's vision/lighting simulations to a real map image.

Uses the same models as palette_audit.py: Machado et al. (2009) dichromacy in
linear RGB, greyscale (relative luminance), and a red-headtorch model
(reflectance in the red channel only).

Usage: python3 tools/simulate_image.py IN_IMAGE OUT.png [--crop x0,y0,x1,y1]
"""

import _bootstrap  # noqa: F401
from nzat.render.simulate_image import main

if __name__ == "__main__":
    main()
