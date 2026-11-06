import argparse
import os
import sys
import time

from nzat.qgis.font_files import font_files
from nzat.qgis.map_layers import SHEET_PRESET
from nzat.qgis.open_map import open_map
from nzat.qgis.qgis_prefix import qgis_prefix
from nzat.qgis.render_image import render_image
from nzat.qgis.render_square_main import _free_gb
from nzat.qgis.sheet_file_name import sheet_file_name
from nzat.qgis.sheet_geotransform import sheet_geotransform
from nzat.qgis.sheet_pixel_size import sheet_pixel_size

FREE_FLOOR_GB = 8
PROGRESS_FILE = "progress.tsv"


def _read_sheets(index_path):
    """Return [(code, name, xmin, ymin, xmax, ymax)] from the map sheet layer, by code."""
    from qgis.core import QgsVectorLayer  # noqa: E402

    layer = QgsVectorLayer(index_path, "sheets", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"sheet index not loaded: {index_path}")
    sheets = []
    for feature in layer.getFeatures():
        box = feature.geometry().boundingBox()
        sheets.append(
            (
                feature["sheet_code"],
                feature["sheet_name"],
                box.xMinimum(),
                box.yMinimum(),
                box.xMaximum(),
                box.yMaximum(),
            )
        )
    return sorted(sheets)


def _write_geotiff(image, path, transform):
    """Write the QImage as an RGB, DEFLATE, tiled GeoTIFF in EPSG:2193."""
    import numpy  # noqa: E402
    from osgeo import gdal, osr  # noqa: E402
    from qgis.PyQt.QtGui import QImage  # noqa: E402

    gdal.UseExceptions()
    rgb = image.convertToFormat(QImage.Format.Format_RGB888)
    width, height = rgb.width(), rgb.height()
    buffer = numpy.frombuffer(rgb.constBits().asstring(rgb.sizeInBytes()), numpy.uint8)
    pixels = buffer.reshape(height, rgb.bytesPerLine())[:, : width * 3]
    pixels = pixels.reshape(height, width, 3)

    memory = gdal.GetDriverByName("MEM").Create("", width, height, 3, gdal.GDT_Byte)
    memory.SetGeoTransform(transform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(2193)
    memory.SetProjection(srs.ExportToWkt())
    for band in range(3):
        memory.GetRasterBand(band + 1).WriteArray(pixels[:, :, band])
    partial = path + ".part"
    out = gdal.GetDriverByName("GTiff").CreateCopy(
        partial,
        memory,
        options=[
            "COMPRESS=DEFLATE",
            "PREDICTOR=2",
            "TILED=YES",
            "PHOTOMETRIC=RGB",
        ],
    )
    if out is None:
        raise RuntimeError(f"failed to write {partial}")
    out = None
    os.replace(partial, path)


def main():
    os.environ.setdefault("HOME", "/tmp")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    parser = argparse.ArgumentParser(
        description="Render each Topo50 sheet face to a georeferenced GeoTIFF."
    )
    parser.add_argument("--project", required=True, help="Path to the .qgs file")
    parser.add_argument(
        "--font",
        action="append",
        default=[],
        help="A font file or a directory of .otf and .ttf files",
    )
    parser.add_argument(
        "--index", required=True, help="nztopo50_map_sheet.parquet (sheet bboxes)"
    )
    parser.add_argument(
        "--out-dir", required=True, help="Folder for one .tif per sheet"
    )
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument(
        "--sheet", action="append", default=[], help="Only this sheet code"
    )
    parser.add_argument(
        "--theme",
        default=SHEET_PRESET,
        help="QGIS map theme. Map5View-paper and Map5View-all exist after apply.",
    )
    args = parser.parse_args()

    from qgis.core import QgsApplication  # noqa: E402

    os.makedirs(args.out_dir, exist_ok=True)
    progress = os.path.join(args.out_dir, PROGRESS_FILE)
    fonts = font_files(args.font)
    prefix = qgis_prefix(os.environ.get("QGIS_PREFIX_PATH"))
    print(f"qgis prefix {prefix}", flush=True)
    QgsApplication.setPrefixPath(prefix, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    failed = 0
    try:
        try:
            sheets = _read_sheets(args.index)
            if args.sheet:
                sheets = [sheet for sheet in sheets if sheet[0] in args.sheet]
            session = open_map(args.project, fonts, args.theme)
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 1
        print(f"sheets {len(sheets)} dpi {args.dpi}", flush=True)

        for number, (code, name, xmin, ymin, xmax, ymax) in enumerate(sheets, 1):
            output = os.path.join(args.out_dir, sheet_file_name(code))
            if os.path.exists(output):
                continue
            free = _free_gb(args.out_dir)
            if free is not None and free < FREE_FLOOR_GB:
                print(
                    f"free disk is {free:.1f} GB. Stop. The floor is {FREE_FLOOR_GB} GB.",
                    file=sys.stderr,
                )
                return 1
            width, height = sheet_pixel_size(xmin, ymin, xmax, ymax, args.dpi)
            start = time.monotonic()
            try:
                image = render_image(
                    session, xmin, ymin, xmax, ymax, width, height, args.dpi
                )
                if image.isNull():
                    raise RuntimeError("empty image")
                _write_geotiff(
                    image,
                    output,
                    sheet_geotransform(xmin, ymin, xmax, ymax, width, height),
                )
            except RuntimeError as error:
                failed += 1
                print(f"failed {code}: {error}", file=sys.stderr, flush=True)
                continue
            seconds = time.monotonic() - start
            size = os.path.getsize(output)
            line = f"{code}\t{name}\t{width}x{height}\t{seconds:.1f}\t{size}"
            with open(progress, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")
            print(f"[{number}/{len(sheets)}] {line}", flush=True)
    finally:
        qgs.exitQgis()
    print(f"done, failed {failed}", flush=True)
    return 1 if failed else 0
