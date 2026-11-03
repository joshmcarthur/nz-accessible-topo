from PIL import Image, ImageDraw, ImageFont

LINES = [
    ("Place names", "Taupō · Ōtautahi · Ōpōtiki · Ōamaru · Whanganui-a-Tara"),
    ("Confusables", "Il1|  O0  B8  rn m  5S  2Z  6b"),
    ("Grid ref / trig", "BX24 157 710 · Trig A5MH · 1432 m"),
]


def _load(spec, size):
    path, _, w = spec.partition("@")
    f = ImageFont.truetype(path, size)
    if w:
        try:
            axes = f.get_variation_axes()
            f.set_variation_by_axes(
                [
                    int(w) if a["name"] in (b"Weight", "Weight") else a["default"]
                    for a in axes
                ]
            )
        except Exception:
            pass
    return f


def main(out, specs):
    S, pad = 2, 16
    rows = []
    hdr = ImageFont.truetype(specs[0].split("=", 1)[1].partition("@")[0], 15 * S)
    for spec in specs:
        name, path = spec.split("=", 1)
        for size in (26, 11):
            f = _load(path, size * S)
            for lab, txt in LINES if size == 26 else LINES[:1]:
                rows.append((f"{name} — {lab} ({size}px)", txt, f, size))
    width = 1150 * S
    height = sum((r[3] + 30) * S for r in rows) + pad * S
    im = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(im)
    y = pad * S // 2
    for lab, txt, f, size in rows:
        d.text((pad * S, y), lab, font=hdr, fill=(110, 110, 110))
        d.text((pad * S, y + 16 * S), txt, font=f, fill=(20, 20, 20))
        y += (size + 30) * S
    im.save(out)
    print("wrote", out)
