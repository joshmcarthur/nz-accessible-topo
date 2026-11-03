# Sources

Grades per `method.md`. IDs are referenced from findings and log entries.

## LINZ / New Zealand

| ID | Grade | Source |
|---|---|---|
| S-LINZ-GUIDE | C | LINZ, *Topo50 Map Reading Guide* (PDF). https://www.linz.govt.nz/sites/default/files/topo50-map-guide_0.pdf |
| S-LINZ-DD | C | LINZ NZ Topo Data Dictionary. https://docs.topo.linz.govt.nz/data-dictionary/ |
| S-LINZ-DD-CONTOUR | C | LINZ Data Dictionary, object class `contour`. https://docs.topo.linz.govt.nz/data-dictionary/tdd-class-contour.html |
| S-MCDONALD-2020 | D | McDonald, P. (2020) *One Step at a Time* — context paper for petition to redesign Topo50 track symbols. https://petemcdonald.co/onestep.pdf (see also *Track Symbols on 1:50,000 Printed Topographic Maps*, 2019, https://petemcdonald.co/TrkSym.pdf — not yet read in full) |
| S-LINZ-BASEMAPS-STYLING | C | LINZ Basemaps, *How to Style our Vector Tiles*. https://basemaps.linz.govt.nz/docs/user-guide/working-with-vector-tiles/styling/ |
| S-LINZ-BASEMAPS-USAGE | C | LINZ Basemaps, *How to Use our Vector Tiles*. https://basemaps.linz.govt.nz/docs/user-guide/working-with-vector-tiles/usage/ |
| S-LINZ-RASTER-STYLE | C | `linz/basemaps-config` `config/style/topo-raster-gridded.json`: Topo50 raster tiles (WebP, grid baked in) + client hillshade at 315°. https://github.com/linz/basemaps-config |
| S-LINZ-TOPO-QGIS | C | `linz/topographic-qgis` @ c0edcfc (MIT): the Topo50 QGIS project, 43 layer QMLs, spot-colour palette, Nimbus Sans LINZ fonts (AGPL-3.0 with exemption). https://github.com/linz/topographic-qgis |
| S-LINZ-TOPO-SYSTEM | C | `linz/topographic-system` @ 3b6ec60 (2026-10-15, MIT): containerised QGIS map production (`packages/map` `prepare` / `export`). The map package release v0.9.0 reads private S3 only. https://github.com/linz/topographic-system |
| S-LINZ-BASEMAPS-CONFIG | C | `linz/basemaps-config` (MIT), `config/style/topographic-v2.json`. https://github.com/linz/basemaps-config |

## Colour science & simulation

| ID | Grade | Source |
|---|---|---|
| S-MACHADO-2009 | B | Machado, G.M., Oliveira, M.M., Fernandes, L.A.F. (2009) A physiologically-based model for simulation of color vision deficiency. *IEEE TVCG* 15(6):1291–1298. |
| S-SHARMA-2005 | C | Sharma, G., Wu, W., Dalal, E.N. (2005) The CIEDE2000 color-difference formula: implementation notes, supplementary test data, and mathematical observations. *Color Research & Application* 30(1). |
| S-JENNY-KELSO-2007 | B/C | Jenny, B. & Kelso, N.V. (2007) Color design for the color vision impaired. *Cartographic Perspectives* 58:61–67. https://doi.org/10.14714/CP58.270 ; also *Designing maps for the colour-vision impaired*, SoC Bulletin 41:9–12. Tool: Color Oracle (colororacle.org). |
| S-SCHNECK-2014 | B | Schneck, M.E., Haegerstrom-Portnoy, G., Lott, L.A., Brabyn, J.A. (2014) colour vision in older adults (n=865, age 58–102), *Optometry and Vision Science*. Read via ScienceDaily (2014-02-20) and News-Medical summaries — **primary paper not yet read; verify exact title/DOI**. |
| S-BARBUR-REVIEW | B | Review on S-cone pathways and ageing (PMC5330185), citing Verriest et al. and Knoblauch et al. on tritan-like age losses and their similarity to reduced illuminance. https://pmc.ncbi.nlm.nih.gov/articles/PMC5330185 |
| S-WUERGER-2013 | B | Wuerger, S. (2013) Colour constancy across the life span: evidence for compensatory mechanisms. *PLOS ONE* 8(5):e63921. (n=185, ages 18–75) |

