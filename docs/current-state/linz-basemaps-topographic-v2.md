# Current state: LINZ Basemaps `topographic-v2` (web)

The web counterpart to Topo50. Vector tiles in the **Shortbread** schema
(S-LINZ-BASEMAPS-STYLING), styled with a MapLibre GL style published in
`linz/basemaps-config` (MIT licence, Crown copyright LINZ). Tiles are
available in NZTM2000 (2193) and Web Mercator (3857), max zoom 15, and as
MBTiles exports (S-LINZ-BASEMAPS-USAGE).

Audited revision: `linz/basemaps-config@581b44a` (2026-10-28).

## Inventory

- 287 layers.
- Typefaces: Open Sans (Regular, Italic, Bold, Bold Italic, Medium, Light
  Italic) and Roboto (Light, Bold, Bold Italic, Black, Black Italic, Italic).
- **33 of 63** literal-coloured label layers use an italic face (corrected in log 0014; first count included icon-only layers).
- Water: fill `#B8DCF2`, lines and labels `#008CCC`.
- Contours: `rgba(206,103,6,0.75)` at **0.4–0.6 px**; index contours get a
  black 75% halo line underneath. Labels `#C16809` on `#F3F3F2` halo.
- Highways: fill `#F0A452` with grey casing — same hue family as contours.
- Tracks: foot/cycle/vehicle all `rgba(78,78,78,0.8)` (dark grey), differing
  by width/dash. **Closed** tracks differ from open ones only by a 40%-opacity
  red shadow (`rgba(205,53,53,0.4)`) instead of a light-grey one.
- Vegetation: scrub `#C7E4B7`, scattered scrub `#CCDEC3`.
- Peaks: dark green labels `#295A37`.

## Headline audit results

Full table: [audit-linz-topographic-v2.md](audit-linz-topographic-v2.md).

| # | Observation | Evidence |
|---|---|---|
| W1 | 26 of 63 label layers fall below WCAG 4.5:1 text contrast (corrected in log 0014 — first count of 28/68 wrongly included two icon-only layers with an empty `text-field`). All water labels (`#008CCC`) sit at 3.25–3.73:1. Contour labels 3.60:1. | audit |
| W2 | Two of those are highway shield text drawn on an icon — false positives. **24 are real.** | manual check |
| W3 | Intermediate contour lines are 2.66:1 (index contours are *paler*: 1.71–2.27:1, see `tile-attributes.md`) against white — below the 3:1 WCAG 1.4.11 guidance for graphical objects — and only 0.4–0.6 px wide. | audit |
| W4 | Scrub vs scattered scrub: ΔE 5.6 for normal vision and **<5 for all three dichromacies**; ~1.0 luminance ratio. Effectively indistinguishable for many readers. | audit |
| W5 | Contour vs state highway: ΔE ≈6 for everyone; nearly identical luminance. Relies on width/casing. | audit |
| W6 | Contour vs pipeline collapses for tritanopia (ΔE 3.8). | audit |
| W7 | Closed vs open track: colour difference survives CVD simulation, but it is carried by a faint 40% shadow, fails greyscale (1.7:1) and vanishes under red light (1.1:1). | audit |
| W8 | Under a red-light model, contours drop to 1.39:1 against paper. | audit (crude model) |
