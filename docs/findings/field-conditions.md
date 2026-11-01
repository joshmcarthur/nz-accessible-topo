# Findings: field conditions

## F-21 — Under red light, red ink disappears
Paper only reflects the wavelengths that hit it. Under a narrow-band red
headtorch, red and magenta ink reflect about as much as white paper, so
they vanish; blues and greens go dark. Navigators report missing red
features on charts under red light, and some military land-navigation
training changed red map features to a red-brown for this reason.
**Sources:** physics (reflectance), S-FORUM-REDLIGHT (D, multiple
practitioner reports).
**Grade:** D for the anecdotes; the physical mechanism is not in doubt.
**Our model:** contours drop to ~1.4:1 against paper; the closed-track red
shadow to ~1.1:1 (W7, W8).
**Implication:** anything safety-relevant (closed tracks, hazards, huts)
must be encoded in **lightness + shape**, never in red hue alone.

## F-22 — Dim light worsens colour discrimination for everyone, more for CVD
Under reduced illumination, people with colour vision impairment make
considerably more colour-identification errors (F-01); older observers'
blue–yellow losses resemble those of young people in dim light (F-02).
**Implication:** design the print palette for dusk/tent light, not a
well-lit desk. Lightness contrast is the robust channel.

## F-23 — Maps are photocopied, printed mono, and read on e-ink
Greyscale reproduction is common (club handouts, SAR briefings, e-ink GPS
units, some inReach/e-reader devices). Our audit shows several key pairs
with near-identical luminance (W4, W5, W6).
**Sources:** audit (D); practitioner guidance on mono-legible maps (C,
Harvard Library QGIS publishing guide).