## Typography, dyslexia, low vision

| ID | Grade | Source |
|---|---|---|
| S-RELLO-2013 | B | Rello, L. & Baeza-Yates, R. (2013) Good fonts for dyslexia. *ASSETS '13*. https://doi.org/10.1145/2513383.2513447 |
| S-RELLO-2016 | B | Rello, L. & Baeza-Yates, R. (2016) The effect of font type on screen readability by people with dyslexia. *ACM TACCESS*. https://doi.org/10.1145/2897736 |
| S-KUSTER-2018 | B | Kuster, S.M. et al. (2018) Dyslexie font does not benefit reading in children with or without dyslexia. *Annals of Dyslexia* 68(1):25–42. https://doi.org/10.1007/s11881-017-0154-6 |
| S-WERY-2017 | B | Wery, J.J. & Diliberto, J.A. (2017) The effect of a specialized dyslexia font, OpenDyslexic, on reading rate and accuracy. *Annals of Dyslexia*. (via IDA summary) |
| S-ZORZI-2012 | B | Zorzi, M. et al. (2012) Extra-large letter spacing improves reading in dyslexia. *PNAS* 109(28):11455–9. https://doi.org/10.1073/pnas.1205566109 |
| S-SPACING-2018 | B | (2018) Influence of increased letter spacing and font type on the reading ability of dyslexic children. *Annals of Dyslexia* (Oct 2018), PMID 30094714. Authors to be recorded. |
| S-ATKINSON | C/D | Braille Institute / Applied Design, Atkinson Hyperlegible (2019). https://github.com/googlefonts/atkinson-hyperlegible |
| S-ATKINSON-NEXT | C | Braille Institute press release (2025-02-10): Atkinson Hyperlegible Next — 7 weights, 150+ languages. |

## Cartographic typography guidance

| ID | Grade | Source |
|---|---|---|
| S-AXIS-LABELING | C | Axis Maps, *Labeling and text hierarchy in cartography*. https://www.axismaps.com/guide/labeling |
| S-COLORADO-TYPO | C | *Making Maps* (Colorado pressbooks), ch. Typography. https://colorado.pressbooks.pub/makingmaps/chapter/typography/ |
| S-ESRI-MINSIZE | C | Esri, *Guidelines for minimum size for text and symbols on maps*. |
| S-MN-MAPGUIDE | C | Minnesota IT Services, *Accessibility – Map Design Guide*. |
| S-USGS-SPECS | C | USGS, US Topo / OnDemand Topo cartographic specifications. https://www.usgs.gov/ngp-standards-and-specifications |

## Place names

| ID | Grade | Source |
|---|---|---|
| S-NZGB-2019 | C | NZGB decision, June 2019: 824 Māori place names official, ~300 with macrons added (RNZ, 2019-06-25). |
| S-LINZ-NZGB-AUCK | C | LINZ news: 541 Māori place names in Auckland made official, 194 macrons added. https://www.linz.govt.nz/node/11612 |

## Terrain depiction

| ID | Grade | Source |
|---|---|---|
| S-BILAND-2017 | B | Biland, J. & Çöltekin, A. (2017) An empirical assessment of the impact of the light direction on the relief inversion effect in shaded relief maps: NNW is better than NW. *CaGIS* 44(4):358–372. https://doi.org/10.1080/15230406.2016.1185647 |
| S-COLTEKIN-2018 | B | Çöltekin, A., Rautenbach, V., Coetzee, S., Mokwena, T. (2018) Landform perception accuracy in shaded relief maps: a replication study confirms that NNW lighting is better than NW… *ISPRS Archives* XLII-4:101–106. |
| S-COLTEKIN-2019 | B | Çöltekin, A. & Biland, J. (2019) Comparing the terrain reversal effect in satellite images and in shaded relief maps. *Int. J. Digital Earth* 12(4). https://doi.org/10.1080/17538947.2018.1447030 |
| S-COLTEKIN-2023 | B– | Çöltekin, A. et al. (2023) What moderates the terrain reversal effect in shaded relief maps? *Abstr. Int. Cartogr. Assoc.* 6:40. |
| S-MULTIDIR-2025 | B– | (2025) Multidirectional sky model vs relief inversion — user study. *Abstr. Int. Cartogr. Assoc.* 10:92. Authors to be recorded. |

