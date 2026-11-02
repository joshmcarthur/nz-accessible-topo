#!/usr/bin/env python3
"""Draw 1 km map squares at 600 dpi.

Run this inside the map container. The host Python does not have QGIS.
1000 m on the ground is 20 mm on the 1:50,000 sheet. 20 mm at 600 dpi is 472 px.
The script draws the map face only. It draws the Map5View layers. It does not export the sheet page.

Load every .ttf with QFontDatabase. The stock exporter loads only .otf files.
Set HOME=/tmp before QGIS starts so fontconfig can write a cache.
"""

import argparse
import glob
import os
import sys

METRES = 1000
DPI = 600
PX = 472
SHEET_PRESET = "Map5View"
CONTAINER_PREFIX = "/usr"


def square_extent(east, north, metres=METRES):
    """Return xmin, ymin, xmax, ymax for a square whose south-west corner is given."""
    return (east, north, east + metres, north + metres)


def free_gb(path):
    if not os.path.isdir(path):
        return None
    stats = os.statvfs(path)
    return stats.f_bavail * stats.f_frsize / (1024 ** 3)


def parse_square(text):
    east_text, north_text, output = text.split(",", 2)
    return float(east_text), float(north_text), output


def font_files(paths):
    found = []
    for path in paths:
        if os.path.isdir(path):
            found.extend(sorted(glob.glob(os.path.join(path, "*.otf"))))
            found.extend(sorted(glob.glob(os.path.join(path, "*.ttf"))))
        elif os.path.isfile(path):
            found.append(path)
    return found


def qgis_prefix(env_value, default=CONTAINER_PREFIX):
    """Return the QGIS prefix. An empty value keeps the container prefix."""
    text = (env_value or "").strip()
    return text or default


def sheet_layer_ids(ordered_ids, visible_ids):
    """Keep the layers the sheet map draws. Keep the project draw order."""
    visible = set(visible_ids)
    return [layer_id for layer_id in ordered_ids if layer_id in visible]


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


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    parser = argparse.ArgumentParser(description="Render 1 km map squares at 600 dpi.")
    parser.add_argument("--project", required=True, help="Path to the .qgs file")
    parser.add_argument("--font", action="append", default=[], help="A font file or a directory of .otf and .ttf files")
    parser.add_argument("--square", action="append", required=True, help="EAST,NORTH,OUTPUT.png")
    args = parser.parse_args()

    for path in ("/System/Volumes/Data", "/working", "/"):
        free = free_gb(path)
        if free is None:
            continue
        print(f"free disk on {path}: {free:.1f} GB")
        if free < 8:
            print(f"free disk on {path} is {free:.1f} GB. Stop. The floor is 8 GB.", file=sys.stderr)
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

    squares = [parse_square(item) for item in args.square]
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
        print(f"layers {len(layers)} theme {SHEET_PRESET}")
        for layer in layers:
            print(f"layer {layer.name()}")

        color_context = QgsExpressionContext()
        color_context.appendScope(QgsExpressionContextUtils.globalScope())
        color_context.appendScope(QgsExpressionContextUtils.projectScope(project))
        color_expr = QgsExpression("project_color_object('process_blue')")
        print(f"process_blue {color_expr.evaluate(color_context)} {color_expr.evalErrorString()}")

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


if __name__ == "__main__":
    sys.exit(main())
