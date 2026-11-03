from nzat.colour.srgb import srgb_to_linear


def rel_luminance(rgb):
    r, g, b = srgb_to_linear(rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
