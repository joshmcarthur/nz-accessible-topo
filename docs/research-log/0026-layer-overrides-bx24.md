# 0026 — Layer overrides on BX24, judged one layer at a time

**Date:** 2026-11-01

## Question
The stock BX24 PNG is the full print page. Which map layers do the research changes belong on, and what does a re-render show?

## What we did
Read the deployed `nztopo50.qgs` layer by layer. Left the print layout alone (legend text, sheet index, scale, title). Wrote `tools/override_topo50_project.py` and rendered BX24 again at 150 dpi.

The accessible project is a local `.qgs`. `map prepare` deploys it into a temp directory. That directory must stay on the mounted work dir (`deploy-tmp`). A temp dir inside the container disappears before `map export`.

The label face is `NZAT Legible Test`, built at render time by `tools/patch_atkinson_omacron.py` from Atkinson Hyperlegible Next Regular. Fontconfig sees that family in the container. The print layout still asks for Nimbus Sans LINZ.

## What we found

Map layers, and the change made on each:

- `nztopo50_carto_text`. Family, style, and size are fields. The override replaces those fields with expressions. Upright face. Size at least 7 pt. In the project file, map-label italics are 0. The layout still has one italic Nimbus style.
- `relief_point`. Spot-height labels may stay at 6 pt.
- `contour`. One line symbol. Index is `round(elevation) % 100 = 0`, ink `#8A4F1C`, width 0.28 mm. Other contours are `#C4814B`, width 0.12 mm. The `definition` column is null on every national row, so indefinite contours are not dashed.
- `track_line map`. Categories are cycle, foot, and vehicle. Closed is `status = 'closed'` (153 rows nationally, 1 on BX24). Closed foot tracks get a heavier line and cross-bars.
- `water_point`. The category field in the project was `feature_type`. The column is `type`, so the spring symbol never matched. Hot and cold are `temperature_indicator` (85 hot, 70 cold nationally; 1 spring on BX24). Hot is a black ×. Cold is a `#005C8F` circle.
- `vegetation map`. Native and scrub were the same green at two alphas. Native fill is `#E1EAC3`. Scrub fill is `#A3CC90` plus a line hatch. Scattered scrub keeps its dots. Alpha stays below 255 because this layer draws above the contours.

This project's road ink is `#D5B43C`. The printed highway is `#EA6300`. Those are different inks.

Pair audit (`tools/pairs-topo50-accessible.json`):

- Index `#8A4F1C` vs paper is 6.53:1. Intermediate `#C4814B` vs paper is 3.19:1. Both pass the greyscale 3:1 floor.
- Index vs intermediate is ΔE 20.
- Intermediate vs print highway `#EA6300` is ΔE 8.3 protan and 7.5 deutan. R-04 asks for ΔE ≥10 under every simulated dichromacy. The light intermediate from log 0020 misses that bar. It is still the value that was rendered.
- Native forest vs scrub is grey contrast 1.45:1. That is why scrub also has a hatch (R-10).

The re-render shows brown contours on the Port Hills, and place names such as Christchurch and Ferrymead in the new face. The estuary and the bay are covered by large black question marks. Those marks sit where along-line labels use `StretchWordSpacingToFit` (`Pegasus Bay`, `Estuary of the Heathcote and Avon Rivers / Ihutai`). Offset water names such as Avon River still read as blue text. The question marks are black, not the blue water ink. Cause is not isolated. B-25 and B-11 are not met.

Checksums (sha256) of the full accessible export:

- PDF `35988bc9a74d23b3069503ac1028d4b6061e7e3a5146f2beff11365bd9641780` (12 MB)
- PNG `575be3f31103a0f3091661fbe7893a442fd419fbe815e886c7fcf63d7230f3ea` (4500×6300, 17 MB)

The PDF embeds no fonts. QGIS wrote the page as a picture. The review PNG is `docs/visuals/09-bx24-accessible.png`.

## What changed
- `tools/override_topo50_project.py` edits the four map layers and the label styles.
- `tools/render_sheet.sh` can keep a local project on a mounted temp dir and can point Fontconfig at the patched face.
- `tools/pairs-topo50-accessible.json` is the pair list for these inks. The stock pair file is unchanged.
- B-25, B-11, and B-24 stay open.

## Confidence & gaps
- One sheet. BX24 is flat. A steep sheet is still OQ-09.
- The question marks block any claim that labels are upright and readable.
- Closed-track cross-bars and the spring glyphs are in the project. BX24 has one of each. They were not checked by eye on this page.
- Fontconfig reported no writable cache directory. `fc-list` still showed `NZAT Legible Test`.
