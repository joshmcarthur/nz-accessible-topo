# 0036 — Springs, native forest, and no red-only meaning

**Date:** 2026-11-02

## Question

Do hot and cold springs differ in glyph, and does native forest differ from scrub by a lightness step or a texture?

## What we did

The numbers did not change. `springs.hot` is `cross2` in `#141414`. `springs.cold` is `circle` in `#005C8F`. `vegetation.native.colour` is `#E1EAC3`. Those values already live in `tools/style-topo50.json`.

The vector build reads the native fill. `Vegetation-Native` is `rgba(225, 234, 195, 1)`. The zoom stops are gone. The vector build reads the spring inks. `Water-Spring-Hot` text is `rgba(20, 20, 20, 1)`. `Water-Spring-Cold` icon and text are `rgba(0, 92, 143, 1)`. The icons stay `spring_hot_pnt` and `spring_cold_pnt`. No native hatch was added on the vector.

The QGIS apply step still paints those same values. Scrub keeps the hatch from R-10. Scattered scrub keeps the stock dots. Contour labels and spot heights stay upright.

The four squares were drawn again at 600 dpi. The cold-spring square shows a blue circle. The darker green has a hatch. The paler green has no hatch. The estuary word is `Estuary of`. The square has no black question marks.

## What we found

Native forest versus scrub is grey 1.45:1. The raster hatch carries that pair. Hot spring versus cold spring is grey 2.57:1. The glyphs differ. Hot spring versus paper is 18.42:1 under red light. The hot ink is `#141414`, not red-orange.

Intermediate contour versus the project road `#D5B43C` still has a worst dichromacy ΔE of 12.3. Intermediate contour versus `#EA6300` still fails. The style does not paint `#EA6300`.

## What changed

- `tools/build_style.py` reads the native fill and the spring inks from the style file.
- The four square pictures in `docs/visuals/squares`.
- The site condition images for those squares.

## Confidence & gaps

R-17 is met for this list. The next step is R-01.
