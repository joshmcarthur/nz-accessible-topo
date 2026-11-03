from nzat.check.fonts_in import fonts_in

MACRON_VERIFIED = ("Open Sans", "Roboto", "Noto Sans")


def c5_fonts(style, variant):
    return [
        f"C5: {variant}:{lid} uses unverified family {font}"
        for lid, font in fonts_in(style)
        if not font.startswith(MACRON_VERIFIED)
    ]
