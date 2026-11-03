from nzat.style.lookup_style_path import lookup_style_path


def paint_hillshade(builder, rules, multidirectional=False):
    azimuth = lookup_style_path(rules, "hillshade.azimuth_deg")
    fills = lookup_style_path(rules, "hillshade.fill_azimuths_deg")
    painted = lookup_style_path(rules, "hillshade.painted")
    for layer in builder.style["layers"]:
        if layer["type"] != "hillshade":
            continue
        paint = layer["paint"]
        old = paint.get("hillshade-illumination-direction")
        if not painted:
            layer.setdefault("layout", {})["visibility"] = "none"
            builder.note(
                "R-03", layer["id"], "visibility none — hillshade.painted is false"
            )
            continue
        if not multidirectional:
            paint["hillshade-illumination-direction"] = azimuth
            builder.note(
                "R-03", layer["id"], f"illumination direction {old} → {azimuth} (NNW)"
            )
            continue
        paint["hillshade-method"] = "multidirectional"
        paint["hillshade-illumination-direction"] = [azimuth, *fills]
        paint["hillshade-illumination-altitude"] = [45, 45, 45]
        paint["hillshade-highlight-color"] = [
            "rgba(255,255,255,0.30)",
            "rgba(255,255,255,0.12)",
            "rgba(255,255,255,0.12)",
        ]
        paint["hillshade-shadow-color"] = [
            "rgba(12,12,12,0.45)",
            "rgba(12,12,12,0.18)",
            "rgba(12,12,12,0.18)",
        ]
        paint.pop("hillshade-accent-color", None)
        builder.note(
            "R-03",
            layer["id"],
            f"multidirectional: primary {azimuth}° + weaker {'/'.join(str(item) for item in fills)}° fill lights "
            "(F-16). Colours are provisional — tune visually (OQ-07)",
        )
