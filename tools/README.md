# Tools

## palette_audit.py

Audits a MapLibre GL style JSON for:

- text contrast (WCAG 2.x ratio) of each label against its halo;
- separability of declared "must-distinguish" colour pairs under normal
  vision, protanopia, deuteranopia, tritanopia (Machado et al. 2009 matrices),
  greyscale, and a crude red-headtorch model.

```
python3 tools/palette_audit.py path/to/style.json \
    --pairs tools/pairs-linz-topographic-v2.json \
    --md docs/current-state/audit-linz-topographic-v2.md
```

The maths is checked against reference values (CIEDE2000 Sharma et al. test
pairs; black/white = 21:1). The *perceptual thresholds* used to flag results
are working assumptions — treat output as evidence grade D.

Known limitations:
- Data-driven (`["match", ...]`, `stops`) colours are skipped; only literal
  colours are audited.
- Labels drawn on an icon (e.g. highway shields) are reported against the
  map background and show as false failures.
- Simulation is for *dichromacy* (severity 1.0). Anomalous trichromats see
  more than this; it is a worst case.