## Standards

| ID | Grade | Source |
|---|---|---|
| S-NZ-WAS-1.2 | C | NZ Government Web Accessibility Standard 1.2. https://digital.govt.nz/web-accessibility-standard/ |
| S-NZ-WAS-DRAFT | C | Web Accessibility Standard 1.2 — Draft (complex visual maps modified requirement). digital.govt.nz |
| S-W3C-1411 | C | W3C, Understanding SC 1.4.11 Non-text Contrast. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast |

## Field use

| ID | Grade | Source |
|---|---|---|
| S-FORUM-REDLIGHT | D | Practitioner reports: bushcraftuk.com (2011); paddling.com forum (military "red-brown" note); trawlerforum.com (magenta on air charts). Anecdotal; mechanism is basic reflectance physics. |
| S-HARVARD-MONO | C | Harvard Library, *Styling Maps for Academic Publishing in QGIS* (greyscale legibility). |

## Rendering platform

| ID | Grade | Source |
|---|---|---|
| S-MAPLIBRE-SPEC | C | MapLibre Style Spec — hillshade layer properties (default `hillshade-illumination-direction` 335). https://maplibre.org/maplibre-style-spec/ |
| S-MAPLIBRE-2320 | C | MapLibre Style Spec v23.2.0 release notes: hillshade `multidirectional` method with array-valued illumination. Example: https://maplibre.org/maplibre-gl-js/docs/examples/add-a-multidirectional-hillshade-layer/ |

## Font licensing

| ID | Grade | Source |
|---|---|---|
| S-OFL-ATKINSON-NEXT | C | `OFL.txt`, googlefonts/atkinson-hyperlegible-next @ 7925f50 (read directly) |
| S-DEBIAN-ATKINSON | D | debian-fonts mailing list (2021): Braille Institute download licence is a modified OFL. https://lists.debian.org/debian-fonts/2021/02/msg00050.html |
| S-SCANCODE-ATKINSON | C | ScanCode LicenseDB, "Atkinson Hyperlegible Font License" (Braille Institute PDF 2020-11-04). https://scancode-licensedb.aboutcode.org/atkinson-hyperlegible-font |
| S-NEXT-RFN | D | Secondary listing of "License for The Atkinson Hyperlegible Next Font" naming RFNs "ATKINSON", "HYPERLEGIBLE". https://wiki.mobiusconsortium.org/wiki/Special:Version/License/The_Atkinson_Hyperlegible_Next_Font |

## Our own measurements

Reproducible from tools in this repo, graded D until validated with users.
`tools/extract_graph.py` maps references in findings to these IDs (W1–W8 →
web audit, P1–P9 → print audit, etc.).

| ID | Grade | Source |
|---|---|---|
| S-OUR-AUDIT-WEB | D | `tools/palette_audit.py` on LINZ `topographic-v2` (logs 0004, 0013, 0014) |
| S-OUR-AUDIT-PRINT | D | Topo50 legend colour/dash sampling + audit (log 0019) |
| S-OUR-FONTCHECK | D | `tools/font_check.py` glyph coverage and x-height (log 0006) |
| S-OUR-SHAPING-TEST | D | Shaped vs unshaped rendering of Atkinson Next (log 0018) |
| S-OUR-PALETTE-V0 | D | Palette experiment v0 (log 0009) |
| S-OUR-PATCH | D | `tools/patch_atkinson_omacron.py` — macron placement rule verified against existing glyphs (log 0018) |
| S-OUR-QGIS-ANALYSIS | D | `tools/analyse_qgis_project.py` over topographic-qgis + carto_text sample (log 0023) |
| S-OUR-REAL-RENDER | D | Simulations over LINZ's real Topo50 render (log 0019) |
