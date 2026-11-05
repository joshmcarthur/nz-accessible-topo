# 0079 — Town names lose their bold weight

**Date:** 2026-11-05

## Question

Do any stock label cues disappear on the accessible face, apart from the
italic natural-feature cue (log 0072)?

## What we did

Compared `1572000-5178000` (central Christchurch) and the coast cells.
Counted carto_text `style` values that contain Bold on the BX24 extent.
Checked the earlier "split road name" lead.

## What we found

- Five names are Narrow Bold in stock: CHRISTCHURCH (17 pt), Belfast,
  Sumner, Lyttelton (9.5 pt), and Diamond Harbour (8.5 pt). They are the
  top settlement rank. The accessible face draws them Regular, because
  the patched face (`NZATLegibleTest-Regular.ttf`) is the only file. Size
  still ranks them. The weight cue is lost.
- With log 0072, two cues now need a Bold file: town rank and natural
  features. Atkinson Hyperlegible Next ships Bold under OFL-1.1
  (`docs/findings/atkinson-licence.md`). The macron patch
  (`tools/patch_atkinson_omacron.py`) works on any static weight.
- The "split road name" lead from log 0075 was wrong. "MARINE DRIVE" is
  one curved label (placement 2), not two word labels.

## What changed

Nothing in the style. The Bold file needs a download, which waits for
Josh.

## Confidence & gaps

Grade D. Five labels on this sheet. Other sheets may have more Bold names.
