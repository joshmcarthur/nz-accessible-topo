from nzat.style.vector_params import SPRITE_ID


def paint_sprite_meta(builder, variant):
    old = builder.style.get("sprite")
    builder.style["sprite"] = [
        {"id": "default", "url": old},
        {"id": SPRITE_ID, "url": "./sprites/nzat"},
    ]
    builder.note(
        "infra",
        "(style)",
        f"sprite → multi-sprite: LINZ default + `{SPRITE_ID}` (patterns for R-10/R-11)",
    )
    builder.style["name"] = f"NZ Accessible Topo {variant}"
    builder.style.setdefault("metadata", {})["nzat:derived-from"] = (
        "Vector form of tools/style-topo50.json on the Shortbread catalog "
        "linz/basemaps-config config/style/topographic-v2.json (MIT, Crown copyright LINZ). "
        "Data: LINZ CC BY 4.0. See upstream/README.md."
    )
    builder.style["id"] = f"nzat_{variant.replace('-', '_')}"
    if "id" in builder.doc and builder.doc is not builder.style:
        builder.doc["id"] = builder.style["id"]
        builder.doc["name"] = builder.style["name"]
