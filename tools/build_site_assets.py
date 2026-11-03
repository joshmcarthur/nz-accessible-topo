#!/usr/bin/env python3
"""
build_site_assets.py — pre-render every comparison variant under every condition.

Reads site/src/data/comparisons.json and conditions.json; writes
site/public/compare/<comparison>/<variant-index>-<condition>.webp plus
site/src/data/compare-assets.json (sizes, for layout without shift).

Same models as tools/palette_audit.py, so the site shows exactly what the
audits measure.
"""

import _bootstrap  # noqa: F401
from nzat.site.build_assets import main

if __name__ == "__main__":
    main()
