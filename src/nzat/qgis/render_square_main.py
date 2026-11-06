import argparse
import os
import sys

from nzat.qgis.font_files import font_files
from nzat.qgis.map_layers import SHEET_PRESET
from nzat.qgis.open_map import open_map
from nzat.qgis.qgis_prefix import qgis_prefix
from nzat.qgis.render_image import render_image
from nzat.qgis.render_jobs import render_jobs


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

    parser = argparse.ArgumentParser(
        description="Render 1 km map squares at 600 dpi, or one rectangle at a given size."
    )
    parser.add_argument("--project", required=True, help="Path to the .qgs file")
    parser.add_argument(
        "--font",
        action="append",
        default=[],
        help="A font file or a directory of .otf and .ttf files",
    )
    parser.add_argument(
        "--square", action="append", default=[], help="EAST,NORTH,OUTPUT.png"
    )
    parser.add_argument("--extent", help="xmin,ymin,xmax,ymax")
    parser.add_argument("--dpi", type=int, help="Output dpi with --extent")
    parser.add_argument(
        "--width", type=int, help="Output width in pixels with --extent"
    )
    parser.add_argument(
        "--height", type=int, help="Output height in pixels with --extent"
    )
    parser.add_argument("--output", help="OUTPUT.png with --extent")
    parser.add_argument(
        "--theme",
        default=SHEET_PRESET,
        help="QGIS map theme. Map5View-paper and Map5View-all exist after apply.",
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
    from qgis.core import QgsApplication  # noqa: E402

    try:
        jobs = render_jobs(
            [_parse_square(item) for item in args.square],
            extent=args.extent,
            output=args.output,
            width=args.width,
            height=args.height,
            dpi=args.dpi,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    fonts = font_files(args.font)

    prefix = qgis_prefix(os.environ.get("QGIS_PREFIX_PATH"))
    print(f"qgis prefix {prefix}")
    QgsApplication.setPrefixPath(prefix, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        try:
            session = open_map(args.project, fonts, args.theme)
        except RuntimeError as error:
            print(error, file=sys.stderr)
            return 1

        for xmin, ymin, xmax, ymax, width, height, dpi, output in jobs:
            os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
            image = render_image(session, xmin, ymin, xmax, ymax, width, height, dpi)
            if image.isNull() or not image.save(output):
                print(f"failed to write {output}", file=sys.stderr)
                return 1
            print(f"wrote {output} {image.width()}x{image.height()}")
    finally:
        qgs.exitQgis()
    return 0
