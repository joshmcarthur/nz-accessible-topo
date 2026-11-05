import re

SPOT_HEIGHT = re.compile(r"^\d+(\.\d+)?m?$")


def is_spot_height(text):
    """A spot-height label is a number, with an optional m. It must stay by its dot."""
    return bool(SPOT_HEIGHT.match((text or "").strip()))
