import math

import numpy as np

Z = 14
S = 2
W, H = 620, 460
M_PER_PX = 6.5


def hillshade(z, azimuths, weights, alt=45, exag=1.0):
    """Lambertian shading. Azimuth is clockwise from north (map convention).
    Image rows run north→south, so the northward gradient is -d/drow.
    Verified: a hill lit from 315° is bright on its upper-left (NW) side."""
    dz_drow, dz_dcol = np.gradient(z * exag, M_PER_PX)
    dz_de, dz_dn = dz_dcol, -dz_drow
    n = np.stack([-dz_de, -dz_dn, np.ones_like(z)])
    n /= np.linalg.norm(n, axis=0)
    out = np.zeros_like(z)
    for az, w in zip(azimuths, weights, strict=True):
        a, h = math.radians(az), math.radians(alt)
        light = np.array(
            [math.sin(a) * math.cos(h), math.cos(a) * math.cos(h), math.sin(h)]
        )
        out += w * np.clip(np.tensordot(light, n, axes=1), 0, 1)
    return out / sum(weights)
