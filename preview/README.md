# Preview

Side-by-side, synced view of LINZ `topographic-v2` and our build, with
in-browser simulation of protanopia, deuteranopia, tritanopia, greyscale and
red-headtorch light (same Machado matrices as `tools/palette_audit.py`, applied
in linearRGB via SVG filters).

```sh
python3 -m http.server 8000      # from the repo root
open http://localhost:8000/preview/
```

Paste a LINZ Basemaps API key (free from basemaps.linz.govt.nz). It's kept in
your browser's localStorage only. Starts at Arthur's Pass, z13; the left
map's position is kept in the URL hash so views can be shared.

Caveat: written and validated as code, but **not yet run against live LINZ
tiles** (our build sandbox can't reach basemaps.linz.govt.nz). First run may
need fixes to URL rewriting.
