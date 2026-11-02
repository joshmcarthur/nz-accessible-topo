# Questions

## Does the light intermediate contour still meet R-04 against print highway orange?

**Closed 2026-11-02.** Judge R-04 against `#D5B43C`. Keep `#C4814B`. See the decision "R-04, R-05, and R-06 stay settled in the style loop".


R-04 sets intermediate contours to `#C4814B` so 20 m lines stay recessive (log 0020, revised from `#A8703C`). The pair audit against print highway `#EA6300` is ΔE 11.5 normal, 8.3 protan, 7.5 deutan, 10.2 tritan. The met-when is ΔE ≥10 under every simulated dichromacy.

Against this QGIS project's road ink (`#D5B43C`) the same intermediate passes that ΔE bar. The project does not paint highways in the print orange.

On paper, intermediate vs white is 3.19:1 in greyscale and 1.74:1 under the red-light model. Index vs white is 6.53:1 and 3.45:1.

The accessible render uses `#C4814B` anyway. A darker intermediate would undo log 0020. Leave the value until a steep sheet (OQ-09) shows whether the light line disappears.


## Why do along-line water names render as black question marks?

**Closed as a style question 2026-11-02.** It does not reopen R-05 or R-06. It stays a render defect: load the `.ttf`, and if the marks remain, change `StretchWordSpacingToFit` on the estuary square.


The accessible BX24 render (log 0026) draws large black question marks across the estuary and the bay. They sit on labels whose placement is AL and whose charplace is StretchWordSpacingToFit. Examples: Pegasus Bay, and Estuary of the Heathcote and Avon Rivers / Ihutai. Those rows are process_blue and Italic in the data. Offset water names (Avon River, placement OL) still read as blue text.

The project file has no italic map labels. Fontconfig lists NZAT Legible Test. The PDF has no embedded fonts; QGIS rasterised the page. Fontconfig also reported no writable cache directory because the container user has no home.

Do not treat B-25 or B-11 as done until those marks are gone.

The accessible patch no longer changes that mode. See the decision "Along-line labels keep the official placement".


## Why does a sliding carto label land on a fixed curved label?

With a hint line anchor, QGIS moves `Godley Head` onto `Gun emplacements` on BX24, although water below `Godley` is free. `QgsLabelingResults` boxes are the right size. Rule priority 5 and label engine version 2 do not change it. A guess: under `AllowOverlapIfRequired`, PAL keeps the flexible label and then draws the dropped fixed label over it. Answer this before a hint anchor is tried again.


## Which painted road pairs still fail R-04?

**Open 2026-11-03.** Log 0048. Intermediate versus PMS151 `#FF7F00` fails protan ΔE 9.1 and tritan ΔE 7.6. Index versus highway `#E31A1C` fails protan ΔE 0.9. Intermediate versus that highway fails deutan ΔE 8.8. Pipeline is not on Map5View.

The closed question that judged R-04 against gold `#D5B43C` was a measurement error. Contour fills stay. If a same-hue orange cannot meet ΔE ≥10 against `#C4814B`, leave R-04 open and stop.

Log 0049: a PMS151 lightness sweep meets the bar only as pale orange (`#FFA83B`–`#FFB94C`) or as dark maroon. Highway hue has no L* that meets both contour browns. R-04 stays open. Road and highway fills stay unowned.

