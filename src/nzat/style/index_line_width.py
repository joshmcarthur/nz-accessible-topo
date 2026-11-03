from nzat.style.vector_params import P


def index_line_width(rules):
    """Return vector index width stops. Scale the 0.45 mm calibration by the print width."""
    width = rules["contours"]["index"]["width_mm"]
    factor = width / 0.45
    return {
        "stops": [
            [z, round(w * factor, 2)] for z, w in P["contour_index_width"]["stops"]
        ]
    }
