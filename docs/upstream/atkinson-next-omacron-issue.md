# Draft upstream issue: googlefonts/atkinson-hyperlegible-next

**Title:** Missing Ō / ō (U+014C / U+014D) — blocks te reo Māori

**Body:**

Atkinson Hyperlegible Next 2.001 (repo HEAD `7925f50`, 2025-02-21) includes
Ā ā Ē ē Ī ī Ū ū but not **Ō ō** (`Omacron`, `omacron`). The glyphs are absent
from both `sources/AtkinsonHyperlegibleNext.glyphs` and
`sources/AtkinsonHyperlegibleNext-Italic.glyphs`, and from every built TTF.
The repo's own `sources/CustomFilter_GF_Latin_All.plist` lists `omacronacute`
and `omacrongrave`, which suggests `omacron` was intended.

Impact: te reo Māori is an official language of Aotearoa New Zealand, and ō
is common in official place names (Taupō, Ōtautahi, Ōamaru, Ōpōtiki,
Ōhakune). The font is otherwise an excellent fit for public-sector and
mapping use in NZ. Renderers without OpenType mark positioning (e.g.
MapLibre GL glyph PBFs) cannot fall back to `o` + U+0304.

Suggested fix: add `Omacron` / `omacron` as composites of `O`/`o` + `macroncomb`
(the existing `Amacron`, `Emacron`, etc. presumably follow the same pattern),
in all masters and the italic.

Repro:
```python
from fontTools.ttLib import TTFont
c = TTFont("fonts/ttf/AtkinsonHyperlegibleNext-Regular.ttf").getBestCmap()
print([hex(u) for u in (0x14C, 0x14D) if u not in c])  # ['0x14c', '0x14d']
```

> Status: **draft, not filed.** The maintainer should file it; we could not
> check the issue tracker directly (GitHub API rate-limited from our
> environment, and web search found no existing report).
