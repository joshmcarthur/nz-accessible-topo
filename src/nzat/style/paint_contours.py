import copy

from nzat.style.index_line_width import index_line_width
from nzat.style.intermediate_casing_width import intermediate_casing_width
from nzat.style.lookup_style_path import lookup_style_path
from nzat.style.vector_params import P


def paint_contours(builder, rules):
    idx = builder.layer("Contours-Index")
    idx_colour = lookup_style_path(rules, "contours.index.colour")
    idx_alpha = lookup_style_path(rules, "contours.index.alpha")
    idx["paint"]["line-color"] = idx_colour
    idx["paint"]["line-opacity"] = {
        "stops": [[10, round(0.6 * idx_alpha, 2)], [11, idx_alpha]]
    }
    idx["paint"]["line-width"] = index_line_width(rules)
    builder.note(
        "R-04", "Contours-Index", f"colour → {idx_colour} alpha {idx_alpha}, width ↑"
    )
    halo = builder.layer("Contours-Index-Halo")
    halo.setdefault("layout", {})["visibility"] = "none"
    builder.note(
        "R-04",
        "Contours-Index-Halo",
        "hidden — darker index line no longer needs a 10% offset shadow",
    )
    mid_colour = lookup_style_path(rules, "contours.intermediate.colour")
    mid_alpha = lookup_style_path(rules, "contours.intermediate.alpha")
    for lid in ("Contours-All", "Contours-Designated", "Contours-Natural"):
        layer = builder.layer(lid)
        layer["paint"]["line-color"] = mid_colour
        if lid == "Contours-All":
            layer["paint"]["line-width"] = P["contour_intermediate_width"]
            layer["paint"]["line-opacity"] = {
                "stops": [[13, round(0.6 * mid_alpha, 2)], [14, mid_alpha]]
            }
        else:
            layer["paint"]["line-opacity"] = mid_alpha
        builder.note("R-04", lid, f"colour → {mid_colour} alpha {mid_alpha}")
    all_layer = builder.layer("Contours-All")
    casing = {
        "id": "NZAT-Contours-All-Casing",
        "type": "line",
        "source": all_layer["source"],
        "source-layer": all_layer["source-layer"],
        "filter": copy.deepcopy(all_layer["filter"]),
        "minzoom": all_layer.get("minzoom", 13),
        "layout": copy.deepcopy(all_layer.get("layout", {})),
        "paint": {
            "line-color": lookup_style_path(
                rules, "contours.intermediate.casing_colour"
            ),
            "line-width": intermediate_casing_width(rules),
            "line-opacity": copy.deepcopy(all_layer["paint"].get("line-opacity", 1)),
        },
    }
    builder.insert_after(
        "Contours-Index-Halo",
        casing,
        "R-01",
        "index-ink casing under intermediate fill so the line meets 3:1 under red light",
    )
