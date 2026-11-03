from nzat.colour.ciede2000 import ciede2000
from nzat.colour.composite import composite
from nzat.colour.contrast_ratio import contrast_ratio
from nzat.colour.parse_colour import parse_colour
from nzat.colour.red_light import red_light_reflectance
from nzat.colour.rel_luminance import rel_luminance
from nzat.colour.rgb_to_lab import rgb_to_lab
from nzat.colour.simulate import MACHADO, simulate


def pair_audit(pairs, bg):
    out = []
    for p in pairs:
        a = composite(parse_colour(p["a"]["colour"]), bg)
        b = composite(parse_colour(p["b"]["colour"]), bg)
        res = {
            "name": p["name"],
            "a": p["a"]["label"],
            "b": p["b"]["label"],
            "why": p.get("why", ""),
        }
        res["normal"] = ciede2000(rgb_to_lab(a), rgb_to_lab(b))
        for k in MACHADO:
            res[k] = ciede2000(rgb_to_lab(simulate(a, k)), rgb_to_lab(simulate(b, k)))
        res["grey_cr"] = contrast_ratio(rel_luminance(a), rel_luminance(b))
        res["red_cr"] = contrast_ratio(
            red_light_reflectance(a), red_light_reflectance(b)
        )
        out.append(res)
    return out
