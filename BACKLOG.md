# Backlog

Ordered work for the next phase (local development). IDs are stable; link
them from commits and research-log entries like R-/F-/OQ- IDs.
Status as of 2026-11-01, commit after log 0022. The board needs a mermaid
version with `kanban` support (11.4+); validated with mermaid 12.2.0.

## Board

```mermaid
---
config:
  kanban:
    ticketBaseUrl: '#'
---
kanban
  done[Done]
    d1[Research: 29 findings, 17 recommendations, graded sources]@{ ticket: logs-0001-0010 }
    d2[accessible-v0 web styles built from LINZ upstream]@{ ticket: log-0014 }
    d3[CI gates C1-C6 and style validation]@{ ticket: log-0015 }
    d4[Real Topo50 print legend audit]@{ ticket: log-0019 }
    d5[Astro site with evidence Sankey and vision comparisons]@{ ticket: log-0021 }
    d6[Site gates S1-S3 and live-capture ingestion]@{ ticket: log-0022 }
  ready[Ready - first local session]
    b01[Decide history slim then push to GitHub]@{ ticket: B-01, priority: 'Very High' }
    b02[First CI run on GitHub]@{ ticket: B-02, priority: 'Very High' }
    b03[Run preview on live LINZ tiles and fix URLs]@{ ticket: B-03, priority: 'Very High' }
    b04[Live-tile captures with compare.mjs]@{ ticket: B-04, priority: 'High' }
    b07[Check LINZ glyph PBFs include macrons]@{ ticket: B-07, priority: 'High' }
    b08[Inspect MBTiles for contour definition attribute]@{ ticket: B-08, priority: 'High' }
    b10[File Atkinson Next O-macron issue or PR]@{ ticket: B-10, priority: 'High' }
    b15[Headtorch swatch experiment]@{ ticket: B-15, priority: 'High' }
  next[Next - needs real terrain]
    b05[Tune contour weight on steep terrain]@{ ticket: B-05, priority: 'High' }
    b06[Tune multidirectional hillshade colours]@{ ticket: B-06, priority: 'High' }
    b09[Dashed indefinite contours]@{ ticket: B-09, priority: 'Low' }
    b19[Audit tool reads interpolated colours]@{ ticket: B-19, priority: 'Low' }
    b16[Deploy site to GitHub Pages]@{ ticket: B-16, priority: 'High' }
  later[Later]
    b11[Trial Atkinson Next on web with own glyph PBFs]@{ ticket: B-11, priority: 'Low' }
    b12[Choose print toolchain]@{ ticket: B-12, priority: 'High' }
    b13[Print fixes - springs, forest vs scrub, italics]@{ ticket: B-13, priority: 'High' }
    b14[Greyscale and high-contrast variants]@{ ticket: B-14, priority: 'Low' }
    b17[Site dark theme]@{ ticket: B-17, priority: 'Very Low' }
    b18[Show replication in chain grades]@{ ticket: B-18, priority: 'Very Low' }
  validate[Validation]
    b20[User testing plan and recruitment]@{ ticket: B-20, priority: 'Very High' }
    b21[Run sessions and log results]@{ ticket: B-21, priority: 'Very High' }
```

The coloured bar on each card is mermaid's priority marker (red = very high,
orange = high, dark blue = low, pale blue = very low). It's colour-only, so
priority is also written out in the table below.

Columns: **Ready** has no unmet dependencies; **Next** waits on live-tile
captures (B-04); **Validation** waits on tuned styles and print fixes. Move a
card by moving its line between columns, and log the move in the research log
when it changes what we believe.

## Items

