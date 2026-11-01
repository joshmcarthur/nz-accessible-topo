# 0007 — Relief shading, contours, and which standards apply

**Date:** 2026-11-01

## Question
(1) Is LINZ's NW relief lighting the best choice? (2) Which accessibility
standards apply to a topo map, and what targets should we hold ourselves to?

## What we did
- Read Biland & Çöltekin (2017), its 2018 replication, Çöltekin & Biland
  (2019) on colour/texture, and two ICA abstracts (2023, 2025).
- Read W3C's Understanding 1.4.11 and the NZ Web Accessibility Standard 1.2.

## What we found
- NNW beats NW for landform perception, replicated (F-14). In NZ, NNW is also
  where the real sun is — a rare case where research and realism agree
  (F-15). Multidirectional sky shading helps further (F-16).
- NZ's standard has a complex-maps exception; we'll still use WCAG ratios as
  targets (F-19, F-20).

## What changed
- `docs/findings/relief-and-contours.md`, `docs/findings/standards.md`

## Confidence & gaps
- Relief studies used foreign terrain; NZ has extreme relief (Southern Alps)
  and very subtle relief (Canterbury Plains) — test both. OQ-07.
