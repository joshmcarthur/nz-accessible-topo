# Backlog

Status as of 2026-11-02, after log 0044 (R-03 optional hillshade overlay).
Log 0025 is the stock sheet. Log 0024 records the font decision: the
accessible sheet uses Atkinson Hyperlegible Next with Ō/ō; the stock sheet
keeps Nimbus. The estuary name draws upright (log 0029).
The square uses the sheet map layers. The pink lines were a hidden layer (log 0029).
Square draws use QGIS 4.2.3 at `/Applications/QGIS-final-4_2_3.app` (log 0031). The sheet export stays on the map image. QGIS 3.36.3 cannot open the project (log 0030).
R-09 is met. Suburb and Locality are 11 px. Town is 14 px. City is 17 px (log 0032).
R-07 is met. Label ink is at least 4.8:1 against the drawn buffer. The text-contrast table has no fail rows except the two highway shields (log 0033).
R-10 is met. Scrub is `#A3CC90` plus a hatch. Scattered is `#E0EDD8` plus a pattern (log 0034).
R-11 is met. Closed tracks have cross-bars. Historic labels keep hue and meet 3:1 under red light (log 0035).
R-17 is met. Hot is a black ×. Cold is a `#005C8F` circle. Native is `#E1EAC3`. Scrub keeps the hatch (log 0036).
R-01 is met. Intermediate contours have a 0.2 mm `#8A4F1C` casing. Index is 0.45 mm. Casing versus paper is 3.45:1 under red light (logs 0037, 0038).
R-08 stays provisional. Vector labels use 0.05 em from the style file. Raster along-line labels keep normal spacing. No A/B test (log 0039).
R-12 is met. `tracks.access.reserved_channel` is `casing_colour`. `tracks.access.painted` is false. Access is not drawn (log 0042).
R-03 stays open. Hillshade is an overlay at 337.5°. Raster shade waits for `dem.tif` beside the project. Vector reads the same numbers (log 0044).
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
| B-05–B-09, B-19 | Very Low | Secondary web-vector track (see board) | — | — | logs 0013–0020 |
