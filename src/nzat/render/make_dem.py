import math

import numpy as np

from nzat.render.hillshade import H, W


def make_dem():
    y, x = np.mgrid[0:H, 0:W].astype(float)
    z = 350 + 0.0 * x

    def g(cx, cy, sx, sy, h, rot=0):
        c, s = math.cos(rot), math.sin(rot)
        dx, dy = x - cx, y - cy
        u, v = c * dx + s * dy, -s * dx + c * dy
        return h * np.exp(-(u**2 / (2 * sx**2) + v**2 / (2 * sy**2)))

    z += g(330, 170, 260, 55, 900, math.radians(30))
    z += g(400, 140, 70, 60, 450)
    z += g(210, 300, 120, 35, 420, math.radians(-50))
    z += g(500, 330, 90, 40, 380, math.radians(70))
    z -= g(150, 120, 60, 45, 160)
    z += 18 * np.sin(x / 23.0) * np.cos(y / 31.0)
    return z
