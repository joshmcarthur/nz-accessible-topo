# Style loop prompt

Paste the block below into a fresh agent session. One paste does one step, then stops. Paste the same block again for the next step. Do not start this loop from inside a running step.

The loop is finished only when the status file says `loop finished: yes`.

```text
You are working in the nz-accessible-topo repo. Do one step of the style loop, then stop. Do not start the next step.

Talk to Josh in short sentences. One fact per sentence. Use the same word for the same thing.

## End state

The loop is finished only when all of these are true.

1. tools/style-topo50.json is the only place that sets colour, type size, font family, and symbol rules for the accessible Topo50 style. The file has no sheet code. The same file can style any NZ Topo50 sheet.
2. A QGIS apply step reads that file and writes a project the local LINZ map container can render.
3. A vector style build reads that same file and writes a MapLibre style. Colours, size floors, and symbol meaning match the raster style. Do not keep a second palette in tools/build_style.py.
4. The static site shows stock and accessible for each comparison square. Each of those images has the six conditions in site/src/data/conditions.json: normal, deutan, protan, tritan, grey, red. Produce the condition images with tools/build_site_assets.py. That tool uses the same models as tools/palette_audit.py. Do not draw impairment pictures by hand. Do not add a vision model.
5. docs/style-topo50.md says how to apply the file. It does not restate the research logs.

The pictures are outputs of the style. A style change is an edit to tools/style-topo50.json, then a render, then the site build.

## Read first

Read these before you edit anything. Do not work from memory of an earlier session.

- docs/plans/style-loop-status.md if it exists
- docs/recommendations.md, including each item's "Met when"
- BACKLOG.md
- the newest file in docs/research-log/
- tools/style-topo50.json if it exists
- git show refs/lore/topo50-qgis-render:plan.md
- git show refs/lore/topo50-qgis-render:decisions.md
- git show refs/lore/topo50-qgis-render:questions.md

Then do the first incomplete step below.

## Settled

Do not reopen these. Do not pick new values for them.

R-06. The accessible raster face is NZAT Legible Test, the patched Atkinson Hyperlegible Next. font_check on that TTF reports all ten macron vowels and the combining macron. The stock sheet keeps unmodified Nimbus Sans LINZ. The vector style keeps Open Sans until macron glyph PBFs exist. Pegasus Bay and the estuary name do not contain Ō or ō. A missing macron is not the cause of the question marks. Do not spend a step swapping the vector face.

R-05. Map labels in the accessible project are upright. The italic count on those styles is 0. Layout text stays Nimbus, including its italic. Do not spend a step removing italics again.

R-04. Keep index `#8A4F1C` and intermediate `#C4814B`. Judge a contour against the road ink the style paints. In this QGIS project that ink is `#D5B43C`, including the highway layers. Intermediate versus that gold is 3.19:1 on white. The worst dichromacy ΔE is 12.3. The written gate is ≥3:1 and ΔE ≥10. `#EA6300` is the print-legend orange. This project has no layer in that ink and no pipeline layer. Do not change the intermediate to clear `#EA6300`. Do not return to `#A8703C`. That older brown also fails against `#EA6300` (protan ΔE 7.2).

## Along-line question marks

This is a render defect. It does not reopen R-05 or R-06. The marks are black (0,0,0). They sit on labels whose placement is AL and whose charplace is StretchWordSpacingToFit. Offset water names, such as Avon River, render as blue letters. On the first render of square 1577000 E, 5178000 N, load the .ttf with QFontDatabase. If the marks remain, change that placement mode and render the square again. The sheet is not acceptable while those labels are question marks.

## Step A — Create the configuration

Do this only if tools/style-topo50.json does not exist.

Copy the current values from tools/override_topo50_project.py and the matching rules in docs/recommendations.md. Do not invent new colours or sizes. Carry the settled values above into the JSON as they are.

Point tools/override_topo50_project.py at the JSON. Leave the vector build for a later step if doing both in this step is not safe. Write docs/style-topo50.md. Write the next research log and add it to docs/research-log/README.md. Do not edit old logs. Update docs/plans/style-loop-status.md. Stop.

## Step B — One recommendation

Work the first id in this list that is not met for both the raster config and the vector style. R-06, R-05, and R-04 are settled above. Skip them. When the vector style is generated, copy their settled values. Do not pick new ones.

1. R-09 size floor.
2. R-07 label contrast and halo.
3. R-10 vegetation pattern.
4. R-11 closed tracks and hazards encoded in shape.
5. R-17 springs, forest versus scrub, and no meaning that exists only as red.
6. R-01 pair gates. Run the audit against the inks the style paints. If a pair fails, fix the config or leave the recommendation open. Do not fail a pair against `#EA6300` unless the style paints that ink.
7. R-08 letter-spacing. This one is provisional. One attempt. Leave it provisional if the evidence is still weak.
8. R-12 track-access symbol channel, if R-11 did not already cover it.
9. R-03 relief shading. Do this only if the backlog says the served raster tiles already bake relief. Otherwise write a skip and stop.
10. R-14 pair audit reads the shared config.
11. R-13 greyscale-safe and high-contrast variants. Do this only after R-01 passes for the main style.
12. R-15 the vector style stays derived from LINZ topographic-v2, and it reads the shared config.

