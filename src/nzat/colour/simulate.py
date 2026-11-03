import numpy as np

from nzat.colour.srgb import linear_to_srgb, srgb_to_linear

# Machado, Oliveira & Fernandes (2009), severity 1.0, linear RGB.
MACHADO = {
    "protanopia": np.array(
        [
            [0.152286, 1.052583, -0.204868],
            [0.114503, 0.786281, 0.099216],
            [-0.003882, -0.048116, 1.051998],
        ]
    ),
    "deuteranopia": np.array(
        [
            [0.367322, 0.860646, -0.227968],
            [0.280085, 0.672501, 0.047413],
            [-0.011820, 0.042940, 0.968881],
        ]
    ),
    "tritanopia": np.array(
        [
            [1.255528, -0.076749, -0.178779],
            [-0.078411, 0.930809, 0.147602],
            [0.004733, 0.691367, 0.303900],
        ]
    ),
}


def simulate(rgb, kind):
    lin = srgb_to_linear(rgb)
    return tuple(linear_to_srgb(MACHADO[kind] @ lin))
