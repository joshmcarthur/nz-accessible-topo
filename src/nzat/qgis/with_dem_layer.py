def with_dem_layer(layers, dem_layer):
    """Put a valid DEM under the map layers so elevation shading can read it."""
    if dem_layer is None:
        return layers
    return [dem_layer] + [layer for layer in layers if layer is not dem_layer]
