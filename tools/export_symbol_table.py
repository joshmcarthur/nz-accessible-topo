#!/usr/bin/env python3
"""Write site/src/data/symbols.json and the legend crops in site/public/symbols/.

Reads the stock legend TIFF and the accessible legend PNG outside the repo.
CI does not run this. Commit its outputs.
"""

import _bootstrap  # noqa: F401
from nzat.site.export_symbol_table import main

if __name__ == "__main__":
    main()
