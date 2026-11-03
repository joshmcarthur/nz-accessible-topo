from nzat.style.vector_params import P


def intermediate_casing_width(rules):
    """Return vector casing width stops. Scale the fill stops by the millimetre ratio."""
    mid = rules["contours"]["intermediate"]
    factor = mid["casing_width_mm"] / mid["width_mm"]
    return {
        "stops": [
            [z, round(w * factor, 2)]
            for z, w in P["contour_intermediate_width"]["stops"]
        ]
    }
