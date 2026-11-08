import argparse
import json
import os
import sys
from pathlib import Path

import duckdb
from pyproj import Transformer

from nzat.qgis.cover_set import (
    BBOX_AREA,
    CELL_M,
    extra_square_jobs,
    greedy_cells,
    in_situ_jobs,
    split_base_hits,
)
from nzat.qgis.font_files import font_files
from nzat.qgis.qgis_prefix import qgis_prefix
from nzat.qgis.sample_grid import BX24_EXTENT
from nzat.qgis.symbol_queries import QUERIES, missing_symbol_keys

DEFAULT_DATA = (
    Path.home() / "Projects/github.com/linz/topo50-bx24/squares/accessible-sheets"
)
_TO_NZTM = Transformer.from_crs(4326, 2193, always_xy=True)
_TO_WGS = Transformer.from_crs(2193, 4326, always_xy=True)


def _bx24_lonlat():
    lons = []
    lats = []
    for east in (BX24_EXTENT[0], BX24_EXTENT[2]):
        for north in (BX24_EXTENT[1], BX24_EXTENT[3]):
            lon, lat = _TO_WGS.transform(east, north)
            lons.append(lon)
            lats.append(lat)
    return min(lons), min(lats), max(lons), max(lats)


def _parquet_is_lonlat(con, path, cache):
    if path not in cache:
        xmin = con.execute(
            "SELECT min(bbox.xmin) FROM read_parquet(?)", [path]
        ).fetchone()[0]
        cache[path] = xmin is not None and xmin <= 180
    return cache[path]


def _to_nztm(x, y, lonlat):
    if lonlat:
        return _TO_NZTM.transform(x, y)
    return x, y


def _hit_sql(where, extra=""):
    return f"""
        SELECT
            (t.bbox.xmin + t.bbox.xmax) / 2.0 AS x,
            (t.bbox.ymin + t.bbox.ymax) / 2.0 AS y
        FROM read_parquet(?) t
        WHERE ({where}) {extra}
        ORDER BY {BBOX_AREA} ASC
        LIMIT 1
    """


def _one_hit(con, data_dir, query, lonlat, bx24_box):
    path = str(Path(data_dir) / f"{query['parquet']}.parquet")
    xmin, ymin, xmax, ymax = bx24_box
    local_extra = (
        "AND (t.bbox.xmin + t.bbox.xmax) / 2.0 >= ? "
        "AND (t.bbox.xmin + t.bbox.xmax) / 2.0 < ? "
        "AND (t.bbox.ymin + t.bbox.ymax) / 2.0 >= ? "
        "AND (t.bbox.ymin + t.bbox.ymax) / 2.0 < ?"
    )
    local = con.execute(
        _hit_sql(query["where"], local_extra),
        [path, xmin, xmax, ymin, ymax],
    ).fetchone()
    if local:
        east, north = _to_nztm(local[0], local[1], lonlat)
        return east, north, True
    row = con.execute(_hit_sql(query["where"]), [path]).fetchone()
    if not row:
        return None
    east, north = _to_nztm(row[0], row[1], lonlat)
    return east, north, False


def _sheet_for_point(con, index_path, x, y):
    sql = """
        SELECT t.sheet_code, t.sheet_name
        FROM read_parquet(?) t
        WHERE t.bbox.xmin <= ? AND t.bbox.xmax >= ?
          AND t.bbox.ymin <= ? AND t.bbox.ymax >= ?
        ORDER BY t.sheet_code
        LIMIT 1
    """
    row = con.execute(sql, [str(index_path), x, x, y, y]).fetchone()
    if not row:
        return None, None
    return row[0], row[1]


def collect_hits(con, data_dir, index_path):
    hits = []
    absent = []
    empty = []
    crs_cache = {}
    bx24_nztm = BX24_EXTENT
    bx24_wgs = _bx24_lonlat()
    for query in QUERIES:
        if query["parquet"] is None:
            absent.append({"key": query["key"], "reason": query["reason"]})
            continue
        path = str(Path(data_dir) / f"{query['parquet']}.parquet")
        lonlat = _parquet_is_lonlat(con, path, crs_cache)
        box = bx24_wgs if lonlat else bx24_nztm
        found = _one_hit(con, data_dir, query, lonlat, box)
        if found is None:
            empty.append({"key": query["key"], "parquet": query["parquet"]})
            continue
        x, y, on_bx24 = found
        code, name = _sheet_for_point(con, index_path, x, y)
        hits.append(
            {
                "key": query["key"],
                "x": x,
                "y": y,
                "on_bx24": on_bx24,
                "sheet_code": code,
                "sheet_name": name,
                "parquet": query["parquet"],
                "reason": query["reason"],
            }
        )
    return hits, absent, empty


