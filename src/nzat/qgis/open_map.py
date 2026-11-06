import os

from nzat.qgis.defaults import DEM_LAYER_NAME
from nzat.qgis.dem_path import dem_path
from nzat.qgis.hillshade_rules import hillshade_rules
from nzat.qgis.hillshade_should_paint import hillshade_should_paint
from nzat.qgis.map_layers import SHEET_PRESET, map_layers
from nzat.qgis.with_dem_layer import with_dem_layer


def open_map(project_path, fonts, preset=SHEET_PRESET):
    """Load fonts and the project once. Return what render_image needs.

    Call this after QgsApplication.initQgis(). Raise RuntimeError on a failure.
    """
    # QGIS is installed in the map container only. A top-level import fails on the host.
    from qgis.core import (  # noqa: E402
        QgsExpression,
        QgsExpressionContext,
        QgsExpressionContextUtils,
        QgsMapSettings,
        QgsProject,
    )
    from qgis.PyQt.QtGui import QFontDatabase  # noqa: E402

    for path in fonts:
        if QFontDatabase.addApplicationFont(path) < 0:
            raise RuntimeError(f"font not loaded: {path}")
        print(f"font loaded: {path}")

    project = QgsProject.instance()
    if not project.read(project_path):
        raise RuntimeError(f"failed to read {project_path}")

    layers = map_layers(project, preset)
    if not layers:
        raise RuntimeError(f"theme {preset} has no valid map layers")
    project_dir = os.path.dirname(os.path.abspath(project_path))
    dem_layer = None
    rules = hillshade_rules()
    hillshade = hillshade_should_paint(project_dir)
    if hillshade:
        from qgis.core import QgsElevationUtils, QgsRasterLayer  # noqa: E402

        for layer in project.mapLayers().values():
            if layer.name() == DEM_LAYER_NAME and layer.isValid():
                dem_layer = layer
                break
        if dem_layer is None:
            raster = dem_path(project_dir)
            dem_layer = QgsRasterLayer(raster, DEM_LAYER_NAME)
            if not dem_layer.isValid():
                print(f"dem not loaded: {raster}")
                dem_layer = None
            else:
                QgsElevationUtils.enableElevationForLayer(dem_layer)
                print(f"dem loaded: {raster}")
    else:
        print(f"hillshade off: no {rules['raster_file']}")
    layers = with_dem_layer(layers, dem_layer)
    print(f"layers {len(layers)} theme {preset}")
    for layer in layers:
        print(f"layer {layer.name()}")

    color_context = QgsExpressionContext()
    color_context.appendScope(QgsExpressionContextUtils.globalScope())
    color_context.appendScope(QgsExpressionContextUtils.projectScope(project))
    color_expr = QgsExpression("project_color_object('process_blue')")
    print(
        f"process_blue {color_expr.evaluate(color_context)} {color_expr.evalErrorString()}"
    )

    flag = getattr(QgsMapSettings, "DrawLabeling", None)
    if flag is None and hasattr(QgsMapSettings, "Flag"):
        flag = QgsMapSettings.Flag.DrawLabeling

    return {
        "project": project,
        "layers": layers,
        "color_context": color_context,
        "hillshade": hillshade,
        "rules": rules,
        "flag": flag,
    }
