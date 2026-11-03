from nzat.colour.srgb import srgb_to_linear


def red_light_reflectance(rgb):
    """Relative reflectance under narrow-band red light: linear R channel only."""
    return float(srgb_to_linear(rgb)[0])
