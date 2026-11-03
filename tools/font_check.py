#!/usr/bin/env python3
"""
font_check.py — check candidate typefaces for NZ topographic labelling.

Reports, per font file:
  - te reo Māori macron vowel coverage (precomposed Āā Ēē Īī Ōō Ūū) and the
    combining macron U+0304 (fallback for decomposed input)
  - x-height / em and x-height / cap-height (larger x-height reads bigger at
    the same point size — matters at 6–8 pt map label sizes)
  - whether an italic companion exists is noted by the caller

Usage: python3 tools/font_check.py FONT.ttf [FONT.ttf ...]
Requires fontTools.
"""

import _bootstrap  # noqa: F401
from nzat.fonts.check import main

if __name__ == "__main__":
    main()
