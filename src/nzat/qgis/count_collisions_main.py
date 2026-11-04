import argparse
import json
import os
import sys

from nzat.qgis.font_files import font_files
from nzat.qgis.map_layers import map_layers
from nzat.qgis.new_collisions import new_collisions
from nzat.qgis.qgis_prefix import qgis_prefix

FACE_DPI = 150
# 2000 m2 on the ground is 0.8 mm2 on the 1:50,000 sheet.
REPORT_AREAS_M2 = (500, 2000, 5000)
MIN_OVERLAP_M2 = 25


def main():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    parser = argparse.ArgumentParser(
        description="Count label pairs whose label shapes overlap on a map face."
    )
    parser.add_argument("--project", required=True)
    parser.add_argument("--font", action="append", default=[])
    parser.add_argument("--extent", required=True, help="XMIN,YMIN,XMAX,YMAX")
    parser.add_argument("--output", required=True, help="JSON of colliding pairs")
    parser.add_argument("--compare", help="Stock JSON from an earlier run")
    args = parser.parse_args()
    extent = [float(value) for value in args.extent.split(",")]

    # QGIS is only in the QGIS Python. Tests import new_collisions on the host.
    from qgis.core import (  # noqa: E402
        QgsApplication,
        QgsCoordinateReferenceSystem,
        QgsExpressionContext,
        QgsExpressionContextUtils,
        QgsMapRendererSequentialJob,
        QgsMapSettings,
        QgsProject,
        QgsRectangle,
    )
    from qgis.PyQt.QtCore import QSize  # noqa: E402
    from qgis.PyQt.QtGui import QFontDatabase  # noqa: E402

    QgsApplication.setPrefixPath(qgis_prefix(os.environ.get("QGIS_PREFIX_PATH")), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        for path in font_files(args.font):
            if QFontDatabase.addApplicationFont(path) < 0:
                print(f"font not loaded: {path}", file=sys.stderr)
                return 1
        project = QgsProject.instance()
        if not project.read(args.project):
            print(f"failed to read {args.project}", file=sys.stderr)
            return 1
        layers = map_layers(project)
        settings = QgsMapSettings()
        settings.setLayers(layers)
        settings.setDestinationCrs(QgsCoordinateReferenceSystem.fromEpsgId(2193))
        settings.setExtent(QgsRectangle(*extent))
        mm_per_m = 1000 / 50000
        settings.setOutputSize(
            QSize(
                round((extent[2] - extent[0]) * mm_per_m / 25.4 * FACE_DPI),
                round((extent[3] - extent[1]) * mm_per_m / 25.4 * FACE_DPI),
            )
        )
        settings.setOutputDpi(FACE_DPI)
        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.globalScope())
        context.appendScope(QgsExpressionContextUtils.projectScope(project))
        settings.setExpressionContext(context)
        settings.setLabelingEngineSettings(project.labelingEngineSettings())
        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        labels = [
            label
            for label in job.takeLabelingResults().allLabels()
            if not label.isUnplaced
        ]
        pairs = []
        for i, first in enumerate(labels):
            for second in labels[i + 1 :]:
                if not first.labelRect.intersects(second.labelRect):
                    continue
                overlap = first.labelGeometry.intersection(second.labelGeometry)
                if overlap.isEmpty() or overlap.area() < MIN_OVERLAP_M2:
                    continue
                centre = first.labelRect.center()
                pairs.append(
                    {
                        "a": first.labelText,
                        "b": second.labelText,
                        "x": round(centre.x()),
                        "y": round(centre.y()),
                        "area": round(overlap.area()),
                    }
                )
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump({"labels": len(labels), "pairs": pairs}, handle, indent=1)
        print(f"{len(labels)} labels, {len(pairs)} overlapping pairs")
        if args.compare:
            with open(args.compare, encoding="utf-8") as handle:
                stock = json.load(handle)["pairs"]
            counts = [
                len(new_collisions(pairs, stock, area)) for area in REPORT_AREAS_M2
            ]
            print(
                "new collisions over "
                + ", ".join(
                    f"{a} m2: {n}" for a, n in zip(REPORT_AREAS_M2, counts, strict=True)
                )
            )
            for pair in new_collisions(pairs, stock, REPORT_AREAS_M2[1])[:20]:
                print(
                    f"  {pair['area']:6d} m2  {pair['a']!r} | {pair['b']!r}  {pair['x']}, {pair['y']}"
                )
    finally:
        qgs.exitQgis()
    return 0
