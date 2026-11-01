# Findings: accessibility standards

## F-19 — NZ government web must meet WCAG 2.2 AA, with a maps exception
The NZ Government Web Accessibility Standard 1.2 (effective 17 March 2025)
requires WCAG 2.2 Level AA, with listed exceptions including **complex
visual maps**; the draft modified requirement was that data presented in
complex visual maps be published in open, machine-readable formats via
data.govt.nz. A Digital Accessibility Standard is being developed to extend
beyond websites.
**Sources:** S-NZ-WAS-1.2 (C), S-NZ-WAS-DRAFT (C).
**Implication:** a topo map is likely "exempt", but the exemption is about
*equivalent data*, not permission to be hard to read. LINZ already publishes
the data openly, so our job is purely legibility. We should still adopt
WCAG ratios as *design targets* because they encode real low-vision limits.

## F-20 — WCAG ratios we will use as targets
- Text: 4.5:1 (1.4.3 AA); 3:1 for large text.
- Graphical objects needed for understanding: 3:1 against adjacent colours
  (1.4.11). W3C's own guidance treats each line/shape in a chart as a
  graphical object; where many adjacent colours make 3:1 impossible, giving
  areas a contrasting border is a common practitioner fix.
- Use of colour (1.4.1): colour must not be the *only* means of conveying
  information.
**Sources:** S-W3C-1411 (C), W3C WAI-IG thread (D).
