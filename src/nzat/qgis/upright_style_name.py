from nzat.qgis.defaults import STYLE


def upright_style_name(style, style_file=None):
    """Map a named font style onto the upright face we can ship."""
    fallback = (style_file or STYLE)["fonts"]["raster_upright_style"]
    text = (style or "").strip().lower()
    if not text or "italic" in text or "narrow" in text:
        return fallback
    return style
