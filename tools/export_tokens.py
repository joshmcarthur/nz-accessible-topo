#!/usr/bin/env python3
"""
export_tokens.py — the site shares the map's theme: derive CSS tokens from the
same parameters build_style.py uses, and refuse to write tokens that would
break the project's own rules (R-07 text ≥4.5:1; graphical objects ≥3:1).

Writes site/src/styles/tokens.css and site/src/data/tokens.json.
"""

import _bootstrap  # noqa: F401
from nzat.site.export_tokens import main

if __name__ == "__main__":
    main()
