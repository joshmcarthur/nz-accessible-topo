# Backlog

Status as of 2026-11-05, after log 0094.
Label placement (G2, B-31) is parked. The order now is: style and symbology, full LINZ sheets, a legend of our styles, then vector parity. Log 0090 lists the remaining raster style items.
`tools/render_sheets.py` draws all 445 sheet faces as 150 dpi GeoTIFFs, outside the repo. Flat names are not pinned off BX24. The sheets are a source for B-27 (log 0091). Those rasters predate the open foot-track fix, so open foot tracks show the closed cross (log 0092).
`tools/render_legend.py` draws the accessible swatches into the sheet legend (B-46, log 0092).
Black names on the urban fill take an urban-fill halo from a precomputed `urban_text.json` (B-45, log 0093). The sheet project has no `urban_text.json` yet, so sheet halos stay paper.
Josh accepts the 17% spot-height rank step as an R-09 exception, and counts the stream vs index width step as the R-01 shape cue (log 0093).
Stream is `#004C99` (log 0083). Rivers and canals are 0.25 mm. Drains are 0.15 mm (log 0071). Scrub is alpha 26 plus `#6A9A50` `third_arc` plant marks at 0.18 mm (logs 0068, 0071). A greener scrub fill waits for vector alpha (log 0076). Shelterbelt is `#1D9D00`. Grid is `#269FD2`.
Natural names are Regular in index brown `#7A5542` (logs 0072, 0080). Stock Bold town names draw in patched Atkinson Bold (log 0080). Spot heights are black, 6 pt, and pinned (logs 0077, 0081, 0084). Contour-number FontMarkers are Regular with a 0.3 mm white halo (log 0082). State highway numbers draw in a white shield above the road (log 0090).
Closed tracks use `cross2` 0.7 mm every 3 mm. Foot tracks are 0.2 mm. Poled routes and connectors draw as dots (log 0094). G1 passed. R-11 is met (log 0066). R-01 stays open.
A recommendation is met only after the full-grid stock review in `docs/method.md` (log 0057).
Log 0025 is the stock sheet. Log 0024 records the font decision: the
accessible sheet uses Atkinson Hyperlegible Next with Ō/ō; the stock sheet
keeps Nimbus. The estuary name draws upright (log 0029).
The square uses the sheet map layers. The pink lines were a hidden layer (log 0029).
Square draws use QGIS 4.2.3 at `/Applications/QGIS-final-4_2_3.app` (log 0031). The sheet export stays on the map image. QGIS 3.36.3 cannot open the project (log 0030).
R-09 is open again (log 0058). Floors hold. Spot heights need their own rank. Names collide or sit away from their feature on the grid. Suburb and Locality are 11 px. Town is 14 px. City is 17 px (log 0032).
R-07 is met. Label ink is at least 4.8:1 against the drawn buffer. The text-contrast table has no fail rows except the two highway shields (log 0033).
R-10 is met. Scrub is `#A3CC90` at alpha 26 plus `third_arc` plant marks (log 0068). Scattered is `#E0EDD8` plus a pattern (log 0034).
R-11 is met (log 0066). Closed tracks use `cross2` 0.7 mm every 3 mm (log 0094). That mark does not read as a railway, an embankment or a cliff on the G1 cells. Historic labels keep hue and meet 3:1 under red light (log 0035).
R-17 is met. Hot is a black ×. Cold is a `#005C8F` circle. Native is `#E1EAC3`. Scrub keeps its plant marks. Contour-number FontMarkers use the index ink (logs 0036, 0051).
R-01 is open again (log 0058). Index contour on scrub is 4.35:1 grey and 3.02:1 red after scrub alpha 26 (log 0063). Streams `#004C99` are 8.42:1 grey (log 0083) and shelterbelts `#1D9D00` are 3.57:1 on paper. Grid `#269FD2` is 3.01:1. Intermediate contours have a 0.2 mm `#7A5542` casing at alpha 0.5. Index is 0.35 mm at alpha 0.85. Index versus paper is 4.60:1 grey and 3.28:1 red. Intermediate casing versus paper is 2.23:1 grey and 1.89:1 red. Index versus urban still fails. Road fill `#EC7000` is 3.06:1 grey. The dark road casing still carries the road under red light (logs 0037, 0038, 0050, 0051, 0053, 0054).
R-05 is open again (log 0059). Contour-number FontMarkers are Regular in the apply step. Natural-feature names use index brown, Regular (logs 0072, 0080). Both still need the grid review.
R-08 stays provisional. Vector labels use 0.05 em from the style file. Raster along-line labels keep normal spacing. No A/B test (log 0039).
R-12 is met. `tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false. Access is not drawn (log 0042).
R-03 stays open. Hillshade is an overlay at 337.5°. Raster shade waits for `dem.tif` beside the project. Vector reads the same numbers (log 0044).
R-14 is met. Pair colours that live in `tools/style-topo50.json` are dotted paths. C6 resolves them before it measures (log 0045).
R-13 stays open. Greyscale-safe print and high-contrast web inks are not named. Do not invent palettes (log 0046).
R-15 is met. The vector style is the raster style on Shortbread tiles. `P` holds no colour hex (log 0047).
R-04 is met on the painted Map5View inks. Index is `#7A5542` at 0.85. Intermediate is `#B08872` at 0.5. Road fill is `#EC7000`. Highways stay `#E31A1C`. Contour numbers stay opaque in the index ink. Pipeline is not on Map5View (logs 0050, 0051, 0053, 0054).
The starting point remains LINZ's `topo-raster-gridded`, i.e.
Topo50 itself (log 0023, R-18). IDs are stable;
reference them from commits and research-log entries. The board needs mermaid
with `kanban` support (11.4+); validated with mermaid 12.2.0.

