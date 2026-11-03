from nzat.colour.srgb import linear_to_srgb


def lab_to_rgb(lab):
    L, a, b = lab
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    def finv(t):
        return t**3 if t > 6 / 29 else 3 * (6 / 29) ** 2 * (t - 4 / 29)

    x, y, z = finv(fx) * 0.95047, finv(fy), finv(fz) * 1.08883
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bb = 0.0557 * x - 0.2040 * y + 1.0570 * z
    return tuple(float(v) for v in linear_to_srgb([r, g, bb]))
