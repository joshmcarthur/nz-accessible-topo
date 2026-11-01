# Open questions

| ID | Question | Why it matters | Next step |
|---|---|---|---|
| OQ-01 | How much change will Topo50-trained users (SAR, NZDF, trampers) tolerate? | Familiarity is a safety feature too | Include them in R-16 testing |
| OQ-02 | What are the exact print Topo50 colours, line weights and typefaces? | Our audit covers the web style only | Read a physical legend / print-ready TIFF legend |
| OQ-03 | What ΔE is enough for thin lines and small glyphs? | Our ✅/❌ thresholds are assumptions | Literature search on small-field colour discrimination; user test |
| OQ-04 | How do 0.4–1.5 px lines render across DPRs and print resolutions? | Contour visibility depends on it | Render test tiles at 1×/2×/3× and print at 1:50k |
| OQ-05 | Is there CVD research specific to topographic map tasks? | Jenny & Kelso is a review | Deeper search (Cartographic Journal, CaGIS, ICA) |
| OQ-06 | Do dyslexia letter-spacing and italic findings transfer to short map labels in clutter? | R-08 and R-05 assume so | A/B test |
| OQ-07 | Does NNW + multidirectional shading work on both Alpine and Canterbury-flat terrain? | Studies used non-NZ terrain | Generate from LINZ 8 m DEM / LiDAR; test |
| OQ-08 | What actually disappears under common headtorches' red modes? | Only anecdote + model so far | Print swatches; photograph under 3–4 headtorches |
| OQ-09 | Do darker contours swamp tracks and labels on steep sheets? | v0 measured contrast, not clutter | Render Arthur's Pass / Fiordland samples |
| OQ-10 | Is Ō/ō missing from Atkinson Hyperlegible Next already reported upstream? | Determines whether R-06 can adopt it | Check googlefonts/atkinson-hyperlegible-next issues; file one if not |
| OQ-11 | Which licence for this project's styles and docs? | Must be compatible with LINZ MIT style + CC BY 4.0 data attribution | Maintainer decision |
| OQ-12 | Does the Shortbread vector schema carry the attributes we need (e.g. contour `definition`, track status)? | R-04 and R-11 depend on attributes | Inspect topographic-v2 tiles / MBTiles export |