## Board

```mermaid
---
config:
  kanban:
    ticketBaseUrl: '#'
---
kanban
  done[Done]
    d1[Research: 30 findings, 18 recommendations, graded sources]@{ ticket: logs-0001-0010 }
    d2[Topo50 print legend audit and real-render simulations]@{ ticket: log-0019 }
    d3[Astro site, evidence Sankey, vision comparisons, self-checks]@{ ticket: log-0021 }
    d4[Re-scope to topo-raster-gridded; Topo50 QGIS cartography analysed]@{ ticket: log-0023 }
    d5[Font decision: accessible sheet uses Atkinson Next with Ō/ō]@{ ticket: B-28 }
    d6[Stock BX24 sheet from the LINZ map container]@{ ticket: B-22 }
    d7[Topo50 data path for BX24 documented]@{ ticket: B-23 }
    d8[Pair file: line-on-fill pairs and inventory classes]@{ ticket: B-40 }
    d9[Site page: ink contrast matrix]@{ ticket: B-41 }
  ready[Ready]
    b01[Decide history slim then push to GitHub]@{ ticket: B-01, priority: 'Very High' }
    b02[First CI run on GitHub]@{ ticket: B-02, priority: 'Very High' }
    b03[Preview topo-raster-gridded on live tiles]@{ ticket: B-03, priority: 'High' }
    b26[Check whether raster tiles bake in relief shading]@{ ticket: B-26, priority: 'High' }
    b15[Headtorch swatch experiment]@{ ticket: B-15, priority: 'High' }
    b10[File Atkinson Next O-macron issue or PR]@{ ticket: B-10, priority: 'Low' }
  next[Next - QGIS fork]
    b25[Labels: upright and size floor via style override]@{ ticket: B-25, priority: 'Very High' }
    b11[Swap accessible labels to Atkinson Next with Ō/ō]@{ ticket: B-11, priority: 'Very High' }
    b24[Symbology: contours, closed tracks, springs, forest vs scrub]@{ ticket: B-24, priority: 'Very High' }
    b29[Audit rendered sheets: inks, pairs, simulations]@{ ticket: B-29, priority: 'High' }
    b04[Captures of stock vs accessible Topo50 for site]@{ ticket: B-04, priority: 'High' }
  review[Next - grid review fixes]
    b42[Loop prompt runs the full-grid review]@{ ticket: B-42, priority: 'High' }
    b35[Streams at least 3:1 on paper and fills]@{ ticket: B-35, priority: 'Very High' }
    b34[Scrub keeps contours at 3:1]@{ ticket: B-34, priority: 'High' }
    b36[Shelterbelts and green dots visible]@{ ticket: B-36, priority: 'High' }
    b31[Label fit counts symbols and keeps names near features]@{ ticket: B-31, priority: 'High' }
    b32[Natural-feature names get a non-italic cue]@{ ticket: B-32, priority: 'High' }
    b37[Contour numbers upright with a line gap]@{ ticket: B-37, priority: 'High' }
    b33[Spot-height rank and urban halo]@{ ticket: B-33, priority: 'Low' }
    b43[Draw BX24 hillshade and review on the grid]@{ ticket: B-43, priority: 'Low' }
    b38[Forest tree glyph visible]@{ ticket: B-38, priority: 'Low' }
    b39[Dual names stay one block]@{ ticket: B-39, priority: 'Low' }
  later[Later]
    b27[Render accessible raster tiles for a region and serve]@{ ticket: B-27, priority: 'High' }
    b14[Greyscale and high-contrast variants]@{ ticket: B-14, priority: 'Low' }
    b16[Deploy site to GitHub Pages]@{ ticket: B-16, priority: 'High' }
    b17[Site dark theme]@{ ticket: B-17, priority: 'Very Low' }
    b18[Show replication in chain grades]@{ ticket: B-18, priority: 'Very Low' }
  validate[Validation]
    b20[User testing plan and recruitment]@{ ticket: B-20, priority: 'Very High' }
    b21[Run sessions and log results]@{ ticket: B-21, priority: 'Very High' }
  secondary[Secondary - web vector style]
    b05[Tune topographic-v2 contour weight]@{ ticket: B-05, priority: 'Very Low' }
    b06[Tune multidirectional hillshade]@{ ticket: B-06, priority: 'Very Low' }
    b07[Glyph PBFs include macrons]@{ ticket: B-07, priority: 'Very Low' }
    b08[MBTiles contour definition attribute]@{ ticket: B-08, priority: 'Very Low' }
    b09[Dashed indefinite contours]@{ ticket: B-09, priority: 'Very Low' }
    b19[Audit tool reads interpolated colours]@{ ticket: B-19, priority: 'Very Low' }
```

