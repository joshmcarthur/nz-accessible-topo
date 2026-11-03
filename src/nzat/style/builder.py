import copy


class Builder:
    def __init__(self, style):
        self.doc = copy.deepcopy(style)
        self.style = self.doc.get("style", self.doc)
        self.log = []

    def note(self, rid, layer, what):
        self.log.append((rid, layer, what))

    def layer(self, lid):
        for layer in self.style["layers"]:
            if layer["id"] == lid:
                return layer
        raise KeyError(lid)

    def insert_after(self, lid, new_layer, rid, why):
        idx = next(
            i for i, layer in enumerate(self.style["layers"]) if layer["id"] == lid
        )
        self.style["layers"].insert(idx + 1, new_layer)
        self.note(rid, new_layer["id"], f"added after `{lid}` — {why}")
