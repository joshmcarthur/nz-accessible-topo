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
