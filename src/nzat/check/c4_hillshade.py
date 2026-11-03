def c4_hillshade(style, variant):
    failures = []
    for layer in style["layers"]:
        if layer["type"] != "hillshade":
            continue
        direction = layer["paint"].get("hillshade-illumination-direction")
        primary = direction[0] if isinstance(direction, list) else direction
        if primary != 337.5:
            failures.append(f"C4: {variant}:{layer['id']} primary light {primary}")
    return failures
