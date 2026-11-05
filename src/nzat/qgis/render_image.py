def render_image(session, xmin, ymin, xmax, ymax, width, height, dpi):
    """Draw one NZTM rectangle with the map from open_map. Return the QImage."""
    from qgis.core import (  # noqa: E402
        QgsCoordinateReferenceSystem,
        QgsMapRendererParallelJob,
        QgsMapSettings,
        QgsRectangle,
    )
    from qgis.PyQt.QtCore import QSize  # noqa: E402
    from qgis.PyQt.QtGui import QColor  # noqa: E402

    project = session["project"]
    rules = session["rules"]
    settings = QgsMapSettings()
    settings.setLayers(session["layers"])
    settings.setDestinationCrs(QgsCoordinateReferenceSystem.fromEpsgId(2193))
    settings.setExtent(QgsRectangle(xmin, ymin, xmax, ymax))
    settings.setOutputSize(QSize(width, height))
    settings.setOutputDpi(dpi)
    settings.setBackgroundColor(QColor(255, 255, 255))
    settings.setTransformContext(project.transformContext())
    settings.setExpressionContext(session["color_context"])
    renderer = project.elevationShadingRenderer()
    if session["hillshade"]:
        renderer.setActive(True)
        renderer.setActiveHillshading(True)
        renderer.setLightAzimuth(rules["azimuth_deg"])
        renderer.setLightAltitude(rules["altitude_deg"])
        renderer.setHillshadingMultidirectional(rules["multidirectional"])
        renderer.setHillshadingZFactor(rules["z_factor"])
    settings.setElevationShadingRenderer(renderer)
    if session["flag"] is not None:
        settings.setFlag(session["flag"], True)

    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    return job.renderedImage()
