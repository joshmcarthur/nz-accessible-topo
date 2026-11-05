def legend_box_extent(box, metres_per_px):
    """Return xmin, ymin, xmax, ymax, width, height for a legend pixel box."""
    x0, y0, x1, y1 = box
    return (
        x0 * metres_per_px,
        -y1 * metres_per_px,
        x1 * metres_per_px,
        -y0 * metres_per_px,
        x1 - x0,
        y1 - y0,
    )
