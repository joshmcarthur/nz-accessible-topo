import copy

from nzat.style.vector_params import SPRITE_ID
from nzat.style.vegetation_fill import vegetation_fill


def paint_vegetation(builder, rules):
    native = vegetation_fill("native", rules)
    scrub = vegetation_fill("scrub", rules)
    scattered = vegetation_fill("scattered", rules)
    builder.layer("Vegetation-Native")["paint"]["fill-color"] = native
    builder.note("R-17", "Vegetation-Native", f"fill → {native}")
    builder.layer("Vegetation-Scrub")["paint"]["fill-color"] = scrub
    builder.note("R-10", "Vegetation-Scrub", f"fill → {scrub}")
    sc = builder.layer("Vegetation-Scatteredscrub")
    sc["paint"]["fill-color"] = scattered
    builder.note("R-10", "Vegetation-Scatteredscrub", f"fill → {scattered}")
    stipple = {
        "id": "NZAT-Vegetation-Scatteredscrub-Stipple",
        "type": "fill",
        "source": sc["source"],
        "source-layer": sc["source-layer"],
        "filter": copy.deepcopy(sc["filter"]),
        "minzoom": 11,
        "paint": {"fill-pattern": f"{SPRITE_ID}:scattered_stipple"},
    }
    builder.insert_after(
        sc["id"],
        stipple,
        "R-10",
        "stipple so scattered scrub survives greyscale and CVD",
    )