The coloured bar on each card is mermaid's priority marker (red = very high,
orange = high, dark blue = low, pale blue = very low). It's colour-only, so
priority is also written out in the table.

**Secondary track:** `styles/accessible-v0*.json` (derived from
`topographic-v2`) remains valid work and stays gated in CI, but it is not the
product. Its research and decisions carry over to the QGIS fork.

## Items

| ID | Priority | Item | Done when | Depends on | Refs |
|---|---|---|---|---|---|
| B-01 | Very High | Decide whether to drop superseded composite PNGs from history; create GitHub repo; push | Pushed; decision logged | — | OQ-14 |
| B-02 | Very High | First GitHub Actions run (`check`, `site`) | Both green on `main` | B-01 | R-14 |
| B-22 | Very High | Build LINZ's `map` container (`topographic-system/packages/map`) and render one sheet (e.g. BX24) with the **stock** `topographic-qgis` project | Stock PDF/PNG of one sheet committed as baseline | — | R-18 |
| B-23 | Very High | Obtain Topo50 GeoParquet data for that sheet (NZTopo50 QGIS plugin download or the project JSON referenced in `packages/map/README.md`) | Data path documented; render reproducible | — | R-18 |
| B-28 | High | Check AGPL-3.0 (+ font exemption) obligations if we modify or swap Nimbus Sans LINZ | Decision logged | — | R-18, R-06 |
| B-03 | High | Extend `preview/` to show `topo-raster-gridded` side by side; run on live tiles | Raster panes render | — | — |
| B-26 | High | Do served raster tiles include baked relief shading? Only then decide on the client hillshade direction for the raster style | Answer + decision logged | B-03 | R-03 |
| B-15 | High | Headtorch swatch experiment (print the six Topo50 inks + proposed inks) | Photos + measured contrast | — | OQ-08, F-21 |
| B-10 | Low | File Atkinson Next Ō/ō issue/PR (less urgent: QGIS shapes text, F-28) | URL logged | — | OQ-10 |
| B-25 | Very High | QML override: label FontStyle → upright; size floor (≥7 pt default, 6 pt min) | Re-rendered sheet; italic share 0% | B-22, B-23 | R-05, R-09, F-30 |
| B-24 | Very High | QML symbology: index/intermediate contours, closed-track symbol, distinct spring glyphs, forest vs scrub step, no red-orange-only meaning | Print audit pairs pass floors on re-render | B-22, B-23 | R-04, R-11, R-17 |
| B-29 | High | Audit rendered sheets (palette pairs, simulations) and add to site comparisons | Before/after on site | B-24, B-25 | R-14 |
| B-04 | High | Captures of stock vs accessible Topo50 at the 7 scenarios | On the site | B-27 or B-29 | R-16 |
| B-11 | Very High | Accessible QGIS labels use Atkinson Hyperlegible Next with Ō/ō added (OFL patch). Stock sheet stays Nimbus | Accessible sheet uses the patched face, beside the stock sheet | B-22, B-23 | R-06, F-26, F-28, F-29, log 0024 |
| B-27 | High | Render accessible raster tiles for a region; serve alongside `topo-raster-gridded` | Preview shows both | B-24, B-25 | R-18 |
| B-14 | Low | Greyscale-safe print and high-contrast variants from the QGIS fork | Variants rendered + gated | B-24 | R-13 |
| B-16 | High | Deploy site (GitHub Pages, `SITE_BASE`) | Public URL | B-02 | — |
| B-17 | Very Low | Site dark theme | S1–S3 pass in both schemes | — | — |
| B-18 | Very Low | Replication shown in chain grades | Trace page updated | — | — |
| B-20 | Very High | User testing plan + recruitment | Plan doc | B-24, B-25 | R-16 |
| B-21 | Very High | Run sessions; log results | Grade-B findings from our own study | B-20 | R-16 |
| B-40 | Very High | Add line-on-fill pairs (index and intermediate contour, stream, track on scrub, native, water, urban) and the log 0060 classes (stream `#009EFF`, shelterbelt `#94FF3B`, grid) to `tools/pairs-topo50-accessible.json`. Keep the ink list in one data file the site can read | Audit reports every pair; new fails named | — | R-01, R-14, logs 0058, 0060, 0061 |
| B-41 | High | Site page: ink contrast matrix. Every painted ink against every other (contour vs stream, contour vs scrub, stream vs scrub, …). Each cell shows contrast in normal, grey and red light and the worst dichromacy ΔE, with a line-on-fill swatch. Use the `palette_audit.py` models; no new vision model | Page on the site; passes S1–S3. **Done:** `/inks/` lists every pair in the pair file (log 0062) | B-40 | R-01, R-14, logs 0060, 0062 |
| B-42 | High | Loop prompt Step B renders the 4 km grid and runs the stock review before it marks a recommendation met | Prompt updated | — | log 0057 |
| B-30 | Very High | Closed-track symbol that does not read as a railway, embankment or cliff where tracks are dense. Ideas: fewer bars, an ×, mask bars under labels. **Conflict:** a bar every 4 mm looked open (log 0056); one × per gap dominated the 4 km grid. **Done:** `cross2` 0.5 mm every 3 mm. G1 passed. R-11 met (log 0066). Josh: "slightly bolder and larger", so 0.7 mm with a 0.15 mm stroke; still not a railway, embankment or cliff (log 0094) | Grid review passes G1; R-11 "Met when" | — | R-11, G1, logs 0057, 0063, 0064, 0065, 0066 |
| B-35 | Very High | Streams ≥3:1 on paper and on scrub/native fills. Darker blue or wider line. Check against the contour mesh on steep slopes. **Pairs:** stream `#0064BD` passes paper and fills (log 0063). **Style XML:** rivers and canals 0.25 mm, drains 0.15 mm. A 0.35 mm floor on every blue line was undone (logs 0070, 0071). Stream `#004C99`: index vs stream 1.83:1 grey, was 1.28 (log 0083). **Closed pair (Josh, log 0093):** index vs stream counts as met by the width step (0.25 vs 0.35 mm) plus hue and red light (6.41:1) | Pairs pass; grid review passes G6 | B-40 | R-01, G6, F-31, logs 0057, 0060, 0063, 0067, 0070, 0071, 0083, 0093 |
| B-34 | High | Rebalance scrub (lighter fill or lower alpha, hatch carries the class) so the index contour is ≥3:1 on scrub. **Pairs:** scrub alpha 26, index vs scrub 4.35:1 grey and 3.02:1 red (log 0063). **Style XML:** pale fill plus stock `third_arc` 1.4 mm at 3 mm (logs 0068, 0070). A greener raster fill needs the vector build to apply scrub alpha first (log 0076) | Pair passes; grid review passes G5 | B-40 | R-01, R-10, G5, F-31, logs 0057, 0063, 0067, 0068, 0070 |
| B-36 | High | Shelterbelt line and green dots ≥3:1, or a dark edge. **Pairs:** shelterbelt `#1D9D00` passes paper and native (log 0063). **Style XML:** shelterbelt keeps stock 0.25 mm in `#1D9D00` (log 0071) | Pair passes | B-40 | R-01, F-31, logs 0060, 0063, 0070, 0071 |
| B-31 | High | Fit tool counts point symbols, spot heights and track bars, and penalises distance from the anchor. **Measured:** 134 new collisions over 0.8 mm² vs stock after a 3 mm reach (was 158). Multi-line names now fit: 116 (log 0074). Road suffixes abbreviate when the name overruns its baseline: 114 (log 0075). Parallel curved road names (MARINE DRIVE, BAYVIEW RD) still collide. Spot heights no longer move (they drifted up to 3.4 mm off their dots): 125 (log 0077). Heights back at 6 pt: 111 (log 0084). Flat names drop stock alignment padding: 105 (log 0085). Straight names stored one segment per letter join the fit: 98 (log 0086). Fit costs ink within 0.72 mm beside or 0.4 mm above or below a neighbour: 93 (log 0087). Every flat name is pinned where the fit put it, and the band is 0.6 mm above or below: 92 (log 0088). The fit masks match the render to 0.04 mm; the "worse" stacked pairs are box overlaps with a 0.6 mm or wider ink gap (log 0089) | Grid review passes G2; R-09 placement test | — | R-09, G2, logs 0052, 0057, 0073, 0074, 0075, 0077, 0084, 0085, 0086, 0087, 0088, 0089 |
| B-32 | High | Natural-feature names get a non-italic cue (index brown, weight or case), read from the carto_text `style` value. **Style XML:** Bold never drew: the face has no Bold file, and Narrow settlements were also mapped. Now black italic names and spot heights take index brown `#7A5542` (log 0072). Patched Atkinson Bold now draws the five stock Bold town names. Natural names stay Regular brown: Bold on every italic made heights and water names heavy (log 0080). Spot heights stay black, apart from brown contour numbers (log 0081) | Grid review passes G3; R-05 | — | R-05, F-08, G3, logs 0057, 0059, 0063, 0072, 0079, 0080, 0081 |
| B-37 | High | Contour numbers upright Atkinson ≥6 pt; QGIS selective mask breaks the contour under the number. **Style XML:** FontMarker Regular, size ≥6 pt; casing mask kept (log 0063). The face only applied after log 0082: FontMarker reads `font`/`font_style`. 0.3 mm white halo under each digit (log 0082) | Italic count 0 incl. FontMarkers; R-05, R-17 P8 | — | R-05, R-17, logs 0059, 0063, 0082 |
| B-33 | Low | Spot heights at the 6 pt rank; label halo on urban fill matches `#BCBAB6` (black on it is 10.8:1). **Style XML:** `relief_point` buffer uses urban fill (log 0063). Spot heights are carto_text, so the 7 pt name floor had lifted them; they now keep 6 pt (log 0084). **R-09 rank step:** Josh accepts 17% as a written exception. Colour, digits and position carry the rank (log 0093) | Grid review passes G4 | — | R-09, R-07, G4, logs 0057, 0063, 0084, 0093 |
| B-43 | Low | Drop a DEM as `dem.tif` beside the BX24 project; draw the 337.5° shade; review Port Hills on the grid | Grid review | — | R-03 |
| B-38 | Low | Forest tree glyph visible on its pale fill. **Style XML:** apply paints `vegetation.native.marker` `#3F6B32` when a marker layer is already in the project. BX24 native is fill-only (log 0063) | Grid review | — | R-10, R-17, log 0063 |
| B-39 | Low | Dual names (`Whakaraupō / Lyttelton Harbour`, `Port Levy (Potiriwi)`) stay one block; no orphan `/` | Grid review | — | F-13 |
| B-44 | Medium | State highway numbers draw. The stock number layer reads a LINZ staff Downloads path, so no number draws in stock. **Done:** the number reads the symbol source, uses the raster face and `#940000`, and sits in a white shield above the road (log 0090). "74A" is a little wider than the shield | Numbers on the grid | — | R-07, R-06, log 0090 |
| B-45 | Medium | Black names on urban fill get an urban-fill halo, not a white hole (G4). A render-time `overlay_intersects` on `residential_area map` hangs the parallel render job (log 0090). **Done (log 0093):** Josh chose a precomputed flag. `tools/tag_urban_text.py` writes `urban_text.json` (3456 ids for the country). The apply step reads it into a static `"id" IN (...)` halo colour. Black names in the list take `#BCBAB6`. Brown and blue names keep the paper halo. The BX24 render does not hang (55 s). The sheet project still needs the tag step | Grid review passes G4 | — | R-07, G4, logs 0090, 0093 |
| B-46 | High | Sheet legend shows the accessible swatches. The legend is a picture with the labels as pixels. **Done:** 18 rows draw from the applied layers over the stock image (log 0092). 14 row groups still show stock looks; log 0092 lists them. Swatches stay at true sheet size (Josh, 2026-11-05). The track rows now show foot dashes, closed ×, and poled-route dots (log 0094). Josh to decide any new legend text | Every swatch row matches the map | — | log 0092 |
| B-47 | High | Symbol definition table: every stock legend symbol with its LINZ crop, our symbol, measured inks and sizes against R-01, R-11, R-17 and F-31, and a proposal that keeps the LINZ shape. **Done:** `/symbols/` lists 126 symbols. 38 done, 34 proposed, 54 blocked (log 0095) | Page on the site; passes S1–S3 | B-46 | R-01, R-11, R-17, F-31, log 0095 |
| B-48 | High | Apply the approved symbol proposals from `/symbols/`. Josh reviews first: locked-gate cue, fumarole size, tree size, scattered scrub, vegetation outline `#859E3E`, gas pipeline `#951600`, bivouac glyph, and which hidden layers the sheet shows | Every proposed row done on the grid | B-47 | R-01, R-11, R-17, F-31, log 0095 |
| B-05–B-09, B-19 | Very Low | Secondary web-vector track (see board) | — | — | logs 0013–0020 |
