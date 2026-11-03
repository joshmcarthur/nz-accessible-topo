SHEET_PRESET = "Map5View"


def map_layers(project, preset=SHEET_PRESET):
    ordered = []
    for item in project.layerTreeRoot().layerOrder():
        layer = item.layer() if hasattr(item, "layer") else item
        if layer is not None and layer.isValid():
            ordered.append(layer)
    themes = project.mapThemeCollection()
    if not themes.hasMapTheme(preset):
        names = ", ".join(themes.mapThemes())
        raise RuntimeError(f"project has no map theme {preset}. Themes: {names}")
    visible = {layer.id() for layer in themes.mapThemeVisibleLayers(preset)}
    return [layer for layer in ordered if layer.id() in visible]
