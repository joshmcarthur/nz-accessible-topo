#!/usr/bin/env python3
"""
patch_atkinson_omacron.py — PROOF OF CONCEPT: add Ō/ō to Atkinson Hyperlegible Next.

Usage: python3 tools/patch_atkinson_omacron.py IN.ttf OUT.ttf
"""

import sys

import _bootstrap  # noqa: F401
from nzat.fonts.patch_omacron import main

if __name__ == "__main__":
    main(*sys.argv[1:3])
