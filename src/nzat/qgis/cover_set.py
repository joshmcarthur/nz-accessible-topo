from pathlib import Path

from nzat.qgis.render_jobs import DPI, PX
from nzat.qgis.sample_grid import BX24_EXTENT, CELL_M, CELL_PX, crop_name

IN_SITU_M = 1000
IN_SITU_DPI = DPI
IN_SITU_PX = PX
BBOX_AREA = "(t.bbox.xmax - t.bbox.xmin) * (t.bbox.ymax - t.bbox.ymin)"
# These tables exist, but Map5View-all does not draw them. Crops would be landscape only.
MAP_ALL_OFF = frozenset({"place_point", "transport_point"})


def cell_origin(x, y, cell_m=CELL_M, origin=None):
    """Return the south-west NZTM corner of the 4 km cell that holds the point.

    The origin matches the BX24 review grid, so extra squares use the same phase.
    """
    ox, oy = BX24_EXTENT[:2] if origin is None else origin
    return (
        int(ox + int((x - ox) // cell_m) * cell_m),
        int(oy + int((y - oy) // cell_m) * cell_m),
    )


def in_extent(x, y, extent=BX24_EXTENT):
    xmin, ymin, xmax, ymax = extent
    return xmin <= x < xmax and ymin <= y < ymax


def greedy_cells(hits, cell_m=CELL_M):
    """Pick 4 km cells that cover the most remaining keys until none remain.

    hits is a list of dicts with keys key, x, y. Returns (cells, leftover_keys).
    Each cell is {east, north, keys}.
    """
    remaining = {hit["key"] for hit in hits}
    by_cell = {}
    for hit in hits:
        cell = cell_origin(hit["x"], hit["y"], cell_m)
        by_cell.setdefault(cell, set()).add(hit["key"])
    chosen = []
    while remaining:
        best = max(by_cell, key=lambda cell: len(by_cell[cell] & remaining))
        covered = by_cell[best] & remaining
        if not covered:
            break
        chosen.append({"east": best[0], "north": best[1], "keys": sorted(covered)})
        remaining -= covered
    return chosen, sorted(remaining)


def in_situ_extent(x, y, metres=IN_SITU_M):
    """Return a square centred on the hit, not a south-west grid cell."""
    half = metres / 2
    return (x - half, y - half, x + half, y + half)


def map_png_name(key):
    return f"{key}-map.png"


def paints_on_map_all(parquet):
    return parquet is not None and parquet not in MAP_ALL_OFF


def map_paint_note(parquet):
    if parquet is None:
        return "No national type"
    if parquet in MAP_ALL_OFF:
        return f"{parquet} is off on Map5View-all"
    return None


def extra_square_jobs(extras, out_dir):
    jobs = []
    for cell in extras:
        east, north = int(cell["east"]), int(cell["north"])
        jobs.append(
            {
                "extent": cell["extent"],
                "width": CELL_PX,
                "height": CELL_PX,
                "dpi": 300,
                "output": str(Path(out_dir) / crop_name(east, north, "accessible")),
            }
        )
    return jobs


def in_situ_jobs(hits, out_dir):
    jobs = []
    for hit in hits:
        if not paints_on_map_all(hit.get("parquet")):
            continue
        jobs.append(
            {
                "extent": in_situ_extent(hit["x"], hit["y"]),
                "width": IN_SITU_PX,
                "height": IN_SITU_PX,
                "dpi": IN_SITU_DPI,
                "output": str(Path(out_dir) / map_png_name(hit["key"])),
            }
        )
    return jobs


def split_base_hits(hits, extent=BX24_EXTENT):
    """Keep BX24 keys on the existing grid. Extra hits are keys BX24 does not hold."""
    base_keys = {hit["key"] for hit in hits if in_extent(hit["x"], hit["y"], extent)}
    extra = [hit for hit in hits if hit["key"] not in base_keys]
    return sorted(base_keys), extra
