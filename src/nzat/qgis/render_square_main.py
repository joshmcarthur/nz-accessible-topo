import argparse
import os
import sys

from nzat.qgis.defaults import DEM_LAYER_NAME
from nzat.qgis.dem_path import dem_path
from nzat.qgis.font_files import font_files
from nzat.qgis.hillshade_rules import hillshade_rules
from nzat.qgis.hillshade_should_paint import hillshade_should_paint
from nzat.qgis.map_layers import SHEET_PRESET, map_layers
from nzat.qgis.qgis_prefix import qgis_prefix
from nzat.qgis.square_extent import square_extent
from nzat.qgis.with_dem_layer import with_dem_layer

DPI = 600
PX = 472


def _free_gb(path):
    if not os.path.isdir(path):
        return None
    stats = os.statvfs(path)
    return stats.f_bavail * stats.f_frsize / (1024**3)


def _parse_square(text):
    east_text, north_text, output = text.split(",", 2)
    return float(east_text), float(north_text), output


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    parser = argparse.ArgumentParser(description="Render 1 km map squares at 600 dpi.")
    parser.add_argument("--project", required=True, help="Path to the .qgs file")
    parser.add_argument(
        "--font",
        action="append",
        default=[],
        help="A font file or a directory of .otf and .ttf files",
    )
    parser.add_argument(
        "--square", action="append", required=True, help="EAST,NORTH,OUTPUT.png"
    )
    args = parser.parse_args()

    for path in ("/System/Volumes/Data", "/working", "/"):
        free = _free_gb(path)
        if free is None:
            continue
        print(f"free disk on {path}: {free:.1f} GB")
        if free < 8:
            print(
                f"free disk on {path} is {free:.1f} GB. Stop. The floor is 8 GB.",
                file=sys.stderr,
            )
            return 1

    # QGIS is installed in the map container only. A top-level import fails on the host.
    from qgis.core import (  # noqa: E402
        QgsApplication,
        QgsCoordinateReferenceSystem,
        QgsExpression,
        QgsExpressionContext,
        QgsExpressionContextUtils,
        QgsMapRendererParallelJob,
        QgsMapSettings,
        QgsProject,
        QgsRectangle,
    )
    from qgis.PyQt.QtCore import QSize  # noqa: E402
    from qgis.PyQt.QtGui import QColor, QFontDatabase  # noqa: E402

    squares = [_parse_square(item) for item in args.square]
    fonts = font_files(args.font)

    prefix = qgis_prefix(os.environ.get("QGIS_PREFIX_PATH"))
    print(f"qgis prefix {prefix}")
    QgsApplication.setPrefixPath(prefix, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        for path in fonts:
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id < 0:
                print(f"font not loaded: {path}", file=sys.stderr)
                return 1
            print(f"font loaded: {path}")

        project = QgsProject.instance()
        if not project.read(args.project):
            print(f"failed to read {args.project}", file=sys.stderr)
            return 1

        try:
            layers = map_layers(project)
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 1
        if not layers:
            print(f"theme {SHEET_PRESET} has no valid map layers", file=sys.stderr)
            return 1
        project_dir = os.path.dirname(os.path.abspath(args.project))
        dem_layer = None
        rules = hillshade_rules()
        if hillshade_should_paint(project_dir):
            from qgis.core import QgsElevationUtils, QgsRasterLayer  # noqa: E402

            for layer in project.mapLayers().values():
                if layer.name() == DEM_LAYER_NAME and layer.isValid():
                    dem_layer = layer
                    break
            if dem_layer is None:
                raster = dem_path(project_dir)
                dem_layer = QgsRasterLayer(raster, DEM_LAYER_NAME)
                if not dem_layer.isValid():
                    print(f"dem not loaded: {raster}", file=sys.stderr)
                    dem_layer = None
                else:
                    QgsElevationUtils.enableElevationForLayer(dem_layer)
                    print(f"dem loaded: {raster}")
        else:
            print(f"hillshade off: no {rules['raster_file']}")
        layers = with_dem_layer(layers, dem_layer)
        print(f"layers {len(layers)} theme {SHEET_PRESET}")
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

        for east, north, output in squares:
            os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
            settings = QgsMapSettings()
            settings.setLayers(layers)
            settings.setDestinationCrs(QgsCoordinateReferenceSystem.fromEpsgId(2193))
            settings.setExtent(QgsRectangle(*square_extent(east, north)))
            settings.setOutputSize(QSize(PX, PX))
            settings.setOutputDpi(DPI)
            settings.setBackgroundColor(QColor(255, 255, 255))
            settings.setTransformContext(project.transformContext())
            settings.setExpressionContext(color_context)
            renderer = project.elevationShadingRenderer()
            if hillshade_should_paint(project_dir):
                renderer.setActive(True)
                renderer.setActiveHillshading(True)
                renderer.setLightAzimuth(rules["azimuth_deg"])
                renderer.setLightAltitude(rules["altitude_deg"])
                renderer.setHillshadingMultidirectional(rules["multidirectional"])
                renderer.setHillshadingZFactor(rules["z_factor"])
            settings.setElevationShadingRenderer(renderer)
            if flag is not None:
                settings.setFlag(flag, True)

            job = QgsMapRendererParallelJob(settings)
            job.start()
            job.waitForFinished()
            image = job.renderedImage()
            if image.isNull() or not image.save(output):
                print(f"failed to write {output}", file=sys.stderr)
                return 1
            print(f"wrote {output} {image.width()}x{image.height()}")
    finally:
        qgs.exitQgis()
    return 0
