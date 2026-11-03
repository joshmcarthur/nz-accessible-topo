#!/usr/bin/env python3
"""CLI wrapper. Implementation lives in src/nzat/check/."""

import _bootstrap  # noqa: F401
from nzat.check.run import main

if __name__ == "__main__":
    raise SystemExit(main())
