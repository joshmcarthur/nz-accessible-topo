# Method

## How a recommendation is made

```
source(s)  ──►  finding (F-xx)  ──►  recommendation (R-xx)  ──►  style change
   │                 │                      │
 graded A–D     states what we         states what to do,
               believe and why        which findings it rests
                                       on, and how to test it
```

Every recommendation must cite at least one finding; every finding must cite at
least one source. If a recommendation rests only on grade C/D evidence it is
labelled **provisional**.

## When a recommendation is met

A recommendation is met only when both of these are true:

1. Its "Met when" threshold holds on the painted inks (pair audit, gates).
2. A stock-versus-accessible review of the full 4 km grid finds no regression that the change causes.

The grid is one stock face and one accessible face at 300 dpi, drawn with
`tools/render_square.py --extent`, then cut into 27 cells by
`tools/crop_grid.py` (output in `render/bx24-4km/`, not committed). Compare
each cell pair. A regression is anything the stock cell shows more clearly:
a name that collides or moves away from its feature, a class cue that is
lost, a line that is harder to find on the fill under it, or a symbol that
now looks like a different legend symbol.

A threshold checks one pair at a time. Regressions come from dense data and
from neighbouring classes, which a single test square does not show. The
review is our own judgement, so it is grade D until user testing (R-16).

## Evidence grades

| Grade | Meaning | Example |
|---|---|---|
| **A** | Peer-reviewed empirical study that has been replicated or is a large sample | Biland & Çöltekin 2017 + Çöltekin et al. 2018 replication (relief lighting) |
| **B** | Single peer-reviewed empirical study | Zorzi et al. 2012 (letter spacing) |
| **C** | Formal standard, official specification, or established professional guidance | WCAG 2.2; LINZ Topo50 Map Reading Guide |
| **D** | Practitioner guidance, user reports, anecdote, or our own unvalidated measurement | Forum reports of red symbols vanishing under red light |

Our own measurements (e.g. the palette audit tool) are reproducible but are
models of perception, not perception itself — they're graded **D** until
validated with real users.

## Research log convention

Each commit that adds research adds one file to `docs/research-log/` named
`NNNN-short-title.md`, containing:

- **Question** — what we set out to learn
- **What we did** — searches, reading, measurement
- **What we found** — with source IDs
- **What changed** — which docs were added/edited
- **Confidence & gaps**
