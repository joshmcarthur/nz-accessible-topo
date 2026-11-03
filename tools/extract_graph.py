#!/usr/bin/env python3
"""
extract_graph.py — build the source → finding → recommendation → change graph
from the markdown docs, for the site's Sankey and trace pages.

Writes site/src/data/graph.json. Exits 1 (lint) if any finding has no source
or any recommendation rests on nothing — the evidence chain must be complete.

Usage: python3 tools/extract_graph.py
"""

import _bootstrap  # noqa: F401
from nzat.site.extract_graph import main

if __name__ == "__main__":
    main()
