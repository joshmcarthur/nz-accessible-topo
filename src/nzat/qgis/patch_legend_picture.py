import posixpath

from nzat.qgis.legend_swatches import ACCESSIBLE_LEGEND_FILE, STOCK_LEGEND_FILE

LAYOUT_PICTURE = "65640"


def patch_legend_picture(root):
    """Point the layout legend picture at the accessible legend. Return a count."""
    count = 0
    for item in root.iter("LayoutItem"):
        if item.get("type") != LAYOUT_PICTURE:
            continue
        name = posixpath.basename(item.get("file") or "")
        if name in (STOCK_LEGEND_FILE, ACCESSIBLE_LEGEND_FILE):
            item.set("file", "./" + ACCESSIBLE_LEGEND_FILE)
            count += 1
    return count
