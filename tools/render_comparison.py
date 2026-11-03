#!/usr/bin/env python3
"""
render_comparison.py — draw one synthetic terrain scene with two styles.

Usage:
    python3 tools/render_comparison.py --fonts /path/to/google-fonts/ofl --out docs/visuals
"""

import sys

import _bootstrap  # noqa: F401
from nzat.render.comparison_main import main
from nzat.render.hillshade import H, W, hillshade

__all__ = ["H", "W", "hillshade", "main"]

if __name__ == "__main__":
    sys.exit(main())