Skip R-16, B-20, and B-21. Do not plan user testing. Do not contact anyone.

For that one recommendation:

- Change tools/style-topo50.json only for the values that recommendation owns.
- Regenerate the QGIS project and the vector style from that file.
- Render four 1 km squares. Draw the map face only. Use 600 dpi. 1000 m on the ground is 20 mm on the 1:50,000 sheet, which is 472 px. Render stock and accessible at the same extent and the same scale. Do not upscale the 150 dpi page. Do not export the whole sheet. Do not build a tile server.

Squares, named by the south-west NZTM corner:

- 1577000 E, 5178000 N — estuary water names
- 1577000 E, 5172000 N — Port Hills contours
- 1569000 E, 5165000 N — the cold spring
- 1584000 E, 5173000 N — the closed foot track

- Add those squares to site/src/data/comparisons.json with two variants: stock and accessible. Run python3 tools/build_site_assets.py so each variant gets normal, deutan, protan, tritan, grey, and red.
- If you edit docs/recommendations.md or docs/sources.md, run python3 tools/extract_graph.py.
- Run the pair audit. A recommendation is met only when its "Met when" text is true on the new pictures and the audit. If it fails, leave it open, name the failing pair, and stop. Do not lower the bar.
- Write the next research log. Add it to the log index. Do not edit old logs.
- Update the backlog status in one or two lines. Mark an item done only when its "Met when" is true.
- Update docs/plans/style-loop-status.md. Stop.

## Step C — Finish check

Do this only when every Step B id is met or has a written skip.

Check the end-state list. If one item is missing, do only that item, then stop. If the list is complete, set loop finished to yes in the status file and stop. Do not start tile serving.

## Hard rules

- Do not create a GitHub repo. Do not push. Do not commit unless Josh asks in this step.
- Do not modify the Nimbus font files. Do not copy them into the repo. Do not commit the patched Atkinson TTF.
- National GeoParquet stays outside this repo.
- Stop a render if free disk on /System/Volumes/Data would fall below 8 GB.
- The proof sheet is BX24. A steep sheet is later work.
- The vector style may keep Open Sans until macron glyph PBFs exist. Say that in docs/style-topo50.md. Do not claim the vector face matches the raster face until those glyphs exist. Colours and symbol meaning still match.
- Layout text on the QGIS sheet stays Nimbus, including italic. Change map layers only.
- The container image tag is map, built from linz/topographic-system at 3b6ec60. Do not rebuild it unless the render cannot start.
- The stock exporter writes the whole tiff-50 page and loads only .otf files. A square render is a separate script. Load .ttf with QFontDatabase. Set HOME=/tmp so fontconfig can write a cache.
- Datasources in the project are relative ./name.parquet. Cache files are hash-prefixed. Put the project copy and relative symlinks in one directory. Do not symlink the .qgs itself, or QGIS will look for data beside the real file.
- If the estuary square still shows black question marks after the .ttf is loaded, change StretchWordSpacingToFit and render that square again. Do not reopen R-05 or R-06 because of those marks.
- Do not change `#C4814B` to clear `#EA6300`. Judge R-04 against `#D5B43C`.
- If a choice is not in this prompt, the recommendations, or the lore decisions, stop. Write the choice in the status file. Do not guess.
- One recommendation per step. Do not refactor surrounding code.
- Extend tools/test_tools.py when you change a pure function. State in the status file what the test catches. If python3 tools/test_tools.py exits 139, run it again outside the sandbox.
- Do not use --no-verify.
- Before a plan that creates a file or adds a dependency, read ~/.dotfiles/agents/skills/thermo-nuclear-plan-review/SKILL.md and put the verdict on one line in the status file.
- Record a significant decision in lore refs/lore/topo50-qgis-render before you implement it. Follow ~/.claude/skills/edit-lore/SKILL.md. Do not push lore.

## Where things are

- Render work directory: ~/Projects/github.com/linz/topo50-bx24
- Stock project pin: topographic-qgis c0edcfc8c8b4321359cd9dbc2f66cd8d0e539a78
- STAC item: https://d1jzh93b1t1cv.cloudfront.net/qgis/nztopo50/commit_prefix=c/commit=c0edcfc8c8b4321359cd9dbc2f66cd8d0e539a78/nztopo50.json
- Cache: ~/Projects/github.com/linz/topo50-bx24/.cache/
- Accessible project from the last attempt: ~/Projects/github.com/linz/topo50-bx24/accessible/nztopo50.qgs
- Patched font: ~/Projects/github.com/linz/topo50-bx24/accessible/fonts/NZATLegibleTest-Regular.ttf
- Family name: NZAT Legible Test
- Sheet render wrapper: tools/render_sheet.sh
- Vector style today: styles/accessible-v0.json, built by tools/build_style.py from upstream/linz-topographic-v2.json
- Site comparisons: site/src/data/comparisons.json
- Conditions: site/src/data/conditions.json
- Comparison component: site/src/components/Compare.astro

## Status file

Write docs/plans/style-loop-status.md at the end of the step. Use these lines.

- date
- step
- recommendation (or "config")
- result: met, open, or skipped
- reason
- files changed
- next step
- loop finished: yes or no
- thermo-nuclear verdict, if this step created a file or added a dependency

Then stop. Do not paste this prompt again yourself.
```
