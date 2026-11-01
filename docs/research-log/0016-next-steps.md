# 0016 — Status and next steps

**Date:** 2026-11-01

## Where we are
Research → recommendations → a generated, validated, CI-gated style. Every
shipped colour change traces to an R-id in `docs/styles/*-changes.md`.

## Next, in priority order
1. **Push and run.** First CI run on GitHub; first preview run against live
   LINZ tiles (fix URL rewriting if needed).
2. **Eyes on terrain (OQ-07, OQ-09).** Compare at Arthur's Pass (steep),
   Canterbury Plains (flat), Tongariro (volcanic, scree). Tune contour weight
   and multidirectional colours; record before/after screenshots in the log.
3. **OQ-13.** Fetch LINZ glyph PBF range 256–511 per font stack; confirm Ō/ō.
4. **OQ-12 remainder.** Download the MBTiles export; check for contour
   `definition` to enable dashed indefinite contours (R-04).
5. **Print (R-13, OQ-02).** Get a Topo50 legend; decide print toolchain
   (QGIS with the same parameters is the likely "boring tech" route).
6. **File the Atkinson issue** (`docs/upstream/`) after checking the tracker.
7. **User testing (R-16).** Recruit via a tramping club / LandSAR.
