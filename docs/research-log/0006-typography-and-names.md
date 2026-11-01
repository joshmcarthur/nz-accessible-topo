# 0006 — Typography, dyslexia, low vision, and Māori place names

**Date:** 2026-11-01

## Question
What does the evidence say about label typography for dyslexic and
low-vision readers, and what constraints do NZ place names add?

## What we did
- Read the Rello & Baeza-Yates eye-tracking studies; Kuster et al. and the
  IDA summary of Wery & Diliberto on dyslexia fonts; Zorzi et al. on letter
  spacing and a 2018 follow-up.
- Read cartographic labelling guidance (Axis Maps, Colorado *Making Maps*,
  Esri, Minnesota IT) for conventions and size minimums.
- Wrote `tools/font_check.py` and ran it on six open fonts from google/fonts
  to check macron coverage and x-height.
- Read NZGB/LINZ notices on official Māori names and macrons.

## What we found
- Strong agreement: roman sans-serif good, italics bad, dyslexia fonts no
  better, spacing helps (F-05 – F-07).
- Conflict with cartographic convention of italic water names (F-08).
- **Measured:** Atkinson Hyperlegible Next lacks Ō/ō — the most common
  macron vowel in NZ place names — so it is blocked for this project until
  fixed upstream or patched (F-10).
- Open Sans, already used by LINZ, has full macron support and the largest
  x-height of the candidates (F-11).

## What changed
- `docs/findings/typography.md`, `docs/findings/te-reo-maori-names.md`,
  `tools/font_check.py`; sources added.

## Confidence & gaps
- Dyslexia studies are about continuous reading, mostly by children. Map
  labels are single words scanned in clutter. Transfer is plausible (crowding
  is the mechanism) but unproven for maps. OQ-06.
- Did not check whether an upstream issue already exists for Atkinson Ō/ō.
