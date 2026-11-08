# 0108 — Legend review set from national parquet

**Date:** 2026-11-07

## Question

Which 4 km squares, besides BX24, hold every stock-legend class that exists in
the national Topo50 GeoParquet?

## What we did

N-8 vector parity is deferred. Josh asked for a sample of sheets or squares
that cover the legend, so later work can test every representation.

`tools/find_symbol_sheets.py` (QGIS Python, DuckDB) reads
`accessible-sheets/*.parquet`. One predicate per `/symbols/` key. A hit
prefers the BX24 bbox. Remaining hits snap to the same 4 km origin as the
BX24 grid (`CELL_M` 4000, origin 1564000 E, 5154000 N). Greedy cover then
picks extra squares. Feature `bbox` is lon/lat on most layers and NZTM on
the sheet index and `nztopo50_carto_symbol`; the tool transforms lon/lat
to EPSG:2193.

## What we found

126 legend rows: 75 have a feature inside BX24, 39 need an extra 4 km
square, 11 have no class in the national files. No query returned zero rows
when a class exists.

**No national type (stay blocked):** cattlestop, plaque or signpost,
pipeline above, pipeline underground, power pylons, power poles, telephone,
buried gas pipeline, terrace, seawall, geothermal bore.

Some BX24 hits are still undrawn on Map5View (ford on `transport_point`,
orchard on `landuse`). The class is on the sheet. A theme or rule change
can show it. Do not treat those as missing data.

Fumarole has a square on BH35 Turangi. Do not apply the log 0096 shape
until Josh reviews it.

## Extra 4 km squares

Extent is `east,north,east+4000,north+4000`. Render with
`tools/render_square.py` at 945×945 px, 300 dpi.

| Square | Sheet | Name | Keys |
|---|---|---|---|
| `1956000-5786000` | BE40 | Whakatāne | cutting, embankment |
| `1856000-5814000` | BD36 | Lower Kaimai | poled_route |
| `1736000-6042000` | AX31 | Bream Head | track_connector |
| `1452000-5262000` | BU19 | Kumara | walkwire |
| `1852000-5858000` | BC36 | Katikati | tramway |
| `1704000-6010000` | AY29 | Ruawai | stockyard |
| `1812000-5998000` | AY34 | Claris | grave |
| `1596000-5242000` | BV25 | Motunau Beach | helipad |
| `1716000-5994000` | AY30 | Maungaturoto | historic_pa |
| `1908000-5810000` | BD38 | Maketu | redoubt |
| `1916000-5630000` | BJ38 | Te Pohue | reservoir_uncovered |
| `1824000-5978000` | AZ34 | Moehau | tower |
| `1564000-6182000` | AT24 | Cape Reinga | lighthouse |
| `1388000-5002000` | CC16 | Kyeburn | water_race_disused |
| `1452000-5306000` | BT19 | Runanga | industrial_cableway |
| `1468000-5358000` | BS20 | Charleston | mine_underground |
| `1512000-5186000` | BX21 | Windwhistle | mine_opencast |
| `1148000-4978000` | CC06 | Taitetimu/Caswell Sound | ice_contours |
| `1572000-6182000` | AT24 | Cape Reinga | depression_contours |
| `1812000-5666000` | BH34 | Raurimu | shallow_depression |
| `1604000-6106000` | AV25ptAV26 | Tauroa Peninsula | small_depression_shaft |
| `1984000-5758000` | BF41 | Oponae | slip |
| `1724000-6090000` | AV30 | Cape Brett | cave |
| `1400000-5166000` | BX17 | Mount Sibbald | moraine |
| `1384000-5154000` | BX16 | Mount Elie De Beaumont | moraine_wall |
| `1444000-5158000` | BX19 | Hakatere | scree |
| `1432000-4970000` | CD18 | Palmerston | shoal_reef |
| `1436000-5158000` | BX18 | Lake Clearwater | shingle |
| `1360000-5094000` | BZ15 | Twizel | marine_farm |
| `1468000-5290000` | BU20 | Moana | dam |
| `1760000-5870000` | BC32 | Pukekawa | floodgate |
| `1456000-5258000` | BV19 | Lake Kaniere | weir |
| `2008000-5770000` | BE42 | Houpoto | rapids |
| `2064000-5774000` | BE44 | Te Puia Springs | hot_spring |
| `1836000-5682000` | BH35 | Turangi | fumarole |
| `1904000-5810000` | BD38 | Maketu | canal_small |
| `1572000-5150000` | BY24 | Birdlings Flat | scattered_scrub |
| `1756000-5974000` | AZ32 | Kawau Island | mangroves |
| `1820000-5506000` | BN34 | Shannon | bivouac |

## What changed

- `src/nzat/qgis/symbol_queries.py`, `cover_set.py`, `find_symbol_sheets_main.py`
- `tools/find_symbol_sheets.py`
- `tests/qgis/test_cover_set.py`
- This log. BACKLOG next work points here. N-8 stays deferred.

## Confidence & gaps

The set is data presence, not a drawn Map5View proof. Closest-class
substitutes: soakhole for stream disappearing, sinkhole for shallow
depression, railway siding for station/yard, landuse mine for underground
mine, structure reservoir for covered reservoir. Compositional rows
(level crossing, road over railway) reuse a component layer.
