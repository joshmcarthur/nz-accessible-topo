# 0083 — Streams separate from index contours in greyscale

**Date:** 2026-11-05

## Question

Do the darker inks from logs 0063 and 0071 hold up in the greyscale and
red-light simulations on a real cell?

## What we did

Ran `tools/simulate_image.py` on a 400 px crop of `1564000-5162000`. Read
the stream pairs in the Topo50 pair audit. Scored darker streams with the
`nzat.colour` models against the index contour and the black track and
road-casing inks. Checked that the shields, golf, and opencast symbols on
`nztopo50_carto_symbol` still drew after the log 0082 blend change. They
do.

## What we found

In the greyscale panel, a stream and an index contour were the same
mid-grey line. Index vs stream was 1.28:1 grey. In red light they already
differ (6.41:1). On a photocopy only width told them apart (0.25 mm and
0.35 mm).

| Stream | vs index grey | vs `#232323` casing grey | vs paper grey |
|---|---|---|---|
| `#0064BD` (log 0063) | 1.28 | — | 5.90 |
| `#004C99` | 1.83 | 1.87 | 8.42 |
| `#00408A` | 2.17 | 1.57 | 10.00 |

Darker streams move toward the black inks. `#004C99` keeps at least
1.8:1 on both sides. Tracks are also dashed, so shape helps there.

## What changed

- `reference_inks.stream` `#004C99`. Tests and `docs/style-topo50.md`.
  B-35.

## Confidence & gaps

Grade C for the contrast numbers, D for the look. Index vs stream is still
under 3:1 in grey. Width and the blue hue carry the rest. Streams still read
blue in colour on the steep `1580000-5154000` cell.
