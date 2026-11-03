"""Put src/ on sys.path so python3 tools/*.py and QGIS can import nzat."""

import sys
from pathlib import Path

_SRC = str(Path(__file__).resolve().parent.parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