def build_report(hits, absent, extra_cells):
    by_key = {hit["key"]: hit for hit in hits}
    extras = []
    for cell in extra_cells:
        keys = cell["keys"]
        examples = [by_key[key] for key in keys]
        extras.append(
            {
                "east": cell["east"],
                "north": cell["north"],
                "extent": [
                    cell["east"],
                    cell["north"],
                    cell["east"] + CELL_M,
                    cell["north"] + CELL_M,
                ],
                "keys": keys,
                "sheet_code": examples[0]["sheet_code"],
                "sheet_name": examples[0]["sheet_name"],
            }
        )
    return extras


def _render_jobs(session, jobs):
    from nzat.qgis.render_image import render_image

    wrote = 0
    skipped = 0
    for job in jobs:
        output = Path(job["output"])
        if output.exists():
            skipped += 1
            print(f"skip {output}")
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        xmin, ymin, xmax, ymax = job["extent"]
        image = render_image(
            session,
            xmin,
            ymin,
            xmax,
            ymax,
            job["width"],
            job["height"],
            job["dpi"],
        )
        if image.isNull() or not image.save(str(output)):
            print(f"failed to write {output}", file=sys.stderr)
            return None
        wrote += 1
        print(f"wrote {output} {image.width()}x{image.height()}")
    return wrote, skipped


def render_on_map(project, fonts, theme, jobs):
    """Draw each job. Skip a PNG that already exists. One QGIS session."""
    from qgis.core import QgsApplication  # noqa: E402

    from nzat.qgis.open_map import open_map

    prefix = qgis_prefix(os.environ.get("QGIS_PREFIX_PATH"))
    QgsApplication.setPrefixPath(prefix, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        session = open_map(project, font_files(fonts), theme)
        result = _render_jobs(session, jobs)
    finally:
        qgs.exitQgis()
    if result is None:
        return 1
    wrote, skipped = result
    print(f"render wrote {wrote} skipped {skipped}")
    return 0


def main():
    missing, extra = missing_symbol_keys()
    if missing or extra:
        print(
            f"query list does not match SYMBOLS missing={missing} extra={extra}",
            file=sys.stderr,
        )
        return 1
    parser = argparse.ArgumentParser(
        description="Find 4 km squares that cover legend classes absent from BX24."
    )
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA))
    parser.add_argument(
        "--index",
        default="",
        help="Sheet index parquet. Default: <data-dir>/nztopo50_map_sheet.parquet",
    )
    parser.add_argument("--out", help="Write JSON here. Also prints a short table.")
    parser.add_argument(
        "--render-dir",
        help="Write 4 km PNGs (945 px, 300 dpi, Map5View-all). Skip files that exist.",
    )
    parser.add_argument(
        "--in-situ-dir",
        help="Write 1 km 600 dpi crops centred on each hit. Skip files that exist.",
    )
    parser.add_argument(
        "--project",
        default="",
        help="QGIS project for --render-dir. Default: <data-dir>/nztopo50.qgs",
    )
    parser.add_argument(
        "--font",
        action="append",
        default=[],
        help="Font file or directory for --render-dir",
    )
    parser.add_argument("--theme", default="Map5View-all")
    args = parser.parse_args()
    index_path = args.index or str(Path(args.data_dir) / "nztopo50_map_sheet.parquet")
    con = duckdb.connect()
    hits, absent, empty = collect_hits(con, args.data_dir, index_path)
    if empty:
        print(f"queries with no rows: {empty}", file=sys.stderr)
    base_keys, extra_hits = split_base_hits(hits)
    extra_cells, leftover = greedy_cells(extra_hits)
    extras = build_report(hits, absent, extra_cells)
    report = {
        "cell_m": CELL_M,
        "bx24_extent": list(BX24_EXTENT),
        "bx24_keys": base_keys,
        "hits": hits,
        "absent": absent,
        "empty_queries": empty,
        "leftover_keys": leftover,
        "extra_squares": extras,
    }
    text = json.dumps(report, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(f"hits {len(hits)} bx24 {len(base_keys)} extra_squares {len(extras)}")
    print(f"absent {len(absent)} empty {len(empty)} leftover {leftover}")
    for cell in extras:
        print(
            f"{cell['east']}-{cell['north']}\t{cell['sheet_code']}\t"
            f"{cell['sheet_name']}\t{','.join(cell['keys'])}"
        )
    if not args.render_dir and not args.in_situ_dir:
        return 0
    project = args.project or str(Path(args.data_dir) / "nztopo50.qgs")
    fonts = args.font or [
        str(Path.home() / "Projects/github.com/linz/topo50-bx24/accessible/fonts")
    ]
    jobs = []
    if args.render_dir:
        jobs.extend(extra_square_jobs(extras, args.render_dir))
    if args.in_situ_dir:
        jobs.extend(in_situ_jobs(hits, args.in_situ_dir))
    return render_on_map(project, fonts, args.theme, jobs)
