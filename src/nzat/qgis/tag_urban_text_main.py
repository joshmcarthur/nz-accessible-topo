import argparse
import json
import os
import sys

from nzat.qgis.defaults import CARTO_TEXT_LAYER, URBAN_FILL_LAYER, URBAN_TEXT_FILE
from nzat.qgis.parse_extent import parse_extent
from nzat.qgis.qgis_prefix import qgis_prefix


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    parser = argparse.ArgumentParser(
        description="Write urban_text.json: carto_text row ids inside the urban fill."
    )
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--extent", help="XMIN,YMIN,XMAX,YMAX in EPSG:2193. Default: every row"
    )
    args = parser.parse_args()
    extent = parse_extent(args.extent) if args.extent else None

    # QGIS is only in the QGIS Python. Tests import the apply step on the host.
    from qgis.core import (  # noqa: E402
        QgsApplication,
        QgsCoordinateReferenceSystem,
        QgsCoordinateTransform,
        QgsFeatureRequest,
        QgsGeometry,
        QgsProject,
        QgsRectangle,
        QgsSpatialIndex,
    )

    QgsApplication.setPrefixPath(qgis_prefix(os.environ.get("QGIS_PREFIX_PATH")), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        project = QgsProject.instance()
        if not project.read(args.project):
            print(f"failed to read {args.project}", file=sys.stderr)
            return 1
        found = {}
        for name in (URBAN_FILL_LAYER, CARTO_TEXT_LAYER):
            layers = [
                layer for layer in project.mapLayersByName(name) if layer.isValid()
            ]
            if len(layers) != 1:
                print(
                    f"need one valid layer {name}, found {len(layers)}", file=sys.stderr
                )
                return 1
            found[name] = layers[0]
        urban, carto = found[URBAN_FILL_LAYER], found[CARTO_TEXT_LAYER]
        # The fill is one symbol on every row. A rule or category renderer would need its filter here.
        if urban.renderer().type() != "singleSymbol":
            print(
                f"{URBAN_FILL_LAYER} renderer is {urban.renderer().type()}",
                file=sys.stderr,
            )
            return 1

        to_carto = QgsCoordinateTransform(urban.crs(), carto.crs(), project)
        urban_request = QgsFeatureRequest().setNoAttributes()
        carto_request = QgsFeatureRequest().setSubsetOfAttributes(
            ["id"], carto.fields()
        )
        if extent:
            box = QgsRectangle(*extent)
            to_box = QgsCoordinateTransform(
                QgsCoordinateReferenceSystem.fromEpsgId(2193), urban.crs(), project
            )
            urban_request.setFilterRect(to_box.transformBoundingBox(box))
            to_text = QgsCoordinateTransform(
                QgsCoordinateReferenceSystem.fromEpsgId(2193), carto.crs(), project
            )
            carto_request.setFilterRect(to_text.transformBoundingBox(box))

        fills = {}
        index = QgsSpatialIndex()
        for feature in urban.getFeatures(urban_request):
            geometry = QgsGeometry(feature.geometry())
            if geometry.isEmpty():
                continue
            geometry.transform(to_carto)
            engine = QgsGeometry.createGeometryEngine(geometry.constGet())
            engine.prepareGeometry()
            fills[feature.id()] = engine
            index.addFeature(feature.id(), geometry.boundingBox())

        inside = set()
        rows = 0
        for feature in carto.getFeatures(carto_request):
            rows += 1
            geometry = feature.geometry()
            if geometry.isEmpty():
                continue
            for fid in index.intersects(geometry.boundingBox()):
                if fills[fid].intersects(geometry.constGet()):
                    inside.add(str(feature["id"]))
                    break

        path = os.path.join(
            os.path.dirname(os.path.abspath(args.project)), URBAN_TEXT_FILE
        )
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(sorted(inside), handle, indent=0)
            handle.write("\n")
        print(f"urban fills {len(fills)}, carto_text rows {rows}, inside {len(inside)}")
        print(f"wrote {path}")
        return 0
    finally:
        qgs.exitQgis()
