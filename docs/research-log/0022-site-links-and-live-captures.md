# 0022 — Cross-links, link checking, live-capture ingestion, and a fix to 0021

**Date:** 2026-11-01

## Correction to log 0021
Log 0021 said the legend crops had moved into the comparisons manifest. They
hadn't: that edit was chained (`&&`) behind an `rm` that failed on shell
brace expansion, so it never ran — and the crop PNGs were deleted afterwards.
The committed manifest pointed at missing files and CI would have failed.
Fixed here (manifest crops + crop support in `build_site_assets.py`).
**Process change:** verify from a clean clone before committing (below).

## What we did
- **Cross-linking.** `site/src/lib/linkify.ts` links plain-text IDs in log
  entries, findings and recommendations: F-xx, R-xx, S-… (only IDs that
  exist), and "log 0019" / "logs 0004, 0009 and 0014". It edits text only —
  never tags, existing links, `<pre>` or headings. (0021's note about "repo
  links" was wrong: log entries contain no markdown links; IDs were the gap.)
- **S3 gate** in `tools/check_site.py`: every internal link and `#anchor`
  resolves. Verified by planting a broken link and a missing anchor.
- **Live captures → site.** `compare.mjs` now captures normal vision only by
  default; `build_site_assets.py` discovers `docs/visuals/real/*/none.png`,
  splits each into LINZ/accessible halves and adds them to the comparison page
  (simulated with the audit models). Tested with a synthetic two-colour
  capture to confirm the split is exact, then removed.
