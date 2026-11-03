import json


def c1_stale(path, on_disk, built_doc):
    if on_disk != json.loads(json.dumps(built_doc)):
        return [f"C1: {path} is stale — run tools/build_style.py"]
    return []
