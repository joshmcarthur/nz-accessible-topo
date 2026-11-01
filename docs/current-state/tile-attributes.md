# Tile attributes available to styles (OQ-12)

Inferred from every `filter` expression in `topographic-v2.json`
(`linz/basemaps-config@581b44a`). This shows attributes the style **uses**; the
tiles may carry more. Direct tile inspection is still to do — our sandbox
can't reach `basemaps.linz.govt.nz` (the MBTiles export at
`/v1/export/topographic-v2/2193.mbtiles` is the easy route).

## Attributes that matter for our recommendations

| Need | Source-layer | Attribute / values | Status |
|---|---|---|---|
| R-04 index vs intermediate contours | `contours` | `type = index` | ✅ available |
| R-04 supplementary / depression contours | `contours` | `designated`, `nat_form` | ✅ available |
| R-04 dashed *indefinite* contours | `contours` | `definition` (in Topo50 data dictionary) | ❓ not used by style — check tiles |
| R-10 scrub vs scattered scrub | `land` | `kind = scrub`, `distribution = scattered` | ✅ |
| Native vs exotic forest | `land` | `tree = native / exotic`, `landuse = wood` | ✅ |
| R-11 closed tracks | `streets` | `subclass = foot_closed / foot_route_closed` | ✅ |
| Track type | `streets` | `track_use = foot / vehicle / cycle only` | ✅ |
| Historic sites, huts, bivvies | `pois` | `historic`, `building = hut`, `amenity = bivouac` | ✅ |
| R-12 public access status | — | — | ❌ not in data (as expected, F-25) |

## Hillshade

Not a tile layer: the style computes shading client-side from a
`raster-dem` source (`LINZ-Elevation-Hillshade`) with:

```json
"hillshade-illumination-direction": 315,
"hillshade-illumination-anchor": "map",
"hillshade-exaggeration": 0.4
```

MapLibre's own default direction is **335°** (≈NNW, S-MAPLIBRE-SPEC); LINZ
explicitly overrides it to 315° (NW), matching the Topo50 print convention.
MapLibre style spec v23.2.0 added `hillshade-method` including
`multidirectional`, which accepts arrays of directions and colours
(S-MAPLIBRE-2320).

**Implication:** R-03 on the web is a one-property change, and the
multidirectional part of R-03 is natively supported in current MapLibre.

## Index contours were missed by the first audit

Index contours use zoom-interpolated (data-driven) colours, which
`palette_audit.py` skips. Measured by hand:

| Zoom | Colour | vs white | Red-light model |
|---|---|---:|---:|
| 10 | `rgba(205,128,31,0.5)` | 1.71:1 | 1.25:1 |
| 15 | `rgba(207,129,43,0.75)` | 2.27:1 | 1.38:1 |
| (intermediate, for comparison) | `rgba(206,103,6,0.75)` | 2.66:1 | 1.39:1 |

Index contours are **paler** than intermediate ones and rely on width (and a
10%-opacity black offset line) for emphasis. This strengthens W3.
