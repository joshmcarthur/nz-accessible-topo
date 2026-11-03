#!/usr/bin/env python3
"""
check_site.py — the site must meet the standards the project argues for.

Serves site/dist, then on every page:
  S1  axe-core: no WCAG 2.0/2.1/2.2 A/AA or best-practice violations
  S2  no rendered italic text (R-05 applies to the site too)
  S3  every internal link resolves, including #anchors on the target page

Needs: playwright (Python) with Chromium; site/node_modules/axe-core.
Usage: python3 tools/check_site.py
"""

import _bootstrap  # noqa: F401
from nzat.site.check_site import main

if __name__ == "__main__":
    main()
