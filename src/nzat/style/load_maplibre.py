import json


def load_maplibre(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    return data.get("style", data)
