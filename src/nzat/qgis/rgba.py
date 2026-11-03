def _hex_rgb(colour):
    text = colour.lstrip("#")
    return tuple(int(text[index : index + 2], 16) for index in (0, 2, 4))


def alpha_byte(alpha):
    return int(round(float(alpha) * 255))


def rgb_call(colour):
    red, green, blue = _hex_rgb(colour)
    return f"color_rgb({red},{green},{blue})"


def rgba_call(colour, alpha):
    red, green, blue = _hex_rgb(colour)
    return f"color_rgba({red},{green},{blue},{alpha_byte(alpha)})"


def rgba(colour, alpha):
    red, green, blue = _hex_rgb(colour)
    return f"{red},{green},{blue},{alpha}"
