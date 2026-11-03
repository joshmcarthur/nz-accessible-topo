import tifffile
from PIL import Image


def load_image(path):
    if path.lower().endswith((".tif", ".tiff")):
        return Image.fromarray(tifffile.imread(path)[..., :3])
    return Image.open(path).convert("RGB")
