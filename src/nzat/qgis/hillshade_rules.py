from nzat.qgis.defaults import STYLE


def hillshade_rules(style=None):
    """Return the hillshade block. Values live in tools/style-topo50.json."""
    return (style or STYLE)["hillshade"]
