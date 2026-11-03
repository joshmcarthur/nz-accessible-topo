from nzat.check.fonts_in import fonts_in


def c2_italics(style, variant):
    return [
        f"C2: {variant}:{lid} uses {font}"
        for lid, font in fonts_in(style)
        if "Italic" in font
    ]
