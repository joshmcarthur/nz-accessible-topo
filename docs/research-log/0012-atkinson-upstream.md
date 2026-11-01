# 0012 — Is the Atkinson Ō/ō gap known or fixed upstream? (OQ-10)

**Date:** 2026-11-01

## Question
Is the missing Ō/ō in Atkinson Hyperlegible Next (F-10) already fixed in the
upstream repo or reported?

## What we did
- Web search for an existing report: none found.
- Shallow-cloned `googlefonts/atkinson-hyperlegible-next`. HEAD is `7925f50`
  (2025-02-21) — the same commit google/fonts ships, so no newer build exists.
- Grepped the `.glyphs` sources: `Amacron`, `amacron`, `Emacron`, `emacron`,
  `Imacron`, `imacron`, `Umacron`, `umacron` are present; `Omacron` and
  `omacron` are **absent**. All built TTFs lack U+014C/U+014D.
- Checked `OFL.txt`: no Reserved Font Name is declared, so a patched build
  would be licence-permissible (OFL §3 only restricts names that are
  reserved).

## What we found
- The gap is real in the sources, not a packaging issue.
- Fix is likely small (two composites per master).

## What changed
- `docs/upstream/atkinson-next-omacron-issue.md` — a ready-to-file issue.
- OQ-10 → answered: *not fixed; not found reported; draft issue written.*

## Confidence & gaps
- Could not read the GitHub issue tracker directly (API rate limit). Search
  absence is weak evidence of non-reporting — check before filing.
