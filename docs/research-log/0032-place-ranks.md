# 0032 — Place label ranks

**Date:** 2026-11-02

## Question

Do the named place ranks meet the R-09 20% step?

## What we did

Josh named the ranks. Suburb and Locality are one rank. Town is the next rank. City is the rank after Town. Island labels are a second ladder.

The island layer ids are zoom bands. The number is the max zoom. This step does not name adjacent island ranks. It does not change those sizes.

## What we found

Suburb and Locality stay at 11 px. Town is 14 px. 14/11 is 1.27. City is 17 px. 17/14 is 1.21. Both steps are at least 20%. 13 px is 18% above 11 px, so Town is 14 px.

`Place-Label-City-14` and `Place-Label-City-7` are both 17 px. `Place-Label-Island-12` stays 12 px. The other island layers stay 14 px.

The print size floors did not change. The square pictures did not change. This step did not draw them again.

The pair audit is unchanged. Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/style-topo50.json` holds the three place ranks.
- `tools/build_style.py` writes those sizes into the vector style.
- `styles/accessible-v0.json` has Town at 14 px and City at 17 px.

## Confidence & gaps

R-09 is met for this list. The next step is R-07.
