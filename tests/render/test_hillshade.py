import numpy as np

from nzat.render.hillshade import H, W, hillshade


def test_hillshade_direction():
    # Log 0017: the first renderer lit slopes from the opposite side. Never again.
    y, x = np.mgrid[0:H, 0:W].astype(float)
    z = 1000 * np.exp(-((x - 310) ** 2 + (y - 230) ** 2) / (2 * 60**2))
    for az, lit, dark in [
        (315, (180, 260), (280, 360)),
        (0, (170, 310), (290, 310)),
        (90, (230, 370), (230, 250)),
    ]:
        sh = hillshade(z, [az], [1])
        assert sh[lit] > 0.9 and sh[dark] < 0.1, az
