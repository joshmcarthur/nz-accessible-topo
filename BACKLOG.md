# Backlog

Ordered work for the next phase (local development). IDs are stable; link
them from commits and research-log entries like R-/F-/OQ- IDs.
Status as of 2026-11-01, commit after log 0022.

## Dependency map

```mermaid
flowchart LR
  subgraph now["1. First local session"]
    B01["B-01 Decide history slim<br/>(OQ-14) then push"]
    B02["B-02 First CI run<br/>on GitHub"]
    B03["B-03 Run preview with<br/>LINZ key, fix URLs"]
    B04["B-04 Live-tile captures<br/>compare.mjs"]
  end
  subgraph tune["2. Tune against real terrain"]
    B05["B-05 Contour weight<br/>(OQ-09, R-04)"]
    B06["B-06 Multidirectional<br/>shading colours (OQ-07)"]
    B07["B-07 Glyph PBFs have<br/>macrons (OQ-13)"]
    B08["B-08 MBTiles: contour<br/>definition attr (OQ-12)"]
    B09["B-09 Dashed indefinite<br/>contours (R-04)"]
  end
  subgraph fonts["3. Fonts"]
    B10["B-10 File Atkinson Ō/ō<br/>issue or PR (OQ-10)"]
    B11["B-11 Atkinson web glyph<br/>stack trial (R-06)"]
  end
  subgraph print["4. Print"]
    B12["B-12 Print toolchain<br/>decision: QGIS (R-13)"]
    B13["B-13 Print fixes:<br/>springs, forest/scrub (R-17)"]
    B14["B-14 Greyscale + high-<br/>contrast variants (R-13)"]
    B15["B-15 Headtorch swatch<br/>test (OQ-08)"]
  end
  subgraph site["5. Site"]
    B16["B-16 Deploy site<br/>(GitHub Pages)"]
    B17["B-17 Dark theme"]
    B18["B-18 Show replication<br/>in chain grades"]
    B19["B-19 Audit tool reads<br/>interpolated colours"]
  end
  subgraph users["6. Validation"]
    B20["B-20 User testing plan<br/>+ recruitment (R-16)"]
    B21["B-21 Run sessions,<br/>log results"]
  end

  B01 --> B02 --> B16
  B03 --> B04 --> B05 & B06
  B04 --> B16
  B08 --> B09
  B05 --> B09
  B07 --> B11
  B10 --> B11
  B12 --> B13 --> B14
  B15 --> B13
  B05 & B06 & B13 --> B20 --> B21
  B19 --> B05
```

## Items

| ID | Item | Why / evidence | Done when | Refs |
|---|---|---|---|---|
| B-01 | Decide whether to drop superseded composite PNGs from history, then create the GitHub repo and push | Repo is ~22 MB because of old `docs/visuals/02-*` / `07-*` versions | Pushed; decision noted in log | OQ-14 |
| B-02 | First GitHub Actions run of `check` and `site` jobs | Workflow has only been run locally from a clean clone | Both jobs green on `main` | R-14 |
| B-03 | Run `preview/` against live LINZ tiles; fix URL rewriting / sprite paths if needed | Written and validated, never run on real tiles | Both panes render, sprites (stipple, cross-bars) visible | — |
| B-04 | Run `tools/screenshots/compare.mjs` for all 7 scenarios; commit captures; log what they show | Replaces synthetic scenes with real terrain | `docs/visuals/real/*/none.png` committed; site shows them | R-16 |
| B-05 | Tune contour weight on steep terrain (Arthur's Pass, Fiordland) | v0 intermediates may still be heavy; index must carry relief under red light | Before/after captures + gate floors updated | OQ-09, R-04 |
| B-06 | Tune multidirectional hillshade colours/weights | Values are provisional; never seen on real terrain | Alpine and plains captures look right; R-03 log entry | OQ-07, R-03 |
| B-07 | Fetch LINZ glyph PBF range 256–511 for every font stack used; confirm Ā–Ū | Our macron check used google/fonts builds, not LINZ-served glyphs | Script + result in log; gate C5 updated if needed | OQ-13, F-12 |
| B-08 | Download `topographic-v2` MBTiles; inspect contour attributes | Need `definition = indefinite` for dashed contours | Attribute list recorded in `tile-attributes.md` | OQ-12 |
| B-09 | Dashed indefinite contours | Accuracy is lower in forest/snow; should be visible | Style transform + gate | R-04, F-18 |
| B-10 | Check tracker, file Atkinson Next Ō/ō issue (or PR with two composites) | Draft ready in `docs/upstream/` | Issue/PR URL in log | OQ-10, F-29 |
| B-11 | Trial Atkinson Next on web (patched or upstream-fixed) with self-built glyph PBFs | Better I/l/1 and O/0 separation for grid refs and trig IDs | Side-by-side capture + decision | R-06, F-28 |
| B-12 | Choose print toolchain (likely QGIS project generated from the same parameters) | Print output doesn't exist yet | Decision log + skeleton project | R-13 |
| B-13 | Implement print-specific fixes | Springs fail greyscale; forest vs scrub tint-only; italics in contour labels | Print audit pairs pass floors | R-17, P3–P9 |
| B-14 | Greyscale-safe print and high-contrast web variants | Photocopies, e-ink, low vision | Variants built + gated | R-13, F-23 |
| B-15 | Headtorch swatch experiment: print swatches, photograph under red/white modes | Red-light evidence is anecdotal + model | Photos + measured contrast in log | OQ-08, F-21 |
| B-16 | Deploy site (GitHub Pages; set `SITE_BASE`) | Site builds; not hosted | Public URL; Pages job in CI | — |
| B-17 | Dark theme for the site | Quality floor; maps stay on white | Passes S1–S3 in both schemes | — |
| B-18 | Show replication in chain grades (e.g. "B ×2 replicated") | "Best single source" understates F-14 | Grades on trace page reflect replication | — |
| B-19 | `palette_audit.py` evaluates interpolated/zoom colours | Index contours were missed in the first audit | Audit reports per-zoom values | log 0013 |
| B-20 | User testing plan + recruitment (tramping club, LandSAR, CVD, dyslexic and 60+ readers) | All perceptual claims are grade D until tested | Plan doc + ethics/consent approach | R-16 |
| B-21 | Run sessions; log results; revise recommendations | Closes the evidence loop | Findings with grade B from our own study | R-16 |

## Not in scope (yet)
- Track access status on the map (R-12): needs Walking Access Commission data.
- 1:25k products.
