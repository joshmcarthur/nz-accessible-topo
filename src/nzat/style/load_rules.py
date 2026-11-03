import json

from nzat.paths import STYLE_PATH


def load_rules(path=None):
    with open(path or STYLE_PATH, encoding="utf-8") as handle:
        return json.load(handle)
