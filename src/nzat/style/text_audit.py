from nzat.colour.composite import composite
from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.parse_colour import parse_colour
from nzat.colour.rel_luminance import rel_luminance


def text_audit(style, bg):
    rows = []
    for layer in style["layers"]:
        if layer.get("type") != "symbol":
            continue
        if layer.get("layout", {}).get("text-field") in (None, ""):
            continue
        paint = layer.get("paint", {})
        tc = (
            parse_colour(paint.get("text-color", ""))
            if isinstance(paint.get("text-color"), str)
            else None
        )
        if not tc:
            continue
        halo = (
            parse_colour(paint.get("text-halo-color", ""))
            if isinstance(paint.get("text-halo-color"), str)
            else None
        )
        halo_w = paint.get("text-halo-width", 0)
        behind = (
            composite(halo, bg)
            if halo and (not isinstance(halo_w, (int, float)) or halo_w > 0)
            else bg
        )
        fg = composite(tc, behind)
        cr = contrast_ratio(rel_luminance(fg), rel_luminance(behind))
        font = layer.get("layout", {}).get("text-font", [""])
        font = (
            font[0]
            if isinstance(font, list) and font and isinstance(font[0], str)
            else str(font)
        )
        rows.append(
            (
                layer["id"],
                cr,
                font,
                paint.get("text-color"),
                paint.get("text-halo-color"),
            )
        )
    return rows
