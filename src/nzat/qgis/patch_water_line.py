from nzat.qgis.defaults import STYLE
from nzat.qgis.properties_map import properties_map
from nzat.qgis.put_expr import put_expr


def water_line_width_expression(water):
    """Drains draw thinner than rivers and canals, so the plain keeps a hierarchy."""
    return (
        f"CASE WHEN \"type\" = 'drain' THEN {water['drain_width_mm']} "
        f"ELSE {water['stream_width_mm']} END"
    )


def patch_water_line(layer, style=None):
    """Width by water_line type. Stock draws every type at 0.1 mm."""
    style = style or STYLE
    expression = water_line_width_expression(style["water"])
    for symbol_layer in layer.findall(".//symbol/layer[@class='SimpleLine']"):
        dd = symbol_layer.find("data_defined_properties")
        if dd is None:
            continue
        props = properties_map(dd)
        if props is None:
            continue
        put_expr(props, "outlineWidth", expression)