| ID | Priority | Item | Why / evidence | Done when | Depends on | Refs |
|---|---|---|---|---|---|---|
| B-01 | Very High | Decide whether to drop superseded composite PNGs from history, then create the GitHub repo and push | Repo is ~22 MB because of old `docs/visuals/02-*` / `07-*` versions | Pushed; decision noted in log | — | OQ-14 |
| B-02 | Very High | First GitHub Actions run of `check` and `site` jobs | Workflow has only been run locally from a clean clone | Both jobs green on `main` | B-01 | R-14 |
| B-03 | Very High | Run `preview/` against live LINZ tiles; fix URL rewriting / sprite paths if needed | Written and validated, never run on real tiles | Both panes render, sprites (stipple, cross-bars) visible | — | — |
| B-04 | High | Run `tools/screenshots/compare.mjs` for all 7 scenarios; commit captures; log what they show | Replaces synthetic scenes with real terrain | `docs/visuals/real/*/none.png` committed; site shows them | B-03 | R-16 |
| B-05 | High | Tune contour weight on steep terrain (Arthur's Pass, Fiordland) | v0 intermediates may still be heavy; index must carry relief under red light | Before/after captures + gate floors updated | B-04, B-19 | OQ-09, R-04 |
| B-06 | High | Tune multidirectional hillshade colours/weights | Values are provisional; never seen on real terrain | Alpine and plains captures look right; R-03 log entry | B-04 | OQ-07, R-03 |
| B-07 | High | Fetch LINZ glyph PBF range 256–511 for every font stack used; confirm Ā–Ū | Our macron check used google/fonts builds, not LINZ-served glyphs | Script + result in log; gate C5 updated if needed | — | OQ-13, F-12 |
| B-08 | High | Download `topographic-v2` MBTiles; inspect contour attributes | Need `definition = indefinite` for dashed contours | Attribute list recorded in `tile-attributes.md` | — | OQ-12 |
| B-09 | Low | Dashed indefinite contours | Accuracy is lower in forest/snow; should be visible | Style transform + gate | B-05, B-08 | R-04, F-18 |
| B-10 | High | Check tracker, file Atkinson Next Ō/ō issue (or PR with two composites) | Draft ready in `docs/upstream/` | Issue/PR URL in log | — | OQ-10, F-29 |
| B-11 | Low | Trial Atkinson Next on web (patched or upstream-fixed) with self-built glyph PBFs | Better I/l/1 and O/0 separation for grid refs and trig IDs | Side-by-side capture + decision | B-07, B-10 | R-06, F-28 |
| B-12 | High | Choose print toolchain (likely QGIS project generated from the same parameters) | Print output doesn't exist yet | Decision log + skeleton project | — | R-13 |
| B-13 | High | Implement print-specific fixes | Springs fail greyscale; forest vs scrub tint-only; italics in contour labels | Print audit pairs pass floors | B-12, B-15 | R-17, P3–P9 |
| B-14 | Low | Greyscale-safe print and high-contrast web variants | Photocopies, e-ink, low vision | Variants built + gated | B-13 | R-13, F-23 |
| B-15 | High | Headtorch swatch experiment: print swatches, photograph under red/white modes | Red-light evidence is anecdotal + model | Photos + measured contrast in log | — | OQ-08, F-21 |
| B-16 | High | Deploy site (GitHub Pages; set `SITE_BASE`) | Site builds; not hosted | Public URL; Pages job in CI | B-02, B-04 | — |
| B-17 | Very Low | Dark theme for the site | Quality floor; maps stay on white | Passes S1–S3 in both schemes | — | — |
| B-18 | Very Low | Show replication in chain grades (e.g. "B ×2 replicated") | "Best single source" understates F-14 | Grades on trace page reflect replication | — | — |
| B-19 | Low | `palette_audit.py` evaluates interpolated/zoom colours | Index contours were missed in the first audit | Audit reports per-zoom values | — | log 0013 |
| B-20 | Very High | User testing plan + recruitment (tramping club, LandSAR, CVD, dyslexic and 60+ readers) | All perceptual claims are grade D until tested | Plan doc + ethics/consent approach | B-05, B-06, B-13 | R-16 |
| B-21 | Very High | Run sessions; log results; revise recommendations | Closes the evidence loop | Findings with grade B from our own study | B-20 | R-16 |

## Not in scope (yet)
- Track access status on the map (R-12): needs Walking Access Commission data.
- 1:25k products.
