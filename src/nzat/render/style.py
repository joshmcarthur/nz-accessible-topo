import json

from nzat.colour.parse_colour import parse_colour
from nzat.render.hillshade import Z
from nzat.render.interp import interp


class Style:
    def __init__(self, path):
        d = json.load(open(path))
        self.s = d.get("style", d)
        self.by = {layer["id"]: layer for layer in self.s["layers"]}

    def has(self, lid):
        layer = self.by.get(lid)
        return layer is not None and layer.get("layout", {}).get("visibility") != "none"

    def p(self, lid, prop, default=None, z=Z):
        return interp(self.by[lid].get("paint", {}).get(prop, default), z)

    def lay(self, lid, prop, default=None, z=Z):
        return interp(self.by[lid].get("layout", {}).get(prop, default), z)

    def colour(self, lid, prop, z=Z):
        c = parse_colour(self.p(lid, prop, z=z))
        op = self.p(lid, prop.split("-")[0] + "-opacity", 1, z=z)
        op = op if isinstance(op, (int, float)) else 1
        return (c[0], c[1], c[2], c[3] * op)
