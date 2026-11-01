# Questions

## Does the light intermediate contour still meet R-04 against print highway orange?

R-04 sets intermediate contours to `#C4814B` so 20 m lines stay recessive (log 0020, revised from `#A8703C`). The pair audit against print highway `#EA6300` is ΔE 11.5 normal, 8.3 protan, 7.5 deutan, 10.2 tritan. The met-when is ΔE ≥10 under every simulated dichromacy.

Against this QGIS project's road ink (`#D5B43C`) the same intermediate passes that ΔE bar. The project does not paint highways in the print orange.

On paper, intermediate vs white is 3.19:1 in greyscale and 1.74:1 under the red-light model. Index vs white is 6.53:1 and 3.45:1.

The accessible render uses `#C4814B` anyway. A darker intermediate would undo log 0020. Leave the value until a steep sheet (OQ-09) shows whether the light line disappears.
