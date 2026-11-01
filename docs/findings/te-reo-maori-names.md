# Findings: te reo Māori place names

## F-12 — Macrons are mandatory on official names, and the set is growing
Ngā Pou Taunaha o Aotearoa (NZ Geographic Board) made 824 Māori place names
official in 2019, adding macrons to about 300 (e.g. Taupō). Further batches
since (e.g. 541 Auckland names, 194 gaining macrons). Once official, names
must be used on maps, signs, websites and databases.
**Sources:** S-NZGB-2019 (C), S-LINZ-NZGB-AUCK (C).
**Grade:** C (statutory).
**Map implication:** any typeface we choose must render all ten macron
vowels in every weight/style used, in both the print toolchain and the
MapLibre glyph PBFs. This is a hard gate, not a preference.

## F-13 — Long names stress the label system
Official names include very long single words (the 85-character hill name
in Hawke's Bay) and hyphenated compounds (e.g. Te Horohoroinga-o-ngā-ringa-o-
Kahumatamomoe). Increased letter-spacing (F-07) makes these longer still.
**Sources:** S-NZGB-2019, LINZ NZGB notices (C).
**Implication:** letter-spacing needs a ceiling, and line-breaking at
hyphens/spaces should be allowed (`text-max-width`).
