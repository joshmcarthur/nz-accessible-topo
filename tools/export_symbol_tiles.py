#!/usr/bin/env python3
"""Write site/src/data/symbol-tiles.json from the symbol test tiles.

Run tools/render_symbol_tiles.py first. The tiles are in render/symbol-tiles.
"""

import _bootstrap  # noqa: F401
from nzat.site.export_symbol_tiles import main

if __name__ == "__main__":
    main()
