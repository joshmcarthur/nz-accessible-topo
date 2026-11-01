# Current state: Topo50 printed series

What the official printed 1:50,000 series does today, from LINZ's own
documentation and from published user critique. Items marked **[verify]** need
checking against a physical sheet legend (BX24 Christchurch is used as the
example sheet in LINZ's guide).

## Series facts

| Property | Value | Source |
|---|---|---|
| Scale | 1:50,000 (some small islands 1:25,000) | S-LINZ-GUIDE, S-LINZ-DD |
| Projection / datum | NZTM2000 / NZGD2000 | S-LINZ-GUIDE |
| Grid | Blue grid lines every 2 cm = 1 km | S-LINZ-GUIDE |
| Contour interval | 20 m; supplementary 10 m in very flat areas; no 0 m contour; coastline = MHWS | S-LINZ-DD-CONTOUR |
| Contour accuracy | ~half interval (≈10 m); less accurate in forest and snow | S-LINZ-GUIDE, S-LINZ-DD-CONTOUR |
| Relief shading | Illuminated from the north-west | S-LINZ-GUIDE |
| Colour convention | Blue = water, black = cultural, green = vegetation | S-LINZ-GUIDE |
| Sheet format | A1 portrait | retail listings (D) |

## Symbology observations

- **Tracks are all black.** Topo50 has three main track groups (vehicle
  tracks, foot tracks, poled routes) plus a closed-route sign, all in black.
  The symbology is essentially that of the NZMS 260 series from 1977, and
  the map does not distinguish public from private access. (S-MCDONALD-2020)
- **Content is largely inherited.** A retired LINZ cartographer is reported
  as saying the 2009 Topo50 launch largely reprojected NZMS 260 content.
  (S-MCDONALD-2020, quoting *Wilderness* 2013) — relevant because the
  *design* has not had a ground-up review since 1977.
- **The digital Topo50 is a basemap for other services** (e.g. the Walking
  Access Commission's Tracks and Trails map overlays coloured lines on the
  black Topo50 tracks). (S-MCDONALD-2020)
- ~~[verify]~~ **Measured in log 0019** — see below.

## Why this matters for us

The print series is a 1977 design language running on modern data. That is
not automatically bad — it is familiar to emergency services and trampers —
so any change must weigh **learnability against familiarity**. See
`open-questions.md` (OQ-01).


## Measured print symbology (log 0019)

Source: LINZ's own legend render, `e2e/assets/topo-legend-1.tif` in
`linz/topographic-system@f253c35` (vendored at `docs/visuals/source/`).
Colours are the modal ink colour inside each swatch.

Topo50 print uses a **small spot-colour palette**:

| Ink | Hex | Used for |
|---|---|---|
| Orange | `#F19100` | road fills **and** index + intermediate contours |
| Red-orange | `#EA6300` | state highways, hot springs, fumaroles, buried gas pipeline, signposts, footnote markers |
| Blue | `#008BCA` | water lines, water names, cold springs, snow/ice contours |
| Black | `#000000` | tracks, buildings, cultural features, most labels |
| Pale green | `#E1EAC3` | native forest |
| Paler green | `#ECF3DA` | scrub |
| Pale blue | `#D1E7F5` | water areas |

### Findings from the measurements

| # | Observation | Evidence |
|---|---|---|
| P1 | Contours and road fills are **the same ink**; roads are separated only by black casing and width | sampled ΔE 0.0 |
| P2 | Foot track: dash 24 / gap 12 px; **closed track: dash 23 / gap 24 px**. Same ink and weight — a closed (impassable) track is signalled only by gap length | dash measurement |
| P3 | Hot vs cold spring: same × glyph; blue vs red-orange. Distinct in colour, **1.13:1 in greyscale** | audit |
| P4 | Hot spring and fumarole share ink; distinguished by glyph (× vs ⊗) — good practice | legend |
| P5 | Native forest vs scrub: tint only, ΔE 4.8 normal / 2.5 tritan, 1.1:1 greyscale | audit |
| P6 | Scattered scrub **is** a pattern in print (the web style replaced it with a flat tint) | legend |
| P7 | Under the red-light model, contours are 1.13:1 and red-orange symbols 1.20:1 against paper | audit |
| P8 | Index contour labels and spot heights are **italic** (e.g. *130m*, *100*) | legend |
| P9 | Water names are blue italic (e.g. *Kawarau River*) | real render |

Full table: [audit-topo50-print.md](audit-topo50-print.md).
