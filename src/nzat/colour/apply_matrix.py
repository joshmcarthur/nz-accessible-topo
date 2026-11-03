import numpy as np
from PIL import Image

from nzat.colour.srgb import linear_to_srgb, srgb_to_linear

GREYSCALE = np.array([[0.2126, 0.7152, 0.0722]] * 3)
RED_HEADTORCH = np.array([[1.0, 0, 0]] * 3)


def apply_matrix(img, matrix):
    """Apply a 3×3 linear-RGB matrix to a Pillow image. None leaves the image as-is."""
    if matrix is None:
        return img
    lin = srgb_to_linear(np.asarray(img).astype(float))
    out = linear_to_srgb(lin @ np.asarray(matrix).T)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
