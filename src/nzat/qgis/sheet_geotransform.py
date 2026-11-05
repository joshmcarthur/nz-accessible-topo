def sheet_geotransform(xmin, ymin, xmax, ymax, width, height):
    """Return the GDAL geotransform for a north-up image that fills the NZTM box."""
    return (xmin, (xmax - xmin) / width, 0.0, ymax, 0.0, -(ymax - ymin) / height)
