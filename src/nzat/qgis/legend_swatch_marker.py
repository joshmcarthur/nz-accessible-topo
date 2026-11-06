def set_svg_marker_size_mm(layer, size_mm):
    """Resize a single-symbol SvgMarker layer for legend swatch rendering."""
    from qgis.core import (  # noqa: E402
        QgsSingleSymbolRenderer,
        QgsSvgMarkerSymbolLayer,
        QgsUnitTypes,
    )

    renderer = layer.renderer()
    if not isinstance(renderer, QgsSingleSymbolRenderer):
        raise RuntimeError(f"legend swatch expected single symbol on {layer.name()}")
    symbol = renderer.symbol()
    for index in range(symbol.symbolLayerCount()):
        sl = symbol.symbolLayer(index)
        if isinstance(sl, QgsSvgMarkerSymbolLayer):
            sl.setSize(float(size_mm))
            sl.setSizeUnit(QgsUnitTypes.RenderUnit.RenderMillimeters)
            return
    raise RuntimeError(f"legend swatch has no SvgMarker on {layer.name()}")
