from nzat.render.hillshade import Z


def interp(v, z=Z):
    if isinstance(v, dict) and "stops" in v:
        st = v["stops"]
        if z <= st[0][0]:
            return st[0][1]
        for (z0, a), (z1, b) in zip(st, st[1:], strict=False):
            if z0 <= z <= z1:
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    return a + (b - a) * (z - z0) / (z1 - z0)
                return a if z - z0 < z1 - z else b
        return st[-1][1]
    if isinstance(v, list) and v and v[0] == "interpolate":
        pts = v[3:]
        pairs = list(zip(pts[0::2], pts[1::2], strict=False))
        return interp({"stops": pairs}, z)
    return v
