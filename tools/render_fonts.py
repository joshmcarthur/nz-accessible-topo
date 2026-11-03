#!/usr/bin/env python3
"""render_fonts.py — macron and confusable-character specimen for candidate fonts.

Usage: python3 tools/render_fonts.py OUT.png "Label=path.ttf[@weight]" ...
"""

import sys

import _bootstrap  # noqa: F401
from nzat.fonts.render_specimen import main

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
