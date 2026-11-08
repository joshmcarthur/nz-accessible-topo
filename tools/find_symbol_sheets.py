#!/usr/bin/env python3
"""Find 4 km squares that hold legend classes BX24 does not draw.

Run this with the QGIS python (DuckDB ships in that interpreter).
Host Python does not have DuckDB.
"""

import sys

import _bootstrap  # noqa: F401
from nzat.qgis.find_symbol_sheets_main import main

if __name__ == "__main__":
    sys.exit(main())
